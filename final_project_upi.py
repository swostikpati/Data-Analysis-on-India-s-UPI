# Author: Swostik Pati

'''My Modified Research Question
How have Unified Payments Interface (UPI) and other cashless payment methods influenced the economic growth and financial inclusion in India since their
inception?'''

import pandas as pd
import matplotlib.pyplot as plt

"""This is the first dataset I am using. It is provided by National Payments Corporation of India (NPCI), and provided the details of all the transactions that went through in the country, including several forms of Cashless mechanisms like UPI transactions. The way I was able to get the data is by:

- First visiting this website: (https://www.npci.org.in/statistics/monthly-metrics). It is a bit laggy because of the bulk of data overhead being sent from the backend to the browser. After it successfully loaded, I selected the monthly product statistics. The data was provided in the form of a table in the website. I had the option of web scraping, but before that I used Chrome Dev tools (Inspect Element) to check the source of the data in the "Networks" tab. I realized the data was being fetched from a publicly accessible json file (https://www.npci.org.in/files/npci/MonthlyProductStatistics.json) hosting all the data together which was later filtered in the browser. So instead of web scraping the data from several years, I just downloaded the json file directly. But I remembered from class the complexities of working with json files so I first decided it to convert and save it in the form of a csv file.

I changed the data into the form of tables in a csv file by using the keys of the json file as the table headings. The reason for using this data is because it gives be the ability to make time-series analysis (especially plots) both by volume and value of the cashless transactions (especially highlighting UPI transactions) between the years of 21-23 (for the timing I was only able to find the data for these specific years, but I hope to get the data of other years as well if possible).
"""
# Setting the path to the JSON file
json_file_path = './Data/TransactionsData/MonthlyProductStatistics.json'  

# Reading the JSON file into a DataFrame
json_df = pd.read_json(json_file_path)

# Flattening the nested data in the 'data' column for better analysis
flattened_df = pd.json_normalize(json_df['data'])

# Defining the path for the output CSV file
flattened_csv_file_path = json_file_path.replace('.json', '_flattened.csv')

# Saving the flattened DataFrame as a CSV file for further analysis
flattened_df.to_csv(flattened_csv_file_path, index=False)

# Displaying the first five rows to check the structure
print(flattened_df.head())



"""
Conducting the required checks. 

The distribution by value and by volume both seem to show an expected trend, the bulk of transactions all concentrated together with few ones spread across. With regards to distribution by MonthID, the transactions across the different months across several years seem to be quite uniform, with a trend in rise of transactions towards the end of the financial year (the period from December till February) and a steep drop thereafter. The distribution by year shows the increase in number of transactions from 2021 to 2022 and the current year already very close to the closing number of 2022, which forcasts a definitive growth by the end of the year(especially since the bulk of transactions will be coming now based on past trends by month as discussed above.)

For the timing, there aren't any missing values that were found in the dataset, but I will conduct manual checks to ensure that is the case. In future, if I add more data from other datasets, my method to deal with missing values will be to drop them. 

There are a few outliers that exist by value and by volume, but since the data is directly provided by the nationalized government agency regulating all the transactions, I will chose not to drop this data as the numbers look quite plausible.
"""
# Loading up the newly created CSV Files
csv_file_path = './Data/TransactionsData/MonthlyProductStatistics_flattened.csv'

# Reading the CSV file into a DataFrame
transactions_df = pd.read_csv(csv_file_path)

# Converting numerical columns to numeric data type
# Removing commas and converting to float - to prevent multiplication error later
transactions_df['Volume'] = transactions_df['Volume'].replace(',', '', regex=True).astype(float)
transactions_df['Value'] = transactions_df['Value'].replace(',', '', regex=True).astype(float)

# 1. Distributions
# Exploring variable distributions for both categorical and numerical variables

# Categorical variables: 'Product', 'Month', 'NoOfBankslive'
categorical_columns = ['Product', 'Month', 'NoOfBankslive']
for col in categorical_columns:
    print(f"Value counts for {col}:")
    print(transactions_df[col].value_counts())
    print("\n")

# Numerical variables: 'Volume', 'Value', 'MonthId', 'Year'
numerical_columns = ['Volume', 'Value', 'MonthId', 'Year']
for col in numerical_columns:
    print(f"Histogram for {col}:")
    transactions_df[col].hist()
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()

# 2. Missing or Ridiculous Values
# Checking for missing values and identifying any ridiculous values
print("Missing values in each column:")
print(transactions_df.isnull().sum())
print("\n")

# Add any specific checks for ridiculous values here if needed

# 3. Outliers
# Checking for outliers using the IQR method
for col in numerical_columns:
    Q1 = transactions_df[col].quantile(0.25)
    Q3 = transactions_df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = transactions_df[((transactions_df[col] < (Q1 - 1.5 * IQR)) | (transactions_df[col] > (Q3 + 1.5 * IQR)))]
    print(f"Outliers in {col}:")
    print(outliers)
    print("\n")