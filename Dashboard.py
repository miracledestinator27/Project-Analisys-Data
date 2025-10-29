import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
sns.set(style='dark')

# Membuat class DataAnalyzer untuk analisis data
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

# Membuat fungsi produk paling banyak dibeli
    def get_top_categories(self, n=10):
        category_counts = self.df['product_category_name'].value_counts().reset_index()
        category_counts.columns = ['product_category_name', 'total_orders']
        return category_counts.head(n)
# Membuat fungsi total seller terbanyak
    def get_state_sellers_counts(self):
        state_sellers_counts = self.df.groupby("customer_state")["order_id"].count().reset_index()
        state_sellers_counts.columns = ["customer_state", "total_orders"]
        return state_sellers_counts

# fungsi untuk membuat metric harian
def create_daily_metrics_df(orders_df):
    datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
    for column in datetime_columns: 
        orders_df[column] = pd.to_datetime(orders_df[column])
    daily_df = orders_df.resample(rule='D', on='order_purchase_timestamp').agg({
        'order_id': 'nunique',  # Unique orders
        'order_status': 'count'  # Total orders
    }).reset_index()
    daily_df.rename(columns={'order_id': 'order_count', 'order_status': 'total_orders'}, inplace=True)
    return daily_df

# membuat dataframe metric harian
print ("ORDERS TABLE")
orders_df = pd.read_csv("orders_dataset.csv")
orders_df.head()
daily_metrics_df = create_daily_metrics_df(orders_df)


# sidebar untuk input tanggal
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Date Range',
        value=(daily_metrics_df['order_purchase_timestamp'].min().date(), 
            daily_metrics_df['order_purchase_timestamp'].max().date())
    )

# menggonversi input tanggal ke datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan data input
main_df = daily_metrics_df[(daily_metrics_df['order_purchase_timestamp'] >= start_date) & 
                            (daily_metrics_df['order_purchase_timestamp'] <= end_date)]

# Streamlit header
st.header('E-commerce Dashboard')

# Visualisasi 10 Kota teratas
plt.figure(figsize=(10, 6))
sns.barplot(x=seller_city_counts.head(10).index, y=seller_city_counts.head(10).values, palette='viridis')
plt.title('Top 10 Kota dengan Penjual Terbanyak')
plt.xlabel('Kota')
plt.ylabel('Jumlah Penjual')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Visualize 10 product teratas yang paling sering dibeli
plt.figure(figsize=(10, 6))
sns.barplot(x=products_category_counts.head(10).index, y=products_category_counts.head(10).values, palette='viridis')
plt.title('Top 10 Kategori Produk Terbanyak')
plt.xlabel('Kategori Produk')
plt.ylabel('Jumlah Produk')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()







