from alpha_vantage.timeseries import TimeSeries
import pandas as pd

def GetStockSummary(symbol, api_key, days):
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta = ts.get_daily(symbol=symbol, outputsize='full')

        data.index = pd.to_datetime(data.index)
        one_year_ago = pd.Timestamp.today() - pd.Timedelta(days=days)
        recent_data = data[data.index >= one_year_ago]

        recent_data = recent_data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })

        lines = []
        for i in range(len(recent_data)):
            row = recent_data.iloc[i]
            date = recent_data.index[i].strftime('%B %d, %Y')
            line = "- " + date + ": Open " + str(round(row['Open'], 2)) + ", High " + str(round(row['High'], 2)) + ", Low " + str(round(row['Low'], 2)) + ", Close " + str(round(row['Close'], 2)) + ", Volume " + str(round(row['Volume'] / 1000000, 1)) + "M"
            lines.append(line)

        return "\n".join(lines)

    except Exception as e:
        return "Something went wrong: " + str(e)
