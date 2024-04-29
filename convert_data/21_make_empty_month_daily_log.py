import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create a date range for April 2024
date_range = pd.date_range(start="2024-05-01", end="2024-05-31", freq='D')

# Define the time periods
time_periods = ["4:00 AM", "7:45 AM", "10:45 AM", "12:00 PM", "3:00 PM", "6:00 PM", "8:30 PM"]

# Repeat the time periods for each day of April 2024
time_period_list = np.tile(time_periods, len(date_range))

# Repeat each date for the number of time periods
date_list = np.repeat(date_range, len(time_periods))

# Create the DataFrame
df = pd.DataFrame({
    "Date": date_list,
    "Time Period": time_period_list,
    "Wake Up Time": [""] * len(date_list),
    "Actual Time": [""] * len(date_list),
    "Goal": [""] * len(date_list),
    "Mood": [""] * len(date_list),
    "Food Quality": [""] * len(date_list),
    "MJ": [""] * len(date_list),
    "Alcohol": [""] * len(date_list),
    "Eat Out": [""] * len(date_list),
    "Is_late": [""] * len(date_list),
    "weight": [""] * len(date_list),
    "type": [""] * len(date_list),
    "time": [""] * len(date_list),
    "Notes": [""] * len(date_list)
})

df.to_csv("may_2024.csv")
