# Project Title: Web Traffic Time Series Forecasting
# Members: Yellapragada Srikar Anand (IIT2017504), Akshay Gupta (IIT2017505)

# PROJECT DESCRIPTION:
Data analysis, ML and DL models to analyze, predict and forecast the web views for wikipedia pages.
Comparison can also be done between the models ( ARIMA , LSTM and CNN)
And a web application which can interact with user and access the wikipedia api views data for any search keyword and forecast the data based on the three models. A short comparison can also be done by switching between the models ( ARIMA , LSTM and CNN).


# Prerequisites
Python version >=3.7

Tensorflow

Keras

sklearn

Flask

numpy

pandas

matplotlib

statsmodels

Google Chrome 

Internet Connection required

# RUNNING THE WEB APP

# Step 1:
Install and enable the CORS extension (link provided below), on Google Chrome, to allow the frontend to interact with the python Flask api
Make sure to disable the extension as soon as running the demo is finished.
Link to CORS web extension: "https://chrome.google.com/webstore/detail/moesif-origin-cors-change/digfbfaphojjndkpccljibejjbppifbc"

# Step 2: 
Extract the zip folder "WebTrafficTimeSeriesForecasting.zip" and open the "webapp" folder

# Step 3:
From "src" folder, open and launch "api_flask.py" with python interpreter
From "frontend" folder, open the "home.html" file, with which the user can interact.

# Step 4:
Enter a search word, select the language and access type, and click on search.
Wait for the result to be displayed which is being fetched from Wikimedia REST API through internet.

The model loss and forecasting graph can be seen.
Click on the "Click here" hyperlink to see the result in text format.
Change the parameters, model-type and forecast days length to see how different models work with different pages and parameters.


# RUNNING THE MODELS IN NOTEBOOKS:

# STEP 1:
Extract the zip folder "WebTrafficTimeSeriesForecasting.zip" and open the "notebooks" folder

# STEP 2:
Download the dataset (link mentioned below). Rename the file "train_1.csv" as "web_traffic_train_1.csv" and place it in the data folder.
Dataset download link: "https://www.kaggle.com/c/web-traffic-time-series-forecasting/data"

# STEP 3:
To run ARIMA model, simply run the whole notebook "ARIMA.ipynb". The prediction can be seen for average page views for english data.

To run the LSTM model, open the notebook "LSTM.ipynb". the weights have already been saved to "weights" folder. So one the model need not be trained again. The output of the prediction for various pages can be seen along with the average views of english data.

To run the CNN model, open the notebook "CNN.ipynb". the weights have already been saved to "weights" folder. So one the model need not be trained again. The output of the prediction for various pages can be seen along with the average views of english data.


