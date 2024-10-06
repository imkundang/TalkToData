import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pydeck as pdk
import plotly.express as px


# Sample data
#df = pd.read_csv('/content/Fund_data_final.csv')
df = pd.read_csv('/content/merged.csv')
df = df.drop(['Unnamed: 0'],axis=1)
# List of Fund Incorporation Countries
countries = ['Luxembourg', 'UK', 'France', 'Japan', 'India']
df['AUM'] = pd.to_numeric(df['AUM'], errors='coerce')

def Completeness_Check(data):
    total=(data.isnull().sum()).sort_values(ascending=False)
    percentage=((data.isnull().sum())/(data.isnull().count())*100).sort_values(ascending=False)
    datatype=data.dtypes
    ms=pd.concat([total,percentage,datatype],axis=1,keys=['Total','Percentage','Datatype'])
    #ms=ms[ms['Percentage']>0]
    return ms

#

# List of Fund Incorporation Countries
countries = ['Luxembourg', 'UK', 'France', 'Japan', 'India']
df['Fund_Incorporation_Country'] = [random.choice(countries) for _ in range(len(df))]

# Function to process user queries
def process_query(query):
    if 'describe dataframe' in query.lower():
        st.write("### DataFrame Description")
        st.write(df.describe())
    elif 'columns list' in query.lower():

        st.write("### List of Columns")
        st.write(df.columns.tolist())
    elif 'data quality check' in query.lower():
        st.write('### Data Quality Completeness Issue')
        st.write(Completeness_Check(df))

    elif 'shape of dataframe' in query.lower():
        st.write("### DataFrame Structure")
        st.write(df.shape)
    elif 'information of dataframe' in query.lower():
        st.write("### DataFrame Information")
        st.write(df.info)
    else:
        st.write("I couldn't understand the query. Please try: 'describe dataframe', 'columns list','data quality check' or 'shape of dataframe'.")

# Streamlit app title
st.title("Fund Data Query Tool")

# Display the DataFrame
st.write("### Fund Data")
st.dataframe(df)

# User query input in plain English
user_query = st.text_input("Enter your query (e.g., 'information of dataframe', 'describe dataframe', 'list columns', or 'explain dataframe'): ")

# Process user query and show results
if user_query:
    process_query(user_query)


# Plotting Section
st.write("## Histogram Plot")

# User selects a column for plotting
column_to_plot = st.selectbox("Select a column to plot a histogram:", df.columns)

# Generate histogram for the selected column
if column_to_plot:
    if df[column_to_plot].dtype == 'object':
        st.write(f"### Frequency of unique values in '{column_to_plot}'")
        fig = px.histogram(df, x=column_to_plot, title=f"Histogram of {column_to_plot}")
        st.plotly_chart(fig)
    else:
        st.write(f"### Distribution of values in '{column_to_plot}'")
        fig = px.histogram(df, x=column_to_plot, title=f"Histogram of {column_to_plot}")
        st.plotly_chart(fig)




# Section for displaying statistics (min, max, mean, std)
st.write("## Column Statistics")
# Ensure numeric columns are in the correct data types
# User selects a numeric column for statistics
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
selected_column = st.selectbox("Select a column to view statistics:", numeric_columns)

# Calculate and display statistics
if selected_column:
    col_max = df[selected_column].max()
    col_min = df[selected_column].min()
    col_mean = df[selected_column].mean()
    col_std = df[selected_column].std()
    
    st.write(f"### Statistics for '{selected_column}':")
    st.write(f"**Max**: {col_max}")
    st.write(f"**Min**: {col_min}")
    st.write(f"**Mean**: {col_mean}")
    st.write(f"**Standard Deviation**: {col_std}")




# Streamlit App Title
st.title('Column Comparison for Reconciliation')

# Show the DataFrame
st.write("### Fund Data:")
st.dataframe(df)

# User selects two columns to compare
col1 = st.selectbox("Select first column to compare:", df.columns)
col2 = st.selectbox("Select second column to compare:", df.columns)

