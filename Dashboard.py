import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    
    # Drop rows with NaT in order_date
    df.dropna(subset=['order_date'], inplace=True)
    
    # Group by order_date and count unique orders
    daily_orders_df = df.groupby(df['order_date'].dt.to_period('D')).agg({
        "order_id": "nunique"
    }).reset_index()
    
    # Convert period to timestamp for plotting
    daily_orders_df['order_date'] = daily_orders_df['order_date'].dt.to_timestamp()
    
    # Rename columns
    daily_orders_df.rename(columns={
        "order_date": "date",
        "order_id": "order_count"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_category_items_df(df):
    sum_category_items_df = df.groupby("product_category_name").product_id.nunique().reset_index()
    sum_category_items_df.rename(columns={
        "product_id": "product_count"
    }, inplace=True)
    sum_category_items_df = sum_category_items_df.sort_values(by="product_count", ascending=False)
    return sum_category_items_df

def create_customercity_df(df):
    customercity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    customercity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    customercity_df = customercity_df.sort_values(by="customer_count", ascending=False)
    return customercity_df

def create_sellercity_df(df):
    sellercity_df = df.groupby(by="seller_city").seller_id.nunique().reset_index()
    sellercity_df.rename(columns={
        "seller_id": "seller_count"
    }, inplace=True)
    sellercity_df = sellercity_df.sort_values(by="seller_count", ascending=False)
    return sellercity_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_date"]
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(drop=True, inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column], errors='coerce')

min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()
 
with st.sidebar:
    st.image("https://github.com/payy79/Dicoding/raw/main/bangkit.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_date"] >= str(start_date)) & 
                (all_df["order_date"] <= str(end_date))]

filtered_df = all_df[(all_df['order_date'] >= pd.to_datetime(start_date)) & (all_df['order_date'] <= pd.to_datetime(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_category_items_df = create_sum_category_items_df(main_df)
customercity_df = create_customercity_df(main_df)
sellercity_df = create_sellercity_df(main_df)

st.header('Bangkit E-Commerce Dashboard :sparkles:')

st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["date"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Product Categories with the Most and Least Demand Based on Number of Orders")

# Getting the top 5 and bottom 5 categories
top_5_categories = sum_category_items_df.head(5)
bottom_5_categories = sum_category_items_df.tail(5)

# Creating bar charts
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 12))

colors = ["#72BCD4"] + ["#D3D3D3"] * 4

# Bar chart for top 5 categories
sns.barplot(x="product_count", y="product_category_name", data=top_5_categories, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Top 5 Most In-Demand Product Categories", loc="center", fontsize=25)
ax[0].tick_params(axis='y', labelsize=12)


# Bar chart for bottom 5 categories
sns.barplot(x="product_count", y="product_category_name", data=bottom_5_categories, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Top 5 Least In-Demand Product Categories", loc="center", fontsize=25)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.subheader("Top 10 Cities with the Most Buyers")

top_10_customer_cities = customercity_df.head(10)

fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4"] + ["#D3D3D3"] * (len(top_10_customer_cities) - 1)
sns.barplot(
    x="customer_count",
    y="customer_city",
    data=top_10_customer_cities,
    palette=colors_,
    hue="customer_city",
    dodge=False,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
ax.legend().remove()

st.pyplot(fig)

st.subheader("Top 10 Cities with the Most Sellers")

top_10_seller_cities = sellercity_df.head(10)

fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4"] + ["#D3D3D3"] * (len(top_10_seller_cities) - 1)
sns.barplot(
    x="seller_count",
    y="seller_city",
    data=top_10_seller_cities,
    palette=colors_,
    hue="seller_city",
    dodge=False,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
ax.legend().remove()

st.pyplot(fig)

