import numpy as np
from sklearn.linear_model import LinearRegression
import json

try:
    with open("offset_data.json", "r") as file:
        dict = json.load(file)
        x_data = dict['font_size_list']
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
    params = {'coef': float(model.coef_[0]), 'intercept': float(model.intercept_)}
    print(params)
except:
    print("Data does not exist!")