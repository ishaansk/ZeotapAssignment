import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
customers = pd.read_csv("Customers.csv")
products = pd.read_csv("Products.csv")
transactions = pd.read_csv("Transactions.csv")
print("Customers:-\n", customers.describe())
print("Products:-\n", products.describe(include='all'))
print("Transactions:-\n", transactions.describe(include='all'))
merged_data = transactions.merge(customers, on="CustomerID").merge(products, on="ProductID")
most_selling_regions=merged_data['Region'].value_counts()
most_selling_products=merged_data.groupby('ProductName')['TotalValue'].sum().sort_values(ascending=False)
most_customers_region=customers['Region'].value_counts()
top_customers_spending = merged_data.groupby('CustomerID')['TotalValue'].sum().sort_values(ascending=False).head(10)
print('The regions with the most sales :-\n', most_selling_regions)
print('The regions with the most customers:-\n',most_customers_region)
print('The most popularly sold products :-\n', most_selling_products.head())
print('The customers that have spent the most:-\n', top_customers_spending)
most_selling_products.head(10).plot(kind='bar', title="Top 10 Most Purchased Products")
plt.ylabel("qty sold")
plt.show()
most_selling_regions.plot(kind='bar', title="Regional Sales Analysis")
plt.ylabel("total sales value")
plt.show()
product_of_interest = input("Enter your desired product : ")
product_data = merged_data[merged_data['ProductName'] == product_of_interest]
purchase_counts = product_data.groupby(['Region'])['ProductName'].count().reset_index(name='PurchaseCount')
print(f"Purchase counts for '{product_of_interest}' by region and customer:\n", purchase_counts)
plt.figure(figsize=(10,6))
sns.barplot(x='Region', y='PurchaseCount', data=purchase_counts, palette="Set2")
plt.title(f"Customer Purchases of {product_of_interest} by Region")
plt.xlabel('Region')
plt.ylabel('Number of Purchases')
plt.xticks(rotation=45)
plt.show()