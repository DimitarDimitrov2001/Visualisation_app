# ---LIBRARIES----
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

# Spread the layout to wide
st.set_page_config(layout="wide")

# Our dataset
df = pd.read_csv('data_1.csv')

# ----FILTERING SIDEBAR MENU----

st.sidebar.write("Filters:")

# create an option to include  
chart_select = st.sidebar.selectbox(
    label = 'Include Filters:',
    options = ['Yes', 'No']
)

# when Filters are on
if  chart_select == 'Yes':

    # min/max for all 
    min_val = float(df["price"].min()) 
    max_val = float(df["price"].max())

    min_nights = int(df["minimum_nights"].min()) 
    max_nights = int(df["minimum_nights"].max())  

    min_reviews = int(df["number_of_reviews"].min()) 
    max_reviews = int(df["number_of_reviews"].max()) 

    min_rate = int(df["review_rate_number"].min()) 
    max_rate = int(df["review_rate_number"].max()) 

    # starting with sliders
    values_slider = st.sidebar.slider("Price Range ($)", min_val, max_val, (min_val, max_val))
    min_nights_values_slider = st.sidebar.slider('Minimum Nights', min_nights, max_nights, (min_nights, max_nights))
    reviews_slider = st.sidebar.slider('Number of Reviews', min_reviews, max_reviews, (min_reviews, max_reviews))
    review_rate_number_slider = st.sidebar.slider("Review rate number", min_rate, max_rate, (min_rate, max_rate))

    # couple multiselect options

    roomtype_list = df.room_type.unique()
    roomtype_multiselect = st.sidebar.multiselect("Room Type:", roomtype_list, default=roomtype_list)

    neighbourhood_groups_list = ["Manhattan", "Brooklyn", "Bronx", "Queens", "Staten Island"]
    neighbourhood_groups_multiselect = st.sidebar.multiselect('Regions in NYC:', neighbourhood_groups_list, default=neighbourhood_groups_list)

    # include neighbourhood filtering or not
    agree = st.sidebar.checkbox('EXclude neighbourhood filtering?')
    if agree:
        df_filtered = df.query(f"price.between{values_slider} and minimum_nights.between{min_nights_values_slider} and number_of_reviews.between{reviews_slider} and review_rate_number.between{review_rate_number_slider} and neighbourhood_group =={neighbourhood_groups_multiselect} and room_type ==  {roomtype_multiselect}").dropna(how="any")
    else:
        df_filter_neighnourhood = df.query(f"neighbourhood_group =={neighbourhood_groups_multiselect}").dropna(how="any")
        neighbourhood_list =  df_filter_neighnourhood.neighbourhood.unique()
        neighbourhood_multiselect = st.sidebar.multiselect("Neighbourhoods in NYC:", neighbourhood_list, default=['Chinatown','Midtown', 'West Village', 'Williamsburg'])
        df_filtered = df.query(f"price.between{values_slider} and minimum_nights.between{min_nights_values_slider} and number_of_reviews.between{reviews_slider} and review_rate_number.between{review_rate_number_slider} and neighbourhood_group =={neighbourhood_groups_multiselect} and neighbourhood == {neighbourhood_multiselect} and room_type ==  {roomtype_multiselect}").dropna(how="any")


    # Top layer of the app
    with st.container():
        row1_1, row1_2, row1_3 = st.columns(3)

        # Scatterplot: checking for relationships between the numeric columns
        with row1_1:
            numeric_columns = ['construction_year', 'price', 'service_fee', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'review_rate_number', 'availability_365', 'distance_to_subway', 'distance_from_center']
            st.title("Scatterplot")
            st.subheader("Scatterplot Settings")
            x_values = st.selectbox('X axis', options= numeric_columns)
            y_values = st.selectbox('Y axis', options= numeric_columns)
            plot = px.scatter(data_frame=df_filtered, x=x_values, y=y_values)
            st.plotly_chart(plot, use_container_width=True)

        # Maps: show where the listings are located and the density of the listings
        with row1_2:
            st.title("Scatter mapbox")
            px.set_mapbox_access_token("pk.eyJ1IjoibWl0a28yMDAxIiwiYSI6ImNsZGtoYzdrMzAxdnkzcm1pOHVlaGYxaGoifQ.7ANpE95HzAWjZzuzFEMSTQ")
            fig = px.scatter_mapbox(df_filtered, lat="latitude", lon="longitude", hover_name="name", hover_data=['neighbourhood_group','neighbourhood','room_type','price', 'service_fee'],
                                    color='neighbourhood_group', zoom=8, height=300)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

        # Violinplots: checking for distributions between different categorical values
        with row1_3:
            categorical_columns = ['neighbourhood_group', 'neighbourhood', 'instant_bookable', 'cancellation_policy', 'room_type']
            numeric_columns_1 = ['price','construction_year', 'service_fee', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'review_rate_number', 'availability_365', 'distance_to_subway', 'distance_from_center']
            st.title("Violinplot")
            st.subheader("Violinplot Settings")
            x_values_1 = st.selectbox('X axis', options= categorical_columns)
            y_values_1 = st.selectbox('Y axis', options= numeric_columns_1)
            plot = px.violin(data_frame=df_filtered, x=x_values_1, y=y_values_1)
            st.plotly_chart(plot, use_container_width=True)

    # second layer
    with st.container():
        row2_1, row2_2 = st.columns(2)
        # First Hexabins
        with row2_1:
            st.title('Hexabins for the total count')
            px.set_mapbox_access_token("pk.eyJ1IjoibWl0a28yMDAxIiwiYSI6ImNsZGtoYzdrMzAxdnkzcm1pOHVlaGYxaGoifQ.7ANpE95HzAWjZzuzFEMSTQ")
            fig11 = ff.create_hexbin_mapbox(
                data_frame=df_filtered, lat="latitude", lon="longitude",
                nx_hexagon=10, min_count = 1, opacity=0.9, labels={"color": "Point Count"},
            )
            fig11.update_layout(margin=dict(b=0, t=0, l=0, r=0))
            st.plotly_chart(fig11)
        # Second Hexabins
        with row2_2:
            df_a = df[df['price'].notna()]
            st.title('Hexabins for the average price')
            px.set_mapbox_access_token("pk.eyJ1IjoibWl0a28yMDAxIiwiYSI6ImNsZGtoYzdrMzAxdnkzcm1pOHVlaGYxaGoifQ.7ANpE95HzAWjZzuzFEMSTQ")

            fig111 = ff.create_hexbin_mapbox(
                data_frame=df_filtered, lat="latitude", lon="longitude",
                nx_hexagon=10, min_count = 1, opacity=0.9, labels={"color": "Average price"},
                color="price", agg_func=np.mean
            )
            fig111.update_layout(margin=dict(b=0, t=0, l=0, r=0))
            st.plotly_chart(fig111)
    # Scatter plot Matrix
    with st.container():
        st.title("Scatter Plot Matrix")
        numeric_columns_2 = ['price','service_fee', 'construction_year', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'review_rate_number', 'availability_365', 'distance_to_subway', 'distance_from_center']
        dimensions_var = st.multiselect("Dimensions: ", numeric_columns_2)
        fig = px.scatter_matrix(df_filtered,
        dimensions=dimensions_var)
        st.plotly_chart(fig, use_container_width=True)

