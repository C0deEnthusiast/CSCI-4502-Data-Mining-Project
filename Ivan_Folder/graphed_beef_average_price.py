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


# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(beef_data['Year'], beef_data['Yearly_Average'], marker='o')
plt.plot(sirloin_data['Year'], sirloin_data['Yearly_Average'], marker='o')
plt.plot(round_data['Year'], round_data['Yearly_Average'], marker='o')
plt.plot(ham_data['Year'], ham_data['Yearly_Average'], marker='o')
plt.plot(bacon_data['Year'], bacon_data['Yearly_Average'], marker='o')
plt.plot(chicken_data['Year'], chicken_data['Yearly_Average'], marker='o')
plt.plot(flour_data['Year'], flour_data['Yearly_Average'], marker='o')

plt.legend(['Ground Beef Average Price', 
            'Sirloin Steak Average Price', 
            'Round Steak Average Price', 
            'Ham Average Price', 'Bacon Average Price', 
            'Chicken Average Price', 
            'Flour Average Price'])

plt.title('Average Food Prices Over Time Since 2015')
plt.xlabel('Date')
plt.ylabel('Average Price ($)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
# Show the plot
plt.show()



