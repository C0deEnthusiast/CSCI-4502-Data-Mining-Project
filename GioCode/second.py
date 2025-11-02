import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend
import matplotlib.pyplot as plt
import pandas as pd
import os

# Load the data
base_path = r"c:\Users\giova\OneDrive\Desktop\Fall 2025\Mining Data\Final Project\CSCI-4502-Data-Mining-Project"
food_df = pd.read_csv(os.path.join(base_path, 'food.csv'))
nutrients_df = pd.read_csv(os.path.join(base_path, 'food_nutrient.csv'), low_memory=False)

def get_nutrient_name(nutrient_id):
    """Return a readable nutrient name for an id."""
    nutrient_map = {
        '1003': 'Protein',
        '1004': 'Total lipid (fat)',
        '1005': 'Carbohydrate',
        '1008': 'Energy',
        '1093': 'Sodium',
        '1051': 'Water',
        '1002': 'Fat'
    }
    if nutrient_id is None:
        return str(nutrient_id)
    return nutrient_map.get(str(int(nutrient_id)) if pd.notna(nutrient_id) else str(nutrient_id), str(nutrient_id))

def plot_nutrient_distribution(nutrient_id, title=None):
    """Plot the distribution of a specific nutrient across all foods."""
    nutrients_df['nutrient_id_num'] = pd.to_numeric(nutrients_df['nutrient_id'], errors='coerce')
    nutrient_data = nutrients_df[nutrients_df['nutrient_id_num'] == int(nutrient_id)]['amount'].dropna().astype(float)
    
    plt.figure(figsize=(12, 6))
    plt.hist(nutrient_data, bins=50)
    nutrient_name = get_nutrient_name(nutrient_id)
    plt.title(title or f'Distribution of {nutrient_name} (id={nutrient_id})')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Load category mapping
def build_category_map():
    """Build a mapping from category_id to readable name."""
    cat_path = os.path.join(base_path, 'category_map.csv')
    if os.path.exists(cat_path):
        try:
            cat_df = pd.read_csv(cat_path)
            cat_df['short_name'] = cat_df['representative_description'].apply(
                lambda x: str(x).split(',')[0].split('(')[0].strip().title())
            return pd.Series(cat_df['short_name'].values, 
                           index=cat_df['food_category_id']).to_dict()
        except Exception as e:
            print(f"Warning: couldn't load category map: {e}")
    return {}

category_map = build_category_map()

def get_category_name(category_id):
    """Return a readable category name for an id."""
    if category_id is None:
        return str(category_id)
    return category_map.get(float(category_id) if pd.notna(category_id) else str(category_id), 
                          f"Category {category_id}")

def plot_nutrient_by_categories(nutrient_id, top_n_categories=8):
    """
    Plot nutrient content over time with different lines for each food category.
    Shows only the top N categories by data volume for readability.
    
    Args:
        nutrient_id: The ID of the nutrient to track
        top_n_categories: Number of food categories to show (default 8)
    """
    # Merge food and nutrient data
    merged_df = pd.merge(food_df, nutrients_df, on='fdc_id')
    
    # Convert dates and nutrient values to proper types
    merged_df['publication_date'] = pd.to_datetime(merged_df['publication_date'], format='mixed')
    merged_df['amount'] = pd.to_numeric(merged_df['amount'], errors='coerce')
    
    # Filter for specific nutrient
    nutrient_data = merged_df[merged_df['nutrient_id'] == nutrient_id].copy()
    
    # Get top N categories by number of samples
    top_categories = nutrient_data['food_category_id'].value_counts().head(top_n_categories).index
    
    # Filter for top categories
    nutrient_data = nutrient_data[nutrient_data['food_category_id'].isin(top_categories)]
    
    # Calculate average nutrient amount per publication date and category
    time_series = nutrient_data.groupby(['publication_date', 'food_category_id'])['amount'].mean().reset_index()
    
    plt.figure(figsize=(15, 8))
    
    # Plot line for each category
    for category_id in top_categories:
        cat_data = time_series[time_series['food_category_id'] == category_id]
        if not cat_data.empty:
            label = get_category_name(category_id)
            plt.plot(cat_data['publication_date'], cat_data['amount'], 
                    marker='o', linestyle='-', linewidth=2, label=label)
    
    nutrient_name = get_nutrient_name(nutrient_id)
    plt.title(f'Average {nutrient_name} Content Over Time by Food Category')
    plt.xlabel('Publication Date')
    plt.ylabel(f'Average {nutrient_name} Amount')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Plotting protein content over time by food category...")
    plot_nutrient_by_categories(1003)  # Protein
    
    print("\nPlotting fat content over time by food category...")
    plot_nutrient_by_categories(1004)  # Fat

if __name__ == "__main__":
    print("Plotting protein content over time by food category...")
    plot_nutrient_by_categories(1003)  # Protein
    
    print("\nPlotting fat content over time by food category...")
    plot_nutrient_by_categories(1004)  # Fat