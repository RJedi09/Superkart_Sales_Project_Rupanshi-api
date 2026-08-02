# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_api = Flask("SuperKart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("SuperKart__model_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_sales_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint for single product prediction (POST request)
@superkart_sales_api.post('/v1/predict')
def predict_sales():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product and store details and returns
    the predicted sales total as a JSON response.
    """
    # Get the JSON data from the request body
    product_store_data = request.get_json()

    # Extract relevant features from the JSON data
 
    sample = {
        'Product_Weight': product_store_data['Product_Weight'],
        'Product_Sugar_Content': product_store_data['Product_Sugar_Content'],
        'Product_Type': product_store_data['Product_Type'],
        'Product_Allocated_Area': product_store_data['Product_Allocated_Area'],
        'Product_MRP': product_store_data['Product_MRP'],
        'Store_Id': product_store_data['Store_Id'],
        'Store_Size': product_store_data['Store_Size'],
        'Store_Location_City_Type': product_store_data['Store_Location_City_Type'],
        'Store_Type': product_store_data['Store_Type'],
        'Store_Age_Years': product_store_data['Store_Age_Years']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales_total = model.predict(input_data)[0]

    # Convert predicted_sales_total to Python float and round
    predicted_sales_total = round(float(predicted_sales_total), 2)

    # Return the predicted sales total
    return jsonify({'Predicted Product Store Sales Total': predicted_sales_total})


# Define an endpoint for batch prediction (POST request)
@superkart_sales_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing product and store details for multiple entries
    and returns the predicted sales totals as a list in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Ensure the input_data columns match the model's expected features:
    # ['Product_Weight', 'Product_Allocated_Area', 'Product_MRP', 'Store_Age_Years',
    #  'Product_Sugar_Content', 'Product_Type', 'Store_Id', 'Store_Size',
    #  'Store_Location_City_Type', 'Store_Type']
    # The batch CSV must contain all of these columns.

    # Make predictions for all entries in the DataFrame
    predicted_sales_totals = model.predict(input_data).tolist()

    # Round each prediction and convert to float
    predicted_sales_totals = [round(float(sales), 2) for sales in predicted_sales_totals]

    # Return the list of predictions as a JSON response
    return jsonify({'Predicted Product Store Sales Totals': predicted_sales_totals})

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_api.run(debug=True)
