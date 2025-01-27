import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
customers = pd.read_csv("Customers.csv")
products = pd.read_csv("Products.csv")
transactions = pd.read_csv("Transactions.csv")
transaction_agg = transactions.groupby('CustomerID').agg({'TotalValue': 'sum','Quantity': 'sum','ProductID': lambda x: list(x)}).reset_index()
data = customers.merge(transaction_agg, on="CustomerID", how="left")
data = pd.get_dummies(data, columns=['Region'], prefix='Region')
data['TotalValue'] = data['TotalValue'].fillna(0)
data['Quantity'] = data['Quantity'].fillna(0)
data['TotalValue_Scaled'] = data['TotalValue'] / data['TotalValue'].max()
data['Quantity_Scaled'] = data['Quantity'] / data['Quantity'].max()
features = data.drop(['CustomerID', 'CustomerName', 'SignupDate','TotalValue', 'Quantity', 'ProductID'
], axis=1)
similarity_matrix = cosine_similarity(features)
lookalike_map = {}
customer_ids = data['CustomerID'].iloc[:10].values
for idx, customer_id in enumerate(customer_ids):
    similarities = list(enumerate(similarity_matrix[idx]))
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_similar = [(data.iloc[i]['CustomerID'], score) for i, score in similarities if i != idx][:3]
    lookalike_map[customer_id] = top_similar
lookalike_df = pd.DataFrame([{"CustomerID": cust_id, "Lookalikes": str(lookalikes)}for cust_id, lookalikes in lookalike_map.items()])
lookalike_df.to_csv("Lookalike.csv", index=False)
print("Lookalike.csv has been created:")
print(lookalike_df.head())