
#install.packages("")
#install.packages("DBI")
#install.packages("odbc")
#install.packages("lubridate")
#install.packages("dplyr")
#install.packages("ggplot2")
#install.packages("forecast")
#install.packages("tseries")
#install.packages("urca")

#library()
library(DBI)
library(odbc)
library(lubridate)
library(dplyr)
library(ggplot2)
library(forecast)


con <- dbConnect(
  odbc::odbc(), 
  Driver = "ODBC Driver 17 for SQL Server",  # Verify your installed driver name
  Server = "QUAN\\SQLEXPRESS",  # Include port if needed (e.g., 1433)
  Database = "gt_cse6242",           # Name of the database
  Trusted_Connection = "Yes"                # Enables Windows Authentication
)

df <- dbGetQuery(con, "SELECT * FROM gt_cse6242.[dbo].spd_dataset_modified_v2")

# Check the first few rows
head(df)

# Aggregate monthly counts
df_monthly <- df %>%
  mutate(year_month = floor_date(call_sign_dispatch_date, "month")) %>%
  count(year_month, name = "count")

ggplot(df_monthly, aes(x = year_month, y = count)) +
  geom_line(color = "blue") +
  labs(title = "Monthly Incident Counts Over Time", x = "Year-Month", y = "Number of Cases") +
  theme_minimal()

# Convert to a time series
ts_data <- ts(df_monthly$count, frequency = 12, start = c(year(min(df$call_sign_dispatch_date)), month(min(df$call_sign_dispatch_date))))

# Decompose into trend, seasonality, and residuals
decomposed <- decompose(ts_data, type = "multiplicative")
plot(decomposed)

# KPSS Test for seasonality
library(tseries)

kpss.test(ts_data, null = "Level")

acf(ts_data, lags = 12, main = "Autocorrelation (Seasonal Lags)")

library(urca)

# Original KPSS test (level)
kpss.test(ts_data, null = "Level")  # Rejects stationarity

# KPSS test (trend)
kpss.test(ts_data, null = "Trend")  # Check if trend explains non-stationarity

# ADF test
adf_test <- ur.df(ts_data, type = "drift")  # Tests for unit root
summary(adf_test)

# Differencing
ts_data_diff <- diff(ts_data, differences = 1)
plot(ts_data_diff, main = "Differenced Time Series")

# Re-test stationarity
kpss.test(ts_data_diff, null = "Level")

# Fit ARIMA model to differenced data
library(forecast)

arima_model <- Arima(ts_data_diff, order = c(0,1,1), include.drift = TRUE)

# Generate forecasts
forecast_values <- forecast(arima_model, h = 12)

# Generate future dates
last_date <- as.Date("2025-09-29")
future_dates <- seq(last_date, by = "month", length.out = 12)

# Create data frame
forecast_df <- data.frame(
  Date = future_dates,
  Forecast = forecast_values$mean,
  Lower_80 = forecast_values$lower[, 1],
  Upper_80 = forecast_values$upper[, 1],
  Lower_95 = forecast_values$lower[, 2],
  Upper_95 = forecast_values$upper[, 2]
)

# Export to CSV
write.csv(forecast_df, "forecast_results.csv", row.names = FALSE)

ts_data <- ts(df_monthly$count, frequency = 12, 
              start = c(year(min(df$call_sign_dispatch_date)), 
                        month(min(df$call_sign_dispatch_date))))

# Decompose into trend, seasonality, and residuals
decomposed <- decompose(ts_data, type = "multiplicative")

# Extract the 12 unique seasonal indices (January to December)
seasonal_indices <- decomposed$seasonal[1:12]

# Create a data frame with month names and seasonal indices
seasonal_df <- data.frame(
  Month = month.name[1:12],  # Full month names (January to December)
  Seasonal_Index = seasonal_indices
)

# Print the seasonal formula to the console
print(seasonal_df)

# Save the seasonal formula to a CSV file
write.csv(seasonal_df, "seasonal_formula.csv", row.names = FALSE)

# Optional: Plot the seasonal component for visualization
plot(decomposed$seasonal, main = "Seasonal Component (Monthly Indices)", xlab = "Month", ylab = "Seasonal Index")
