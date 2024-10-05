import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pydeck as pdk

# Sample data
#df = pd.read_csv('/content/Fund_data_final.csv')
df = pd.read_csv('/content/merged.csv')
df = df.drop(['Unnamed: 0'],axis=1)
# List of Fund Incorporation Countries
countries = ['Luxembourg', 'UK', 'France', 'Japan', 'India']

# Add a new column with randomly assigned Fund Incorporation Country
df['Fund_Incorporation_Country'] = [random.choice(countries) for _ in range(len(df))]
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




# Step 1: Group by Fund_Incorporation_Country and sum the AUM
country_aum = df.groupby('Fund_Incorporation_Country')['AUM'].sum().reset_index()

# Step 2: Add latitude and longitude for each country (for visualization purposes)
country_coords = {
    'Japan': [36.2048, 138.2529],
    'UK': [55.3781, -3.4360],
    'France': [46.6034,	1.8883],
    'India': [120.5937,	78.9629],
    'Luxembourg': [49.6117, 6.1319]
}


# Step 3: Add latitude and longitude to the country_aum dataframe
country_aum['latitude'] = country_aum['Fund_Incorporation_Country'].apply(lambda x: country_coords[x][0])
country_aum['longitude'] = country_aum['Fund_Incorporation_Country'].apply(lambda x: country_coords[x][1])

# Streamlit App Title
st.title('Map Showing Total AUM by Fund Incorporation Country')

# Display the grouped data in the app
st.write("### Total AUM by Country")
st.dataframe(country_aum)

# Step 4: Create a PyDeck layer for the map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=country_aum,
    get_position='[longitude, latitude]',
    get_radius='[AUM/1e10]',  # Radius proportional to AUM
    get_color='[200, 30, 0, 160]',  # Red color for the dots
    pickable=True,  # Allow the user to click on the points
    tooltip={"text": "{Fund_Incorporation_Country}\nTotal AUM: {AUM}"}  # Tooltip with country and AUM
)

# Step 5: Set the initial view of the map
view_state = pdk.ViewState(
    latitude=20.0,  # Center of the map (somewhere near the middle of all points)
    longitude=0.0,
    zoom=1.5,  # Zoom out to see the global view
    pitch=50
)

# Create the PyDeck map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Fund_Incorporation_Country}\nTotal AUM: ${AUM / 1e9:.2f} Billion"}  # Display AUM in billions
)

# Render the map in Streamlit
st.pydeck_chart(r)


# Function to highlight mismatched cells
def highlight_mismatch(row):
    return ['background-color: green' if row['Fund_Name'] != row['Fund_Name_Modified'] else '' 
            for _ in row]

# Streamlit app
st.title('Fund Name Comparison')

# Display the DataFrame with highlighting
st.write("### Fund Name Mismatch Highlighting:")
styled_df = df.style.apply(highlight_mismatch, subset=['Fund_Name', 'Fund_Name_Modified'], axis=1)
st.dataframe(styled_df)

# Optional: Display mismatched rows separately
mismatched_df = df[df['Fund_Name'] != df['Fund_Name_Modified']]
if not mismatched_df.empty:
    st.write("### Mismatched Fund Names:")
    st.dataframe(mismatched_df)
else:
    st.write("### No mismatches found.")





