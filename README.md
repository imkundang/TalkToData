# Interactive User Interface for Data Visualization with Streamlit

## Project Overview

This project is a **Streamlit** web application that visualizes the **Top 10 Funds** by **AUM (Assets Under Management)**. 
Users can dynamically select how many of the top funds they want to display, and the app presents the data in an interactive table and bar chart format. 
Additionally, the fund with the highest AUM is highlighted with a metric card.

## Features

- **Slider-Based Filtering**: Users can use a slider to display between 1 and 10 of the top funds.
- **Interactive Bar Chart**: A bar chart visualizing the selected funds based on their AUM.
- **Metric Display**: Highlights the fund with the highest AUM.
- **Responsive Design**: The app is built using Streamlit, making it fast, interactive, and easy to use.

## Installation

### Prerequisites

Make sure you have the following installed on your local machine:

- Google Colab account
- Account on GCP to make Colab BigQuery connection to read tables

### Steps to Install

1. Clone this repository:
   git clone https://github.com/imkundang/TalkToData.git
    ```bash
    
    ```

3. Install the required dependencies:
    ```bash
    pip install streamlit
    ```

## Running the App

Once the dependencies are installed, you can run the Streamlit app with the following command:

```bash
streamlit run app.py
