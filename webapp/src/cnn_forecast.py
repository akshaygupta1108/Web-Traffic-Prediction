import pandas as pd
import numpy as np
from keras.models import load_model
from keras.models import Model
from keras.layers import Input, Conv1D, Dense, Activation, Dropout, Lambda, Multiply, Add, Concatenate
from keras.optimizers import Adam

from data_processing import log_transform,inverse_log_transform

weights_path = 'models/seq2seq_conv_weights.h5'

input_days = 430
pred_steps = 60

model = None

def create_model(n_filters = 32, filter_width = 2, num_layers = 8):

    dilations = [2**i for i in range(num_layers)]

    x = Input(shape=(None,1))
    history_sequence = x
    skips = list()

    for layer_num in range(num_layers):
        dilation = dilations[layer_num]

        x = Conv1D(16,1,padding='same',activation='relu')(x)

        x_f = Conv1D(filters=n_filters,
                    kernel_size = filter_width,
                    padding='causal',
                    dilation_rate=dilation)(x)
        
        x_f = Activation('tanh')(x_f)
        
        x_g = Conv1D(filters=n_filters,
                    kernel_size = filter_width,
                    padding='causal',
                    dilation_rate=dilation)(x)
        
        x_g = Activation('sigmoid')(x_g)
            
        mul = Multiply()([x_f,x_g])
        mul = Conv1D(16,1,padding='same',activation='relu')(mul)

        x = Add()([x,mul])

        skips.append(mul)

    out = Activation('relu')(Add()(skips))

    out = Conv1D(128,1,padding='same')(out)
    out = Activation('relu')(out)
    out = Dropout(0.2)(out)

    out = Conv1D(1,1,padding='same')(out)

    def slice(x, seq_length):
        return x[:,-seq_length:,:]

    pred_seq_train = Lambda(slice, arguments={'seq_length':pred_steps})(out)

    model = Model(history_sequence, pred_seq_train)
    model.compile(Adam(), loss='mean_absolute_error')

    return model

def load_weights(weights_path,model=None):
    if model==None:
        model = create_model()
    model.load_weights(weights_path)
    return model


def predict_sequence(input_sequence):

    history_sequence = input_sequence.copy()
    pred_sequence = np.zeros((1,pred_steps,1)) # initialize output (pred_steps time steps)  
    for i in range(pred_steps):
        
        # record next time step prediction (last time step of model output) 
        last_step_pred = model.predict(history_sequence)[0,-1,0]
        pred_sequence[0,i,0] = last_step_pred
        
        # add the next time step prediction to the history sequence
        history_sequence = np.concatenate([history_sequence, 
                                           last_step_pred.reshape(-1,1,1)], axis=1)

    return pred_sequence


def cnn_forecast(data,days=7):
    tr_data, mean = log_transform(data)
    tr_data = tr_data[-input_days:]
    if len(tr_data) < input_days:
        raise Exception("Not enough data")

    tr_data = np.reshape(tr_data,(1,input_days,1))

    pred = predict_sequence(tr_data)
    pred = np.reshape(pred,(pred_steps,))
    pred = inverse_log_transform(list(pred),mean)

    pred = list(pred)
    pred = pred[:days]

    sequence = list(np.reshape(data,(len(data),))) + pred

    return sequence


model = load_weights(weights_path)
print('Loaded CNN model')