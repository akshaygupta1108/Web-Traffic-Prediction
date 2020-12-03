from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_squared_error

def transform(data):
    sc = MinMaxScaler()
    data = sc.fit_transform(np.reshape(data,(-1,1)))
    data = list(np.reshape(data,(len(data),)))
    return data,sc

def inverse_transform(data,sc):
    data = np.reshape(data,(-1,1))
    data = sc.inverse_transform(data)
    return list(np.reshape(data,(len(data),)))

from math import log1p
def log_transform(sequence):
  sequence = list(np.reshape(sequence,(len(sequence),)))
  sequence = np.array([log1p(x) for x in sequence])
  mean = sequence.mean()
  sequence = sequence - mean
  return sequence,mean


def inverse_log_transform(sequence,mean):
  sequence = np.reshape(sequence,(len(sequence),))
  sequence = sequence + mean
  sequence = np.exp(sequence) - 1
  return sequence

def get_loss(data,prediction,model,past=None):
  if len(data)<len(prediction):
    prediction = prediction[:len(data)]
  elif len(prediction)<len(data):
    data = data[:len(prediction)]
  return mean_squared_error(data,prediction,squared=False)