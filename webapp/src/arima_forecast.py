from statsmodels.tsa.arima_model import ARIMA

import numpy as np
import pandas as pd

import warnings



# params = {'en': [4,1,0], 'ja': [7,1,1], 'de': [7,1,1], 'na': [4,1,0], 'fr': [4,1,0], 
#               'zh': [7,1,1], 'ru': [4,1,0], 'es': [7,1,1]}
params = [(7,1,0),(4,1,1),(7,1,1)]



def arima_forecast(data,days):
    data = np.nan_to_num(np.array(pd.DataFrame(data).fillna(0)))
    predictions = []
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        for hparams in params:
            try:
                arima = ARIMA(data, hparams)
                model = arima.fit(disp=False)
                prediction = model.predict(2,len(data)+days-1,typ='levels')
                return prediction
            except:
                pass
    # if len(predictions)==0:
    #     return None,None
    # losses = [x[0] for x in predictions]
    # print('losses: ',losses)
    # i = losses.index(min(losses))
    # return predictions[i]
    
