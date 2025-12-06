import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend
import matplotlib.pyplot as plt
import pandas as pd
import os

# Load the data
base_path = r"c:\Users\giova\OneDrive\Desktop\Fall 2025\Mining Data\Final Project\CSCI-4502-Data-Mining-Project"
food_df = pd.read_csv(os.path.join(base_path, 'food.csv'))
# read with low_memory=False to avoid mixed-type warnings and coerce nutrient_id to numeric
nutrients_df = pd.read_csv(os.path.join(base_path, 'food_nutrient.csv'), low_memory=False)

# Try to load an explicit nutrient mapping file if present
nutrient_map = {}
nutrient_csv_path = os.path.join(base_path, 'nutrient.csv')
if os.path.exists(nutrient_csv_path):
    try:
        nut_df = pd.read_csv(nutrient_csv_path)
        # Common column names: 'id' and 'name' or 'nutrient_id' and 'name'
        if 'id' in nut_df.columns and 'name' in nut_df.columns:
            nutrient_map = pd.Series(nut_df['name'].values, index=nut_df['id'].astype(str)).to_dict()
        elif 'nutrient_id' in nut_df.columns and 'name' in nut_df.columns:
            nutrient_map = pd.Series(nut_df['name'].values, index=nut_df['nutrient_id'].astype(str)).to_dict()
    except Exception:
        nutrient_map = {}

# Fallback mapping for commonly-used nutrient IDs if nutrient.csv is not available
if not nutrient_map:
    nutrient_map = {
        '1003': 'Protein',
        '1004': 'Total lipid (fat)',
        '1005': 'Carbohydrate, by difference',
        '1008': 'Energy',
        '1093': 'Sodium, Na',
        '1051': 'Water',
        '1002': 'Total lipid (fat) (duplicate id?)',
        # add more mappings as needed
    }

def get_nutrient_name(nutrient_id):
    """Return a readable nutrient name for an id (int or str)."""
    if nutrient_id is None:
        return str(nutrient_id)
    return nutrient_map.get(str(int(nutrient_id)) if pd.notna(nutrient_id) else str(nutrient_id), str(nutrient_id))

def build_category_map():
    """Build a mapping from category_id to readable name."""
    cat_path = os.path.join(base_path, 'category_map.csv')
    if os.path.exists(cat_path):
        try:
            cat_df = pd.read_csv(cat_path)
            # Clean up descriptions - take first part before comma/parentheses for brevity
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

def plot_nutrient_distribution(nutrient_id, title=None):
    """Plot the distribution of a specific nutrient across all foods"""
    plt.figure(figsize=(12, 6))
    # ensure nutrient_id column is numeric for comparisons
    nutrients_df['nutrient_id_num'] = pd.to_numeric(nutrients_df['nutrient_id'], errors='coerce')
    nutrient_data = nutrients_df[nutrients_df['nutrient_id_num'] == int(nutrient_id)]['amount'].dropna().astype(float)
    plt.hist(nutrient_data, bins=50)
    nutrient_name = get_nutrient_name(nutrient_id)
    plt.title(title or f'Distribution of {nutrient_name} (id={nutrient_id})')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_nutrient_by_category(nutrient_id, top_n=10):
    """Plot average nutrient content by food category"""
    # ensure nutrient_id column is numeric for comparisons
    nutrients_df['nutrient_id_num'] = pd.to_numeric(nutrients_df['nutrient_id'], errors='coerce')
    subset = nutrients_df[nutrients_df['nutrient_id_num'] == int(nutrient_id)].copy()
    # Merge food and nutrient data
    merged_df = pd.merge(food_df, subset, on='fdc_id', how='inner')
    # Calculate mean nutrient amount by category
    # coerce amount to numeric, drop missing
    merged_df['amount_num'] = pd.to_numeric(merged_df['amount'], errors='coerce')
    category_means = merged_df.groupby('food_category_id')['amount_num'].mean().sort_values(ascending=False)
    top_categories = category_means.head(top_n)

    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_categories)), top_categories.values)
    nutrient_name = get_nutrient_name(nutrient_id)
    plt.title(f'Average {nutrient_name} Amount by Food Category')
    plt.xlabel('Food Category')
    plt.ylabel('Average Amount')
    labels = [get_category_name(cat_id) for cat_id in top_categories.index]
    plt.xticks(range(len(top_categories)), labels, rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def build_food_map():
    """Build a mapping from fdc_id to a readable food description."""
    # Prefer the 'description' column; fall back to stringified id
    if 'fdc_id' in food_df.columns and 'description' in food_df.columns:
        return pd.Series(food_df['description'].values, index=food_df['fdc_id']).to_dict()
    return {}


food_map = build_food_map()

def get_food_name(fdc_id, max_len=60):
    """Return a human-readable name for a food fdc_id. Truncate to max_len."""
    if pd.isna(fdc_id):
        return str(fdc_id)
    name = food_map.get(int(fdc_id)) if int(fdc_id) in food_map else food_map.get(str(int(fdc_id)), None)
    if not name:
        # try to look up in dataframe directly in case of type mismatch
        row = food_df[food_df['fdc_id'] == int(fdc_id)]
        if not row.empty and 'description' in row.columns:
            name = row.iloc[0]['description']
    if not name:
        name = str(int(fdc_id))
    # truncate long names for plotting
    name = str(name)
    return name if len(name) <= max_len else name[:max_len-3] + '...'


def plot_top_foods_for_nutrient(nutrient_id, top_n=10):
    """Plot the top N foods with the highest average amount of a given nutrient.

    Bars are labeled with readable food descriptions instead of numeric fdc_id.
    """
    nutrients_df['nutrient_id_num'] = pd.to_numeric(nutrients_df['nutrient_id'], errors='coerce')
    subset = nutrients_df[nutrients_df['nutrient_id_num'] == int(nutrient_id)].copy()
    subset['amount_num'] = pd.to_numeric(subset['amount'], errors='coerce')
    # Average by food (fdc_id)
    food_means = subset.groupby('fdc_id')['amount_num'].mean().dropna().sort_values(ascending=False)
    top_foods = food_means.head(top_n)

    labels = [get_food_name(fid) for fid in top_foods.index]

    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_foods)), top_foods.values)
    nutrient_name = get_nutrient_name(nutrient_id)
    plt.title(f'Top {top_n} Foods by Average {nutrient_name}')
    plt.xlabel('Food')
    plt.ylabel('Average Amount')
    plt.xticks(range(len(top_foods)), labels, rotation=45, ha='right')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Plot distribution of protein (nutrient_id = 1003)
    plot_nutrient_distribution(1003, "Distribution of Protein Content")
    
    # Plot distribution of fat (nutrient_id = 1004)
    plot_nutrient_distribution(1004, "Distribution of Fat Content")
    
    # Plot average protein content by food category
    plot_nutrient_by_category(1003)
    
    # Plot average fat content by food category
    plot_nutrient_by_category(1004)