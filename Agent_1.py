import tensorflow as tf
from keras import layers
from keras import models

input_shape = (6, 1)

class Model_NN():
    def __init__(self):
        self.model = models.Sequential()
        self.model.add(layers.InputLayer(6,))
        self.model.add(layers.Dense(128, activation='sigmoid'))
        self.model.add(layers.Dense(64, activation='sigmoid'))
        self.model.add(layers.Dense(3))
        self.model.compile(loss='mse',
                      optimizer='adam',
                      metrics=['acc'])
        
    def training(self, x, y, model):
        return model.train_on_batch(
            x,
            y,
            sample_weight=None,
            class_weight=None,
            reset_metrics=True,
            return_dict=False)

    def predict1(self, x, model):
        x = tf.reshape(x, shape=(1,6))
        x00 =  model.predict(
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
