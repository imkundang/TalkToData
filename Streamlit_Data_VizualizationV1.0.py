import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data
df = pd.read_csv('/content/Fund_data_final.csv')
df['AUM'] = pd.to_numeric(df['AUM'], errors='coerce')
df = df.dropna(subset=['AUM'])


# Streamlit app title
st.title("Fund Dashboard")

# Display the DataFrame
st.write("### Fund Data")
st.dataframe(df)

# Metric 1: Total AUM
total_aum = df['AUM'].sum()
st.metric(label="Total AUM (USD)", value=f"${total_aum / 1e12:.2f} Trillion")

# Metric 2: Top Fund by AUM
top_fund = df.loc[df['AUM'].idxmax()]
st.write(f"### Top Fund by AUM: **{top_fund['Fund_Name']}** with AUM of **${top_fund['AUM'] / 1e9:.2f} Billion**")

# Chart 1: Distribution by Fund Category
category_count = df['Fund_Category'].value_counts()
fig1 = px.pie(df, names='Fund_Category', title='Fund Distribution by Category', values='AUM')
st.plotly_chart(fig1)

# Chart 2: Distribution by Fund Asset Type
fund_size_count = df['Fund_Size'].value_counts()
fig2 = px.bar(df, x='Fund_Size', y='AUM', color='Fund_Size', title='AUM by Fund Size')
st.plotly_chart(fig2)

# Sort by AUM in descending order
df = df.sort_values(by='AUM', ascending=False)

# Streamlit app title
st.title("Top 10 Funds by AUM")

# Slider to select the number of top funds to display
num_funds = st.slider("Select number of top funds to display", min_value=1, max_value=10, value=5)

# Display the selected number of top funds
top_funds_df = df.head(num_funds)

# Display the DataFrame of top funds
st.write(f"### Top {num_funds} Funds by AUM")
st.dataframe(top_funds_df)

# Metric 4: Show the top fund by AUM
top_fund = df.loc[df['AUM'].idxmax()]
st.metric(label="Top Fund by AUM", value=f"{top_fund['Fund_Name']}", delta=f"${top_fund['AUM'] / 1e9:.2f} Billion")

# Create a bar chart to visualize the top funds by AUM
fig = px.bar(
    top_funds_df, 
    x='Fund_Name', 
    y='AUM', 
    color='Fund_Name', 
    title=f"Top {num_funds} Funds by AUM", 
    labels={'AUM': 'Assets Under Management (USD)'},
    hover_data=['Client_Name', 'AUM']
)

# Show the bar chart
st.plotly_chart(fig)