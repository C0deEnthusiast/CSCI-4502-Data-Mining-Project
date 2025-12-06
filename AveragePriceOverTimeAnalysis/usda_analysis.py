import os
import pandas as pd
import matplotlib.pyplot as plt

# Critical macronutrients

# Target Tier-2 group column
CARBS = ['Non-whole-grain breads, cereal, rice, pasta, and flours','Potatoes','Other starchy vegetables']
AVG_CARB_CAL = 4

PROTEIN = ['Beef, pork, lamb, veal and game','Chicken, turkey, and game birds','Fish and seafood','Bacon, sausage, and lunch meats','Nuts, nut butters, and seeds','Tofu and meat substitutes','Egg and egg substitutes']
AVG_PROTEIN_CAL = 4

FATS = ['Fats, oils, and salad dressings']
AVG_FATS_CAL = 9


def aggregate_data_by_macro(nutrient_list, dataframe):
    filtered_df = dataframe[dataframe['Tier 2 group'].isin(nutrient_list)]

    # Aggregate by Year-Month pairs and take the average of each group
    return filtered_df.groupby(['Year','Month'])['Value'].mean().reset_index()


# def plot_data(agg_df, title):
#     agg_df['Date'] = pd.to_datetime(agg_df[['Year', 'Month']].assign(DAY=1))
    
#     plt.figure(figsize=(12, 6))
#     plt.plot(agg_df['Date'], agg_df['Value'], marker='o', linewidth=2, markersize=4)
#     plt.xlabel('Date')
#     plt.ylabel('Average Price per 1000 Calories ($)')
#     plt.title(title)
#     plt.grid(True, alpha=0.3)
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# data/FMAP-Data.csv
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "FMAP-Data.csv")
# data/EFPG_file.txt
txt_path = os.path.join(os.path.dirname(__file__), "..", "data", "EFPG_file.txt")

food_values = pd.read_csv(csv_path)
# Given EFPG_file.txt is a text file, treat tabs as delimiters
food_keys = pd.read_csv(txt_path, sep='\t+', engine='python')

# Merge the two dataframes on the 'EFPG_code' column
merged_df = pd.merge(food_values, food_keys, on='EFPG_code', how='left')

# Clean up dataframe for easier readability
merged_df = merged_df.drop('Metroregion_code', axis=1)
merged_df = merged_df.drop('Tier 1 group', axis=1)
merged_df = merged_df[merged_df['Attribute'] == 'Unit_value_mean_wtd']

# Crunch data based on macronutrients
carbs_df = aggregate_data_by_macro(CARBS, merged_df)
protein_df = aggregate_data_by_macro(PROTEIN, merged_df)
fats_df = aggregate_data_by_macro(FATS, merged_df)

# Convert 'Value' column from average price per 100 grams to average price per 1000 calories
carbs_df['Value'] = (carbs_df['Value'] / (AVG_CARB_CAL)) * 10
protein_df['Value'] = (protein_df['Value'] / (AVG_PROTEIN_CAL)) * 10
fats_df['Value'] = (fats_df['Value'] / (AVG_FATS_CAL)) * 10

# Plot the aggregated data of all three macronutrients separately
# plot_data(carbs_df.copy(), title="Average Price per 1000 Calories of Carbohydrates Over Time")
# plot_data(protein_df.copy(), title="Average Price per 1000 Calories of Proteins Over Time")
# plot_data(fats_df.copy(), title="Average Price per 1000 Calories of Fats Over Time")

# Readjust the 'Date' column on all three dataframes; otherwise there'll be an error
carbs_df['Date'] = pd.to_datetime(carbs_df[['Year', 'Month']].assign(DAY=1))
protein_df['Date'] = pd.to_datetime(protein_df[['Year', 'Month']].assign(DAY=1))
fats_df['Date'] = pd.to_datetime(fats_df[['Year', 'Month']].assign(DAY=1))

# Plot all three macronutrients together
plt.figure(figsize=(12, 6))
plt.plot(carbs_df['Date'], carbs_df['Value'], marker='o', linewidth=2, markersize=4, label='Carbohydrates')
plt.plot(protein_df['Date'], protein_df['Value'], marker='o', linewidth=2, markersize=4, label='Proteins')
plt.plot(fats_df['Date'], fats_df['Value'], marker='o', linewidth=2, markersize=4, label='Fats')
plt.xlabel('Date')
plt.ylabel('Average Price per 1000 Calories ($)')
plt.title("Average Price per 1000 Calories of Macronutrients Over Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()