import tensorflow as tf
from keras import layers, Input
from keras import models
import numpy as np

input_shape = (6, 1)

class Model_NN():
    def __init__(self):
        self.model = models.Sequential()
        self.model.add(Input(shape = (6,)))
        self.model.add(layers.Dense(128, activation='sigmoid'))
        self.model.add(layers.Dense(64, activation='sigmoid'))
        self.model.add(layers.Dense(3))
        self.model.compile(loss='mse',
                      optimizer='adam',
                      metrics=['acc'])
        self.model.summary()

    def training(self, x, y):
        print('Train X : ',x)
        print('Train Y : ',y)
        return self.model.train_on_batch(
            np.array(x),
            np.array(y),
            sample_weight=None,
            class_weight=None,
            reset_metrics=True,
            return_dict=False)

    def predict1(self, x):
#        self.model.summary()
        x = np.array([x])
#        print(x.shape)
        x00 =  self.model.predict(
            x,
            batch_size=None,
            verbose="auto",
            steps=None,
            callbacks=None,
            max_queue_size=10,
            workers=1,
            use_multiprocessing=False)
        #print(f'x ={x}, x00 ={x00}')
        return x00
