
import streamlit as st
import pandas as pd
import requests

# Backend Flask API URL.
# "backend" is the container name assigned when running the backend Docker
# container on the same Docker network - Docker's internal DNS resolves it.
BACKEND_URL = "http://backend:7860/v1/predict"

# Streamlit UI for Sales Revenue Forecasting
st.title("SuperKart Sales Revenue Forecasting App")
st.write("This tool predicts the total sales revenue for a given product in a specific store.")

st.subheader("Enter the product and store details:")

# Collect user input
product_weight = st.number_input("Product Weight (kg)", min_value=4.0, max_value=22.0, value=12.66, step=0.01)
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_type = st.selectbox(
    "Product Type",
    ["Dairy", "Snack Foods", "Fruits and Vegetables", "Frozen Foods", "Household",
     "Baking Goods", "Canned", "Health and Hygiene", "Meat", "Soft Drinks",
     "Breads", "Hard Drinks", "Starchy Foods", "Others", "Breakfast", "Seafood"]
)
product_allocated_area = st.number_input("Product Allocated Area (ratio)", min_value=0.004, max_value=0.298, value=0.06, step=0.001, format="%.3f")
product_mrp = st.number_input("Product MRP (Maximum Retail Price)", min_value=30.0, max_value=270.0, value=150.0, step=0.01)
store_id = st.selectbox("Store Id", ["OUT001", "OUT002", "OUT003", "OUT004"])
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
store_age_years = st.number_input("Store Age (Years)", min_value=17, max_value=39, value=20)

# Build the JSON payload expected by the backend /v1/predict endpoint
payload = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Type": product_type,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Id": store_id,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type,
    "Store_Age_Years": store_age_years
}

# Predict button
if st.button("Predict Sales Revenue"):
    try:
        response = requests.post(BACKEND_URL, json=payload)
        response.raise_for_status()
        prediction = response.json()["Predicted Product Store Sales Total"]
        st.write(f"The predicted sales revenue for this product in the store is: ${prediction:.2f}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not reach the prediction backend: {e}")
    except (KeyError, ValueError):
        st.error(f"Unexpected response from backend: {response.text}")
