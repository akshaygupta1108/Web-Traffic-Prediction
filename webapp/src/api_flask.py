from flask import Flask, json, request
from helpers import get_daily_views, plot_graph, write_to_file
from data_processing import transform,inverse_transform,get_loss
from arima_forecast import arima_forecast
from lstm_forecast import lstm_forecast,past
from cnn_forecast import cnn_forecast

api = Flask(__name__)

@api.route('/<model>/<search_word>/<language>/<int:forecast_days>/<access>',methods=['GET'])
def get_result(model,search_word,language,forecast_days,access):

    print('Getting results for ',search_word)
    data = get_daily_views(search_word,language,access)

    if model=='ARIMA':
        prediction = arima_forecast(data,forecast_days)
    elif model=='LSTM':
        prediction = lstm_forecast(data,forecast_days)
        data = data[past:]
    elif model=='CNN':
        prediction = cnn_forecast(data,forecast_days)
    else:
        raise Exception("Invalid model name")

    loss = get_loss(data,prediction,model,past)

    plot_title = model+' forecast for '+search_word

    if model=='CNN':
        image_path = plot_graph(prediction,data,labels=['Predicted Views','Original Views'],colors=['#ff7f0e','#1f77b4'],title=plot_title)
    else:
        image_path = plot_graph(data,prediction,labels=['Original Views','Predicted Views'],title=plot_title)

    prediction_file_path = write_to_file(str(prediction))

    temp_dict = {'predictionLink':prediction_file_path,'loss':loss,'graphImageSource':image_path}
    return json.dumps(temp_dict)

api.run()