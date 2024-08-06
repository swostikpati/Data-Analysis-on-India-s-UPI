# Author: Swostik Pati

import pandas as pd

# File paths for the datasets
transactions_file_path = './Data/TransactionsData/MonthlyProductStatistics_flattened.csv'
gdp_file_path = './Data/GDP_data/GDPIndia.csv'  
financial_inclusion_file_path = './Data/FinancialInclusionData/financialInclusionIndia.csv'  

# Loading and cleaning NPCI transactions data
transactions_df = pd.read_csv(transactions_file_path)
transactions_df['Year'] = transactions_df['Year'] + 2000
transactions_df['Volume'] = pd.to_numeric(transactions_df['Volume'], errors='coerce')
transactions_df['Value'] = pd.to_numeric(transactions_df['Value'], errors='coerce')

# Aggregating Volume and Value by Year
yearly_transactions = transactions_df.groupby('Year').agg({'Volume': 'sum', 'Value': 'sum'}).reset_index()

# Loading GDP data
gdp_df = pd.read_csv(gdp_file_path)
gdp_long_df = pd.melt(gdp_df, id_vars=['Country Name', 'Country Code'], var_name='Year', value_name='GDP')
gdp_long_df['Year'] = pd.to_numeric(gdp_long_df['Year'].str.extract('(\d+)')[0], errors='coerce')
gdp_long_df.dropna(subset=['Year'], inplace=True)
gdp_long_df['Year'] = gdp_long_df['Year'].astype(int)

# Loading Financial Inclusion data
financial_inclusion_df = pd.read_csv(financial_inclusion_file_path)
financial_inclusion_df.columns = ['Country Name', 'Country Code', 'Indicator', 'Series Code', '2017', '2021']
financial_inclusion_long = pd.melt(financial_inclusion_df, id_vars=['Country Name', 'Country Code', 'Series Code'], 
                                   value_vars=['2017', '2021'], 
                                   var_name='Year', value_name='Financial Inclusion')
financial_inclusion_long['Year'] = pd.to_numeric(financial_inclusion_long['Year'], errors='coerce')

# Merging the yearly transactions data with GDP data
merged_with_gdp = pd.merge(yearly_transactions, gdp_long_df, on='Year', how='outer')

# Final merge with Financial Inclusion data
final_merged_df = pd.merge(merged_with_gdp, financial_inclusion_long, on='Year', how='outer')

# Filtering data for the years 2017 to 2022
final_filtered_df = final_merged_df.loc[final_merged_df['Year'].between(2017, 2022)]

# Displaying the summary table
final_filtered_df.head()

final_filtered_df.sort_values(by='Year', ascending=False, inplace=True)

final_filtered_df.drop('Country Code_x', axis=1, inplace=True)
final_filtered_df.drop('Country Code_y', axis=1, inplace=True)
final_filtered_df.drop('Country Name_x', axis=1, inplace=True)
final_filtered_df.drop('Country Name_y', axis=1, inplace=True)

# final_filtered_df.drop(final_filtered_df.index[1:6], inplace=True)


final_filtered_df.to_csv('merged_summary_table.csv', index=False)

