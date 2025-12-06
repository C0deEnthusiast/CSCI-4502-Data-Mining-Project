#generate interesting and surprisingly plots that may not be the most immediately obviously extractable from the data
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
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
        '1002': 'Fat',
        '1090': 'Fiber',
        '1091': 'Calcium',
        '1087': 'Calcium',
        '1095': 'Iron',
        '1089': 'Iron',
        '1092': 'Potassium',
        '1007': 'Ash',
        '1079': 'Fiber, total dietary'
    }
    if nutrient_id is None:
        return str(nutrient_id)
    return nutrient_map.get(str(int(nutrient_id)) if pd.notna(nutrient_id) else str(nutrient_id), str(nutrient_id))
def plot_nutrient_by_categories(nutrient_id):
    """Plot average nutrient amount by food category."""
    # Merge food and nutrient data
    merged_df = pd.merge(nutrients_df, food_df[['id', 'food_category_id']], left_on='food_id', right_on='id', how='left')
    merged_df['nutrient_id_num'] = pd.to_numeric(merged_df['nutrient_id'], errors='coerce')
    nutrient_data = merged_df[merged_df['nutrient_id_num'] == int(nutrient_id)]
    
    # Group by category and calculate average amount
    category_avg = nutrient_data.groupby('food_category_id')['amount'].mean().dropna()
    
    # Get top 10 categories by average amount
    top_categories = category_avg.sort_values(ascending=False).head(10)
    
    # Plotting
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
def plot_nutrient_correlations(nutrient_ids=None):
    """Plot correlation matrix between different nutrients."""
    if nutrient_ids is None:
        nutrient_ids = [1003, 1004, 1005, 1008, 1093, 1051]  # Protein, Fat, Carbs, Energy, Sodium, Water
    
    # Pivot the data to get nutrients as columns
    pivot_df = pd.pivot_table(
        nutrients_df,
        values='amount',
        index='fdc_id',
        columns='nutrient_id',
        aggfunc='first'
    )
    
    # Select only the nutrients we're interested in
    nutrients_of_interest = pivot_df[nutrient_ids]
    
    # Calculate correlation matrix
    corr_matrix = nutrients_of_interest.corr()
    
    # Create labels using nutrient names
    labels = [get_nutrient_name(nid) for nid in nutrient_ids]
    
    # Plot correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                xticklabels=labels, yticklabels=labels)
    plt.title('Nutrient Content Correlations')
    plt.tight_layout()
    plt.show()

def analyze_nutrient_density(nutrient_id, top_n=10):
    """Analyze nutrient density (amount per calorie) across food categories."""
    # Merge nutrients with foods
    merged_df = pd.merge(nutrients_df, food_df[['fdc_id', 'food_category_id']], 
                        on='fdc_id')
    
    # Get energy content (nutrient_id 1008 is energy)
    energy_df = merged_df[merged_df['nutrient_id'] == 1008].copy()
    energy_df = energy_df[['fdc_id', 'amount']].rename(columns={'amount': 'energy'})
    
    # Get target nutrient content
    nutrient_df = merged_df[merged_df['nutrient_id'] == nutrient_id].copy()
    nutrient_df = nutrient_df[['fdc_id', 'food_category_id', 'amount']]
    
    # Merge energy with nutrient
    density_df = pd.merge(nutrient_df, energy_df, on='fdc_id')
    
    # Calculate density (amount per 100 calories)
    density_df['density'] = (density_df['amount'] / density_df['energy']) * 100
    
    # Get average density by category
    cat_density = density_df.groupby('food_category_id')['density'].mean().sort_values(ascending=False)
    top_cats = cat_density.head(top_n)
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_cats)), top_cats.values)
    plt.title(f'{get_nutrient_name(nutrient_id)} Density by Food Category\n(Amount per 100 calories)')
    plt.xlabel('Food Category')
    plt.ylabel(f'{get_nutrient_name(nutrient_id)} per 100 calories')
    
    # Use category names for labels
    labels = [get_category_name(cat_id) for cat_id in top_cats.index]
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

def analyze_seasonal_patterns(nutrient_id):
    """Analyze if nutrient content shows seasonal patterns."""
    # Merge nutrients with foods to get publication dates
    merged_df = pd.merge(nutrients_df, food_df[['fdc_id', 'publication_date']], 
                        on='fdc_id')
    
    # Convert publication_date to datetime and extract month
    merged_df['publication_date'] = pd.to_datetime(merged_df['publication_date'], format='mixed')
    merged_df['month'] = merged_df['publication_date'].dt.month
    
    # Filter for specific nutrient
    nutrient_data = merged_df[merged_df['nutrient_id'] == nutrient_id].copy()
    
    # Calculate average amount by month
    monthly_avg = nutrient_data.groupby('month')['amount'].agg(['mean', 'std']).reset_index()
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.errorbar(monthly_avg['month'], monthly_avg['mean'], 
                yerr=monthly_avg['std'], capsize=5, marker='o')
    
    plt.title(f'Seasonal Pattern of {get_nutrient_name(nutrient_id)} Content')
    plt.xlabel('Month')
    plt.ylabel(f'Average {get_nutrient_name(nutrient_id)} Amount')
    
    # Use month names for x-axis
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    plt.xticks(range(1, 13), month_names, rotation=45)
    
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("1. Analyzing nutrient correlations...")
    plot_nutrient_correlations()
    
    print("\n2. Analyzing protein density across food categories...")
    analyze_nutrient_density(1003)  # Protein density
    
    print("\n3. Analyzing fat density across food categories...")
    analyze_nutrient_density(1004)  # Fat density
    
    print("\n4. Looking for seasonal patterns in protein content...")
    analyze_seasonal_patterns(1003)  # Protein seasonal patterns
    
    print("\n5. Looking for seasonal patterns in fiber content...")
    analyze_seasonal_patterns(1090)  # Fiber seasonal patterns
    
    print("\n6. Looking for seasonal patterns in calcium content...")
    analyze_seasonal_patterns(1091)  # Calcium seasonal patterns