# Compare the two selected columns and highlight mismatches
if col1 and col2:
    # Function to highlight mismatches for each row
    def highlight_mismatch(row):
        # Compare the two columns in the row
        return ['background-color: green' if row[col1] != row[col2] else '' for _ in row]

    # Apply the highlighting function across rows
    styled_df = df.style.apply(highlight_mismatch, axis=1)

    # Display the DataFrame with highlighted mismatches
    st.write("### Highlighted Mismatches between selected columns:")
    st.dataframe(styled_df)

    # Show only rows where the two columns don't match
    mismatched_df = df[df[col1] != df[col2]]

    # Display mismatches
    st.write(f"### Mismatches between '{col1}' and '{col2}':")
    
    if mismatched_df.empty:
        st.write("No mismatches found.")
    else:
        st.dataframe(mismatched_df)




# Latitude and Longitude for each country
country_coords = {
    'Luxembourg': [49.6117, 6.1319],
    'UK': [55.3781, -3.4360],
    'France': [46.6034, 1.8883],
    'Japan': [36.2048, 138.2529],
    'India': [20.5937, 78.9629]
}

# Step 1: Group by Fund_Incorporation_Country and sum the AUM
country_aum = df.groupby('Fund_Incorporation_Country')['AUM'].sum().reset_index()

# Step 2: Add latitude and longitude for each country (for visualization purposes)
country_coords = {
    'Luxembourg': [49.6117, 6.1319],
    'UK': [55.3781, -3.4360],
    'France': [46.6034, 1.8883],
    'Japan': [36.2048, 138.2529],
    'India': [20.5937, 78.9629]
}

# Add latitude and longitude to the country_aum dataframe
country_aum['latitude'] = country_aum['Fund_Incorporation_Country'].apply(lambda x: country_coords[x][0])
country_aum['longitude'] = country_aum['Fund_Incorporation_Country'].apply(lambda x: country_coords[x][1])

# Step 3: Determine max and min AUM
max_aum = country_aum['AUM'].max()
min_aum = country_aum['AUM'].min()

# Assign colors based on the AUM (highlighting max and min)
def get_color(aum):
    if aum == max_aum:
        return [255, 0, 0]  # Red for max AUM
    elif aum == min_aum:
        return [0, 255, 0]  # Green for min AUM
    else:
        return [30, 144, 255]  # Blue for others

country_aum['color'] = country_aum['AUM'].apply(get_color)

# Streamlit App Title
st.title("Geospatial Visualization of AUM by Fund Incorporation Country")

# Display the grouped data in the app
st.write("### Total AUM by Country")
st.dataframe(country_aum)

# Step 4: Create a PyDeck layer for the map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=country_aum,
    get_position='[longitude, latitude]',
    get_radius='[AUM / 1e9]',  # Radius proportional to AUM (scaled in billions)
    get_fill_color='color',  # Color based on the AUM values (max, min, and others)
    pickable=True,  # Allow the user to click on the points
    get_line_color=[255, 255, 255],  # White outline for all points
    get_line_width=50,
)

# Step 5: Set the initial view of the map
view_state = pdk.ViewState(
    latitude=20.0,  # Center of the map
    longitude=0.0,
    zoom=1.5,  # Zoom out to see the global view
    pitch=50
)

# Step 6: Create a tooltip to display AUM on hover
tooltip = {
    "html": "<b>{Fund_Incorporation_Country}</b><br/>Total AUM: ${AUM / 1e9:.2f} Billion",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

# Step 7: Create the PyDeck map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

# Render the map in Streamlit
st.pydeck_chart(r)




# Streamlit app title
st.title("Top 10 Funds by AUM")

# Sort the DataFrame by AUM in descending order
df = df.sort_values(by='AUM', ascending=False)

# Slider to select the number of top funds to display
num_funds = st.slider("Select number of top funds to display", min_value=1, max_value=10, value=5)

# Display the selected number of top funds
top_funds_df = df.head(num_funds)

# Display the DataFrame of top funds
st.write(f"### Top {num_funds} Funds by AUM")
st.dataframe(top_funds_df)

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


