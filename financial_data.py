import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# note to add alpha_vantage and pandas to requirements.
def get_StockSummary(api_key, symbol):
    try:
        ts = TimeSeries(key=api_key, output_format='pandas')
        data, meta = ts.get_daily(symbol=symbol, outputsize='full')

        data.index = pd.to_datetime(data.index)
        # Adjusted to use months=6 instead of fractional years
        six_months_ago = pd.Timestamp.today() - pd.DateOffset(months=6)
        recent_data = data[data.index >= six_months_ago]

        recent_data = recent_data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })

        lines = []
        for date, row in recent_data.iterrows():
            line = f"- {date.strftime('%B %d, %Y')}: Open {round(row['Open'], 2)}, High {round(row['High'], 2)}, Low {round(row['Low'], 2)}, Close {round(row['Close'], 2)}, Volume {round(row['Volume'] / 1_000_000, 1)}M"
            lines.append(line)

        return "\n".join(lines)

    except Exception as e:
        return "Something went wrong: " + str(e)
