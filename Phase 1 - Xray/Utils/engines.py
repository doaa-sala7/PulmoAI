# #@title #Engines
# # %%writefile engines.py
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D,GRU, LSTM
from keras.layers import Activation, TimeDistributed, LSTM, BatchNormalization
from keras.layers import Dense, Conv2D, MaxPool2D, Dropout, Flatten, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers.legacy import SGD, Adam
from keras.models import Sequential, Model
#from tensorflow.keras.optimizers import SGD, Adam, RMSprop

size = (224, 224,3)

def create_cnn_lstm(Image_shape=size, block1=True, block2=True, block3=True,
                 block4=True, block5=True, lstm=True, regularizer=keras.regularizers.l2(0.0001),
                 Dropout_ratio=0.15):

    # * Create the model
    model = keras.Sequential()

    # * configure the inputshape
    model.add(keras.Input(shape=Image_shape))

    # * Add the first block
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu',
              trainable=block1, kernel_regularizer=regularizer))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu',
              trainable=block1, kernel_regularizer=regularizer))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())

    # * Add the second block
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu',
              trainable=block2, kernel_regularizer=regularizer))
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu',
              trainable=block2, kernel_regularizer=regularizer))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())

    # * Add the third block
    model.add(Conv2D(256, (3, 3), padding='same', activation='relu',
              trainable=block3, kernel_regularizer=regularizer))
    model.add(Conv2D(256, (3, 3), padding='same', activation='relu',
              trainable=block3, kernel_regularizer=regularizer))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())

    # * Add the fourth block
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu',
              trainable=block4, kernel_regularizer=regularizer))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu',
              trainable=block4, kernel_regularizer=regularizer))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu',
              trainable=block4, kernel_regularizer=regularizer))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())

    # * Add the fifth block
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu',
              trainable=block5, kernel_regularizer=regularizer))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu',
              trainable=block5, kernel_regularizer=regularizer))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu',
              trainable=block5, kernel_regularizer=regularizer))
    
    model.add((MaxPooling2D(pool_size=(2, 2))))
    model.add(BatchNormalization())

    # * Reshape the output of the last layer to be used in the LSTM layer
    model.add(keras.layers.Reshape((7*7, 512)))
    model.add(LSTM(512, activation='relu', trainable=lstm, return_sequences=True))
    model.add(BatchNormalization())

    #* flatten + Fc layer
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(Dropout_ratio))
    model.add(BatchNormalization())
    
    # * Output layer
    #model.add(Dense(3, activation='linear'))
    model.add(Dense(3, activation='sigmoid'))
    #print('Done')
    return model


#* compile function
def cnn_lstm_compile(model, loss = 'categorical_crossentropy', optimizer = SGD(learning_rate=0.0001, decay=1e-6)):
    model.compile(
        #loss =keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        loss=loss,
        optimizer=optimizer,
        metrics=['accuracy']
    )
def cnn_compile(model):
  model.compile(loss = "categorical_crossentropy", optimizer = Adam(lr=0.0001, decay=1e-6),metrics = ["accuracy"])


  

def create_cnn_model():
    model = Sequential()

    model.add(Conv2D(input_shape=(224, 224,3),filters=64, kernel_size=(5, 5),  padding="same",kernel_regularizer=keras.regularizers.l2(0.0001), activation='LeakyReLU'))
    model.add(Conv2D(filters=64, kernel_size=(5, 5),  padding="same",kernel_regularizer=keras.regularizers.l2(0.0001), activation='LeakyReLU'))
    model.add(Conv2D(filters=64, kernel_size=(5, 5),  padding="same",kernel_regularizer=keras.regularizers.l2(0.0001), activation='LeakyReLU'))
    model.add(Conv2D(filters=64, kernel_size=(5, 5),  padding="same",kernel_regularizer=keras.regularizers.l2(0.0001), activation='LeakyReLU'))
    model.add(MaxPool2D(pool_size=(5,5), padding='same'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))

    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding="same",kernel_regularizer=keras.regularizers.l2(0.0001), activation='LeakyReLU'))
    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding="same",kernel_regularizer=keras.regularizers.l2(0.0001), activation='LeakyReLU'))
    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding="same",kernel_regularizer=keras.regularizers.l2(0.0001), activation='LeakyReLU'))
    model.add(Conv2D(filters=128, kernel_size=(5, 5), padding="same",kernel_regularizer=keras.regularizers.l2(0.0001),activation='LeakyReLU'))
    model.add(MaxPool2D(pool_size=(5,5), padding='same'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))

    model.add(Flatten())

    model.add(Dense(512,activation = "LeakyReLU"))
    model.add(Dropout(0.3))

    model.add(Dense(512,activation = "LeakyReLU"))
    model.add(Dropout(0.3))

    model.add(Dense(512,activation = "LeakyReLU"))
    model.add(Dropout(0.3))

    model.add(Dense(3,activation = "softmax"))

    return model