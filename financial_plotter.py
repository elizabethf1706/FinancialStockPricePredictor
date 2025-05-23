import plotly.graph_objects as go
import pandas as pd

def _prepare_plotting_data(stock_data_raw):
    if stock_data_raw is None or stock_data_raw.empty:
        return None
    
    stock_df = stock_data_raw.copy()

    if isinstance(stock_df.columns, pd.MultiIndex):
        if stock_df.columns.nlevels == 2:
            level_1_names = stock_df.columns.get_level_values(1).unique().tolist()
            common_fields = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
            if any(field in level_1_names for field in common_fields):
                stock_df.columns = stock_df.columns.get_level_values(1)
            else:
                stock_df.columns = stock_df.columns.get_level_values(0)
        elif stock_df.columns.nlevels == 1:
             stock_df.columns = stock_df.columns.get_level_values(0)

    if not isinstance(stock_df.index, pd.DatetimeIndex):
        stock_df.index = pd.to_datetime(stock_df.index, errors='coerce')
        if stock_df.index.isnull().any():
            return None
            
    cols_to_check = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col_name in cols_to_check:
        if col_name in stock_df.columns:
            if not isinstance(stock_df[col_name], pd.Series):
                 if isinstance(stock_df[col_name], pd.DataFrame) and len(stock_df[col_name].columns) == 1:
                     stock_df[col_name] = stock_df[col_name].iloc[:, 0]
                 else:
                     stock_df[col_name] = pd.Series([None] * len(stock_df))
            
            try:
                stock_df[col_name] = pd.to_numeric(stock_df[col_name], errors='coerce')
            except TypeError:
                stock_df[col_name] = pd.Series([None] * len(stock_df))
            except Exception:
                stock_df[col_name] = pd.Series([None] * len(stock_df))
        else:
            pass
            
    if 'Close' in stock_df.columns:
        if stock_df['Close'].isnull().all():
            return None
        stock_df.dropna(subset=['Close'], inplace=True)
        if stock_df.empty:
            return None
    else:
        return None
            
    return stock_df

#  plotting functions 

def plot_historical_price_with_volume(stock_data_raw, ticker_symbol):
    stock_data = _prepare_plotting_data(stock_data_raw)
    """
    historical price chart with a volume subplot

    Args:
        stock_data (pd.DataFrame): data frame with stock data, we have to have
                                   'Close' and 'Volume' columns and a datetime index.
        ticker_symbol (str): stock ticker 

    Returns:
        plotly.graph_objects.Figure: the plotly figure for the chart.
    """
    if stock_data is None or stock_data.empty:
        return go.Figure().update_layout(title_text=f"No data available for {ticker_symbol}")

    fig = go.Figure()

    # price line
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'],
                             mode='lines', name='Close Price',
                             line=dict(color='blue')))

    # volume bars
    fig.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'],
                         name='Volume', yaxis='y2',
                         marker_color='rgba(0,0,255,0.3)'))

    fig.update_layout(
        title_text=f'{ticker_symbol} - Historical Price and Volume',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(x=0.01, y=0.99, bordercolor='black', borderwidth=1),
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickangle=-45,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            nticks=10
        )
    )
    return fig 

def plot_candlestick_chart(stock_data_raw, ticker_symbol):
    stock_data = _prepare_plotting_data(stock_data_raw)
    """
    candlestick chart for the stock data.

    Args:
        stock_data (pd.DataFrame): data frame with stock data, we have to have
                                   'Open', 'High', 'Low', 'Close' columns
                                   and a datetime index.
        ticker_symbol (str): stock ticker 

    Returns:
        plotly.graph_objects.Figure: the plotly figure for the chart.
    """
    if stock_data is None or stock_data.empty or not all(col in stock_data.columns for col in ['Open', 'High', 'Low', 'Close']):
        return go.Figure().update_layout(title_text=f"OHLC data not available for {ticker_symbol} for Candlestick")

    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                           open=stock_data['Open'],
                                           high=stock_data['High'],
                                           low=stock_data['Low'],
                                           close=stock_data['Close'],
                                           name=ticker_symbol)])

    fig.update_layout(
        title_text=f'{ticker_symbol} - Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickangle=-45,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            nticks=10
        )
    )
    return fig 

def plot_price_with_moving_averages(stock_data_raw, ticker_symbol, short_window=50, long_window=200):
    stock_data = _prepare_plotting_data(stock_data_raw)
    """
    historical price chart with short and long-term moving averages.

    Args:
        stock_data (pd.DataFrame): data frame with stock data, we have to have
                                   'Close' column and a datetime index.
        ticker_symbol (str): stock ticker 
        short_window (int): window for the short-term moving average.
        long_window (int): window for the long-term moving average.

    Returns:
        plotly.graph_objects.Figure: the plotly figure for the chart.
    """
    if stock_data is None or stock_data.empty or 'Close' not in stock_data.columns:
        return go.Figure().update_layout(title_text=f"Close price data not available for {ticker_symbol} for Moving Averages")

    data_with_ma = stock_data.copy()
    data_with_ma[f'MA{short_window}'] = data_with_ma['Close'].rolling(window=short_window).mean()
    data_with_ma[f'MA{long_window}'] = data_with_ma['Close'].rolling(window=long_window).mean()

    fig = go.Figure()

    # price line
    fig.add_trace(go.Scatter(x=data_with_ma.index, y=data_with_ma['Close'],
                             mode='lines', name='Close Price',
                             line=dict(color='blue')))
    # short ma
    fig.add_trace(go.Scatter(x=data_with_ma.index, y=data_with_ma[f'MA{short_window}'],
                             mode='lines', name=f'{short_window}-Day MA',
                             line=dict(color='orange')))
    # long ma
    fig.add_trace(go.Scatter(x=data_with_ma.index, y=data_with_ma[f'MA{long_window}'],
                             mode='lines', name=f'{long_window}-Day MA',
                             line=dict(color='green')))

    fig.update_layout(
        title_text=f'{ticker_symbol} - Price and Moving Averages ({short_window}-day & {long_window}-day)',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        legend=dict(x=0.01, y=0.99, bordercolor='black', borderwidth=1),
        xaxis_rangeslider_visible=True,
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickangle=-45,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            nticks=10
        )
    )
    return fig