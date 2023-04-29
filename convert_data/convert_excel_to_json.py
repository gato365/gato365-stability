
import pandas as pd
from datetime import datetime

# Load the Excel sheet
file_path = 'emans_data_lite.xlsx'
df = pd.read_excel(file_path)

# Filter the date variable to include only dates after "Saturday, July 16, 2022"
date_threshold = datetime.strptime("Saturday, July 16, 2022", "%A, %B %d, %Y")
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Date'] > date_threshold]

# Time points
time_points = ['4:00 am', '7:45 am', '10:45 am', '12:00 pm', '3:00 pm', '6:00 pm', '8:30 pm']


# Function to split columns based on time points and create new rows
def split_columns(row):
    try:
        goals = row['Goals'].split(';')[:7]
    except AttributeError:
        goals = ['NA'] * 7

    try:
        food_quality = row['Food_Quality'].split(';')[:7]
    except AttributeError:
        food_quality = ['NA'] * 7

    try:
        mood = row['Mood'].split(';')[:7]
    except AttributeError:
        mood = ['NA'] * 7

    # Pad with NAs if there are fewer than 6 ';' characters
    goals.extend(['NA'] * (7 - len(goals)))
    food_quality.extend(['NA'] * (7 - len(food_quality)))
    mood.extend(['NA'] * (7 - len(mood)))

    new_rows = []
    for i in range(len(time_points)):
        new_row = row.copy()
        new_row['Time'] = time_points[i]
        new_row['Goals'] = goals[i]
        new_row['Food_Quality'] = food_quality[i]
        new_row['Mood'] = mood[i]
        new_rows.append(new_row)

    return new_rows


# Apply the function to split columns and create new rows
expanded_data = []
for _, row in df.iterrows():
    expanded_data.extend(split_columns(row))

# Create a new DataFrame with the expanded data
df_expanded = pd.DataFrame(expanded_data)

# Save the expanded DataFrame to a JSON file
json_data = df_expanded.to_json(orient='records', date_format='iso')
output_file_path = 'output_expanded.json'
with open(output_file_path, 'w') as f:
    f.write(json_data)

print(f"Expanded JSON data saved to {output_file_path}")
