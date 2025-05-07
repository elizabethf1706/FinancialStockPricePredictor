import yfinance as yf
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error, mean_squared_error

def get_stock_data(ticker, period="1y"):
    """
    get historical stock data from Yahoo
    
    Args:
        ticker (str): stock ticker symbol
        period (str): time to download (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
    Returns:
        dataframe with stock data
    """
    try:
    
        ticker = ticker.upper().strip()
        data = yf.download(ticker, period=period)
    
        if data.empty:
            return None
            
        return data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def prepare_data_for_prophet(stock_data):
    """
    get stock data ready for prophet model.
    
    Args:
        stock_data (DataFrame): stock data from Yahoo 
        
    Returns:
        cleaned up dataframe
    """
    try:
        prophet_data = stock_data.reset_index().copy()
        
        if 'Date' not in prophet_data.columns:
            print("Date column not found in stock data")
            return None
        
        # clean up the data
        prophet_df = pd.DataFrame()
        prophet_df['ds'] = pd.to_datetime(prophet_data['Date']) 
        prophet_df['y'] = prophet_data['Close'].astype(float)   
        
        # drop any rows with NaN values
        if prophet_df['y'].isna().any():
            prophet_df = prophet_df.dropna(subset=['y'])
            
        # print some diagnostics
        print(f"Prophet data shape: {prophet_df.shape}")
        print(f"ds dtype: {prophet_df['ds'].dtype}")
        print(f"y dtype: {prophet_df['y'].dtype}")
            
        return prophet_df
    except Exception as e:
        print(f"Error preparing data for Prophet: {e}")
        return None

def train_prophet_model(data, prediction_days=30):
    """
    trainthe Prophet model and generate predictions.
    
    Args:
        data (DataFrame): data formatted for Prophet (with 'ds' and 'y' columns)
        prediction_days (int): number of days to predict into the future
        
    Returns:
        tuple: (model, forecast DataFrame)
    """
    if data is None or len(data) < 10:
        print("Insufficient data for forecasting")
        return None, None
        
    try:
        model = Prophet(
            daily_seasonality=False,
            yearly_seasonality=True,
            weekly_seasonality=True,
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0
        )
        
        model.fit(data)
        future = model.make_future_dataframe(periods=prediction_days)
        forecast = model.predict(future)
        
        return model, forecast
    except Exception as e:
        print(f"Error training Prophet model: {e}")
        return None, None

def evaluate_model(model, forecast, actual_data):
    """
    see how the Prophet model performs.
    
    Args:
        model (Prophet): the trained Prophet model
        forecast (DataFrame): the forecast from the model
        actual_data (DataFrame): the actual stock data for comparison
        
    Returns:
        dict: metrics
    """
    if model is None or forecast is None or actual_data is None or actual_data.empty:
        return {
            'mae': 0,
            'mse': 0,
            'rmse': 0,
            'mape': 0
        }
    
    try:
        evaluation_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].merge(
            actual_data[['ds', 'y']], on='ds', how='inner'
        )
        
        # check if we have enough data to evaluate
        if len(evaluation_df) < 2:
            return {
                'mae': 0,
                'mse': 0,
                'rmse': 0,
                'mape': 0
            }
        
        # do some metrics
        mae = mean_absolute_error(evaluation_df['y'], evaluation_df['yhat'])
        mse = mean_squared_error(evaluation_df['y'], evaluation_df['yhat'])
        rmse = np.sqrt(mse)
        
        #  just get the mape
        mask = evaluation_df['y'] > 1e-8
        if mask.any():
            mape = np.mean(np.abs((evaluation_df.loc[mask, 'y'] - evaluation_df.loc[mask, 'yhat']) / 
                                   evaluation_df.loc[mask, 'y'])) * 100
        else:
            mape = 0
        
        metrics = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mape': mape
        }
        
        return metrics
    except Exception as e:
        print(f"Error evaluating model: {e}")
        return {
            'mae': 0,
            'mse': 0,
            'rmse': 0,
            'mape': 0
        }