# When filtering is off
if chart_select == 'No':

    # There are no filters, the full dataset is used
    st.sidebar.write("No filters applied")

    # Top layer of the app
    with st.container():
        row1_1, row1_2, row1_3 = st.columns(3)

        # Scatterplot: checking for relationships between the numeric columns
        with row1_1:
            numeric_columns = ['construction_year', 'price', 'service_fee', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'review_rate_number', 'availability_365', 'distance_to_subway', 'distance_from_center']
            st.title("Scatterplot")
            st.subheader("Scatterplot Settings")
            x_values = st.selectbox('X axis', options= numeric_columns)
            y_values = st.selectbox('Y axis', options= numeric_columns)
            plot = px.scatter(data_frame=df, x=x_values, y=y_values)
            st.plotly_chart(plot, use_container_width=True)

        # Maps: show where the listings are located and the density of the listings
        with row1_2:
            st.title("Scatter mapbox")
            px.set_mapbox_access_token("pk.eyJ1IjoibWl0a28yMDAxIiwiYSI6ImNsZGtoYzdrMzAxdnkzcm1pOHVlaGYxaGoifQ.7ANpE95HzAWjZzuzFEMSTQ")
            fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name", hover_data=['neighbourhood_group','neighbourhood','room_type','price', 'service_fee'],
                                    color='neighbourhood_group', zoom=8, height=300)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

        # Violinplots: checking for distributions between different categorical values
        with row1_3:
            categorical_columns = ['neighbourhood_group', 'neighbourhood', 'instant_bookable', 'cancellation_policy', 'room_type']
            numeric_columns_1 = ['price','construction_year', 'service_fee', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'review_rate_number', 'availability_365', 'distance_to_subway', 'distance_from_center']
            st.title("Violinplot")
            st.subheader("Violinplot Settings")
            x_values_1 = st.selectbox('X axis', options= categorical_columns)
            y_values_1 = st.selectbox('Y axis', options= numeric_columns_1)
            plot = px.violin(data_frame=df, x=x_values_1, y=y_values_1)
            st.plotly_chart(plot, use_container_width=True)
    # Second Layer
    with st.container():
        row2_1, row2_2 = st.columns(2)
        # First Hexabins
        with row2_1:
            st.title('Hexabins for the total count')
            px.set_mapbox_access_token("pk.eyJ1IjoibWl0a28yMDAxIiwiYSI6ImNsZGtoYzdrMzAxdnkzcm1pOHVlaGYxaGoifQ.7ANpE95HzAWjZzuzFEMSTQ")
            fig11 = ff.create_hexbin_mapbox(
                data_frame=df, lat="latitude", lon="longitude",
                nx_hexagon=10, min_count = 1, opacity=0.9, labels={"color": "Point Count"},
            )
            fig11.update_layout(margin=dict(b=0, t=0, l=0, r=0))
            st.plotly_chart(fig11)
        # Second Hexabins
        with row2_2:
            df_a = df[df['price'].notna()]
            st.title('Hexabins for the average price')
            px.set_mapbox_access_token("pk.eyJ1IjoibWl0a28yMDAxIiwiYSI6ImNsZGtoYzdrMzAxdnkzcm1pOHVlaGYxaGoifQ.7ANpE95HzAWjZzuzFEMSTQ")

            fig111 = ff.create_hexbin_mapbox(
                data_frame=df_a, lat="latitude", lon="longitude",
                nx_hexagon=10, min_count = 1, opacity=0.9, labels={"color": "Average price"},
                color="price", agg_func=np.mean
            )
            fig111.update_layout(margin=dict(b=0, t=0, l=0, r=0))
            st.plotly_chart(fig111)
    # Scatter Plot Matrix
    with st.container():

        numeric_columns_2 = ['price','service_fee', 'construction_year', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'review_rate_number', 'availability_365', 'distance_to_subway', 'distance_from_center', 'distance_to_subway', 'distance_from_center']
        st.title("Scatter Plot Matrix")
        dimensions_var = st.multiselect("Dimensions: ", numeric_columns_2)
        fig = px.scatter_matrix(df,
        dimensions=dimensions_var)
        st.plotly_chart(fig, use_container_width=True)
