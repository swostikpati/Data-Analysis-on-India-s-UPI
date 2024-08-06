# Author: Swostik Pati

import pandas as pd
import matplotlib.pyplot as plt

# File paths
transactions_file_path = './Data/TransactionsData/MonthlyProductStatistics_flattened.csv'
gdp_file_path = './Data/GDP_data/GDPIndia.csv'  
financial_inclusion_file_path = './Data/FinancialInclusionData/financialInclusionIndia.csv'  

# Loading and cleaning NPCI transactions data
transactions_df = pd.read_csv(transactions_file_path)
transactions_df['Year'] = transactions_df['Year'] + 2000
transactions_df['Volume'] = pd.to_numeric(transactions_df['Volume'], errors='coerce')
transactions_df['Value'] = pd.to_numeric(transactions_df['Value'], errors='coerce')

# Preparing data for combined transaction volume and value charts
monthly_volume = transactions_df.pivot_table(values='Volume', index='Month', columns='Year', aggfunc='sum')
monthly_value = transactions_df.pivot_table(values='Value', index='Month', columns='Year', aggfunc='sum')

# Sorting the data based on typical calendar months
sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_volume = monthly_volume.reindex(sort_order)
monthly_value = monthly_value.reindex(sort_order)

# Combined Transaction Volume Chart (2021-2023)
plt.figure(figsize=(10, 6))
monthly_volume.plot(kind='line', marker='o')
plt.title('Combined Transaction Volume (2021-2023)')
plt.xlabel('Months')
plt.ylabel('Total Volume (in millions)')
plt.legend(title='Year')
plt.grid(True)
plt.show()

# Combined Transaction Value Chart (2021-2023)
plt.figure(figsize=(10, 6))
monthly_value.plot(kind='line', marker='o')
plt.title('Combined Transaction Value (2021-2023)')
plt.xlabel('Months')
plt.ylabel('Total Value (in millions)')
plt.legend(title='Year')
plt.grid(True)
plt.show()

# Loading and cleaning GDP data
gdp_df = pd.read_csv(gdp_file_path)
gdp_long_df = pd.melt(gdp_df, id_vars=['Country Name', 'Country Code'], var_name='Year', value_name='GDP')
gdp_long_df['Year'] = pd.to_numeric(gdp_long_df['Year'].str.extract('(\d+)')[0], errors='coerce')
gdp_long_df.dropna(subset=['Year'], inplace=True)
gdp_long_df['Year'] = gdp_long_df['Year'].astype(int)

# GDP Growth Trend Analysis
gdp_long_df[gdp_long_df['Country Name'] == 'India'].plot(x='Year', y='GDP', kind='line', marker='o', color='purple')
plt.title('GDP Growth Trend in India (2016-2022)')
plt.xlabel('Year')
plt.ylabel('GDP (current US$)')
plt.grid(True)
plt.show()

# Loading and cleaning Financial Inclusion data
financial_inclusion_df = pd.read_csv(financial_inclusion_file_path)
financial_inclusion_df.columns = ['Country Name', 'Country Code', 'Indicator', 'Series Code', '2017', '2021']
financial_inclusion_df.dropna(subset=['2017', '2021'], inplace=True)
financial_inclusion_df['2017'] = pd.to_numeric(financial_inclusion_df['2017'], errors='coerce')
financial_inclusion_df['2021'] = pd.to_numeric(financial_inclusion_df['2021'], errors='coerce')
financial_inclusion_df.set_index('Indicator', inplace=True)

# Extract the common prefix to remove from the indicator labels
common_prefix = 'Used a mobile phone or the internet to buy something online'

# Update the x-axis labels to only include the unique part of each indicator
updated_labels = [label.replace(common_prefix, '').strip(', ') for label in financial_inclusion_df.index]

# Financial Inclusion Indicators Trend Analysis
plt.figure(figsize=(10, 5))  # Increased figure size for better readability

# Plotting both years with correct alignment
ind = range(len(financial_inclusion_df))
width = 0.35  # Width of the bars

fig, ax = plt.subplots(figsize=(10, 5))
rects1 = ax.bar(ind, financial_inclusion_df['2017'], width, label='2017')
rects2 = ax.bar([i + width for i in ind], financial_inclusion_df['2021'], width, label='2021')

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel("Used a mobile phone or the internet to buy something online (Indicator)")
ax.set_ylabel('Percentage')
ax.set_title('Changes in Financial Inclusion Indicators (2017 vs 2021)')
ax.set_xticks([i + width / 2 for i in ind])
ax.set_xticklabels(updated_labels, rotation=45, ha='right')

# Set y-axis to start at 0 and end at an appropriate value with more granular increments
ax.set_ylim(0, 21)  # Ensure y-axis starts at 0
# The y-ticks should be set from 0 to the upper limit of the y-axis, with increments of 1
ax.set_yticks(range(0, 21, 1))  # Set y-axis ticks every 1%

ax.legend()

plt.show()

financial_inclusion_df