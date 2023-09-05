import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# Read the TSLA stock data
df = pd.read_csv('stock_data/PFE.csv')

# Convert the date column to a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Select the relevant columns
df = df[['Date', 'Close']]

# Calculate average closing values by month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
monthly_avg = df.groupby(['Year', 'Month'])['Close'].mean().reset_index()

# Create a new column 'Date' as the first day of each month
monthly_avg['Date'] = pd.to_datetime(monthly_avg[['Year', 'Month']].assign(day=1))

# Plot the historical and forecasted monthly average closing values
plt.plot(monthly_avg['Date'], monthly_avg['Close'], marker='o', linestyle='-', color='b', label='Historical')
plt.title('Average Monthly Closing Price')
plt.xlabel('Date')
plt.ylabel('Average Closing Price')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Prepare data for ARIMA
closing_prices = monthly_avg['Close']

# Initialize and fit ARIMA model
order = (5, 1, 0)  # Example order (p, d, q)
model = ARIMA(closing_prices, order=order)
model_fit = model.fit()

# Forecast future values
forecast_steps = 12  # Forecast next 12 months
forecast = model_fit.forecast(steps=forecast_steps)

# Plot the forecast
plt.figure()
plt.plot(monthly_avg['Date'], monthly_avg['Close'], marker='o', linestyle='-', color='b', label='Historical')
plt.plot(pd.date_range(start=monthly_avg['Date'].iloc[-1], periods=forecast_steps, freq='M'), forecast,
         color='r', marker='o', linestyle='-', label='Forecast')
plt.title('Average Monthly Closing Price Forecast with ARIMA')
plt.xlabel('Date')
plt.ylabel('Average Closing Price')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.legend()

plt.show()

# Calculate and print RMSE
actual = monthly_avg['Close'].iloc[-forecast_steps:]
rmse = np.sqrt(mean_squared_error(actual, forecast))
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
