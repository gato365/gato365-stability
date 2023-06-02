import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data into a DataFrame
df = pd.read_excel("emans_data.xlsx")

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons
df = df[(df["Goals"].str.count(";") == 6) & (df["Mood"].str.count(";") == 6)]

# Only keep the 'Date', 'Goals', 'Mood', and 'Weight_AM' columns
df = df[["Date", "Goals", "Mood", "Weight_AM"]]

# Rename Weight_AM to Weight
df.rename(columns={"Weight_AM": "Weight"}, inplace=True)

# Convert 'Date' to a datetime object
df["Date"] = pd.to_datetime(df["Date"])
df["Goals"] = df["Goals"].str.split(";")
df["Mood"] = df["Mood"].str.split(";")

# Assign numerical values to the goals and calculate average goal
goal_dict = {
    "G-": -1,
    "G": 0,
    "G+": 1,
    "G-e": -1,
    "G+e": 1,
    "G-l": -1,
    "G+l": 1,
    "Gl": 0,
    "G": 0,
    "Ge": 0,
}
df["Average_Goal"] = df["Goals"].apply(
    lambda x: sum(goal_dict[i.strip()] for i in x if i.strip() in goal_dict) / len(x)
)

# Assign numerical values to the moods and calculate average mood
mood_dict = {
    "M-": -1,
    "M": 0,
    "M+": 1,
    "M-e": -1,
    "M+e": 1,
    "M-l": -1,
    "M+l": 1,
    "Ml": 0,
    "Me": 0,
}

df["Average_Mood"] = df["Mood"].apply(
    lambda x: mood_dict[x[0].strip()] if isinstance(x, list) and len(x) > 0 else np.nan
)

# Calculate the num_days-day rolling mean of 'Average_Goal', 'Average_Mood', and 'Weight'
num_days = 15
df["Average_Goal_30D"] = df["Average_Goal"].rolling(num_days).mean()
df["Average_Mood_30D"] = df["Average_Mood"].rolling(num_days).mean()
df["Weight_30D"] = df["Weight"].rolling(num_days).mean()

# Assign season based on month
def assign_season(month):
    if month in [3, 4, 5]:  # Spring
        return "Spring"
    elif month in [6, 7, 8]:  # Summer
        return "Summer"
    elif month in [9, 10, 11]:  # Fall
        return "Fall"
    else:  # Winter
        return "Winter"


df["Season"] = df["Date"].dt.month.apply(assign_season)

# Visualization of seasonal effects
seasons = ["Spring", "Summer", "Fall", "Winter"]


# Calculate correlation for each season
for season in seasons:
    season_df = df[df["Season"] == season]
    correlation_goals_weight = (
        season_df[["Average_Goal_30D", "Weight_30D"]].corr().iloc[0, 1]
    )
    correlation_mood_weight = (
        season_df[["Average_Mood_30D", "Weight_30D"]].corr().iloc[0, 1]
    )
    print(
        f"Correlation between Goals and Weight in {season}: {correlation_goals_weight}"
    )
    print(f"Correlation between Mood and Weight in {season}: {correlation_mood_weight}")

    # Create ratio between mood and goal
    df.loc[df["Season"] == season, "Mood_Goal_Ratio"] = (
        season_df["Average_Mood_30D"] / season_df["Average_Goal_30D"]
    )
    ## scale the ratio to be between 0 and 1
    df.loc[df["Season"] == season, "Mood_Goal_Ratio"] = (
        df.loc[df["Season"] == season, "Mood_Goal_Ratio"]
        - df.loc[df["Season"] == season, "Mood_Goal_Ratio"].min()
    ) / (
        df.loc[df["Season"] == season, "Mood_Goal_Ratio"].max()
        - df.loc[df["Season"] == season, "Mood_Goal_Ratio"].min()
    )


colors = ["green", "red", "orange", "blue"]
plt.figure(figsize=(10, 5))
for season, color in zip(seasons, colors):
    season_df = df[df["Season"] == season]
    plt.plot(
        season_df["Date"],
        season_df["Mood_Goal_Ratio"],
        color=color,
        label=f"{season} (Mood/Goal)",
    )
plt.xlabel("Date")
plt.ylabel("Mood/Goal Ratio")
plt.title("Seasonal Effects on Ratio between Mood and Goal")
plt.legend()
plt.show()
