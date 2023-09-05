import numpy as np
from sklearn.linear_model import LinearRegression
from os import path
import json

desktop = path.join(path.expanduser("~"), "Desktop")
file_path = path.join(desktop, "button_data_new.json")

with open(file_path, "r") as file:
    dict = json.load(file)
    x_data = dict['font_list']
    y_data = dict['offset_list']

# Given data
x_data = np.array(x_data)  # Continue with all x values
y_data = np.array(y_data)  # Continue with all y values

# Reshape the data for scikit-learn
x_data = x_data.reshape(-1, 1)
y_data = y_data.reshape(-1, 1)

# Create and train the linear regression model
model = LinearRegression()
model.fit(x_data, y_data)

# Make predictions for new x values (assuming you have some new x values)
new_x_values = np.array([57, 810, 820, 830]).reshape(-1, 1)
predictions = model.predict(new_x_values)

# Print the predictions of y based on new x values
print("Predicted y values:")
for x, y_pred in zip(new_x_values, predictions):
    print(f"x = {x[0]}, y_pred = {y_pred[0]}")