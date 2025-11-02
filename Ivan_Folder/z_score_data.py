# read from graphed_beef_average_price.csv and plot the data using matplotlib
import pandas as pd
import matplotlib.pyplot as plt 
# Read the CSV file
beef_data = pd.read_csv('ground_beef_average_price_per_pound.csv')
sirloin_data = pd.read_csv('sirloin_steak_avg.csv')
round_data = pd.read_csv('round_steak_avg.csv') 
ham_data = pd.read_csv('ham_avg.csv')
bacon_data = pd.read_csv('bacon_avg.csv')
chicken_data = pd.read_csv('chicken_avg.csv')
flour_data = pd.read_csv('flour_avg.csv')

def normalize(series):
    return (series - series.mean()) / series.std()

beef_data['Normalized'] = normalize(beef_data['Yearly_Average'])
sirloin_data['Normalized'] = normalize(sirloin_data['Yearly_Average'])
round_data['Normalized'] = normalize(round_data['Yearly_Average'])
ham_data['Normalized'] = normalize(ham_data['Yearly_Average'])
bacon_data['Normalized'] = normalize(bacon_data['Yearly_Average'])
chicken_data['Normalized'] = normalize(chicken_data['Yearly_Average'])
flour_data['Normalized'] = normalize(flour_data['Yearly_Average'])


# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(beef_data['Year'], beef_data['Normalized'], marker='o')
plt.plot(sirloin_data['Year'], sirloin_data['Normalized'], marker='o')
plt.plot(round_data['Year'], round_data['Normalized'], marker='o')
plt.plot(ham_data['Year'], ham_data['Normalized'], marker='o')
plt.plot(bacon_data['Year'], bacon_data['Normalized'], marker='o')
plt.plot(chicken_data['Year'], chicken_data['Normalized'], marker='o')
plt.plot(flour_data['Year'], flour_data['Normalized'], marker='o')

plt.legend([
    'Ground Beef', 
    'Sirloin Steak', 
    'Round Steak', 
    'Ham', 
    'Bacon', 
    'Chicken', 
    'Flour'
])

plt.title('Normalized Average Food Prices Over Time Since 2015')
plt.xlabel('Year')
plt.ylabel('Normalized Price (0–1)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()



