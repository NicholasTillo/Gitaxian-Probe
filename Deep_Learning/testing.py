import json
import tensorflow as tf
import keras
from keras import layers
from numpy import random
import numpy as np
import requests
import time 
import flatdict
import itertools


arr = np.array([i for i in range(262)])
print(tf.reshape([0, 262],tf.stack(arr)))
arr2 = []
for i in range(262):
    arr2 = np.append(arr2, [0])
print(tf.stack(arr2))


# data = ["Thraben Sentry // Thraben Militia",        "en",        "2011-09-30",        "transform",        "1",        "highres_scan",        "",        "4.0",        "Creature — Human Soldier // Creature — Human Soldier",        "",        "",        "",        "not_legal",        "not_legal",        "not_legal",        "not_legal",        "not_legal",        "not_legal",        "not_legal",        "legal",        "legal",        "legal",        "legal",        "legal",        "legal",        "legal",        "not_legal",        "not_legal",        "not_legal",        "legal",        "legal",        "not_legal",        "not_legal",        "not_legal",        "0",        "0",        "0",        "0",        "0",        "isd",        "Innistrad",        "expansion",        "38",        "0",        "common",        "",        "David Rapoza",        "black",        "2003",        "0",        "0",        "1",        "0",        "21773",        "11296",        "0.08",        "0.24",        "None",        "0.09",        "0.14",        "0.04",        "0",        "0",        "0",        "0",        "0",        "1",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "1",        "1",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "1",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        
#                                       "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "0",        "1",        "1",        "0",        "1",        "1"]
# data = [data,data]
# y_vec = 0.07142857142857142

# testing_data = [
#         "Nine Lives",
#         "en",
#         "2020-07-31",
#         "normal",
#         "0",
#         "lowres",
#         "{1}{W}{W}",
#         "3.0",
#         "Enchantment",
#         "Hexproof\nIf a source would deal damage to you, prevent that damage and put an incarnation counter on Nine Lives.\nWhen there are nine or more incarnation counters on Nine Lives, exile it.\nWhen Nine Lives leaves the battlefield, you lose the game.",
#         "",
#         "",
#         "not_legal",
#         "not_legal",
#         "legal",
#         "legal",
#         "legal",
#         "legal",
#         "legal",
#         "legal",
#         "legal",
#         "not_legal",
#         "legal",
#         "legal",
#         "legal",
#         "legal",
#         "not_legal",
#         "legal",
#         "not_legal",
#         "not_legal",
#         "legal",
#         "not_legal",
#         "not_legal",
#         "not_legal",
#         "0",
#         "0",
#         "1",
#         "1",
#         "0",
#         "prm",
#         "Magic Online Promos",
#         "promo",
#         "81938",
#         "1",
#         "rare",
#         "",
#         "Paul Scott Canavan",
#         "black",
#         "2015",
#         "0",
#         "0",
#         "0",
#         "0",
#         "6147",
#         "2731",
#         "None",
#         "None",
#         "None",
#         "None",
#         "None",
#         "0.38",
#         "1",
#         "0",
#         "0",
#         "0",
#         "0",
#         "1",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "1",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "0",
#         "1",
#         "0",
#         "1",
#         "1"
#     ]
# testing_y_vec = 0.08333333333333333



# layer = keras.layers.TextVectorization(split = None, )
#         #layer = keras.layers.TextVectorization()

# for i in data:
#     layer.adapt(data)

# x2 = []

# for i in data:
#     q = layer(i)
#     x2.append(np.array(q))

# data = np.array(x2)
# #data = tf.stack(layer(data))


# layer.adapt(testing_data)
# testing_data = tf.stack(layer(testing_data))
# #print(tf.stack(data))
# #data = tf.stack(data)

# """
# inputs = keras.Input(shape = (262,))

# dense = layers.Dense(64, activation="relu")(inputs)
# #Do a dropout here, 
# dense2 = layers.Dense(64, activation="relu")(dense)

# outputs = layers.Dense(10)(dense2)
# model = keras.Model(inputs=inputs, outputs=outputs, name="mnist_model")
# """
# """
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Input(shape=(262,)),

#     tf.keras.layers.Dense(262, activation='relu'),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Dense(262, activation='relu'),

#     tf.keras.layers.Dense(1)
# ])
# print(tf.keras.layers.Input(shape=(262,)))
# """

# model = tf.keras.models.Sequential()
# model.add(tf.keras.layers.Input(shape=(262,)))
# model.add(tf.keras.layers.Dense(262, activation='relu'))
# model.add(tf.keras.layers.Dense(1))

# model.summary()

# model.compile(
#     loss=keras.losses.MeanAbsoluteError(
#                                         reduction="sum_over_batch_size", 
#                                         name="mean_absolute_error"
#                                         ),
#     optimizer=keras.optimizers.Adagrad(),
#     metrics=[keras.metrics.MeanSquaredError(name="mean_squared_error",dtype=None)]
# )
# list(data).append(y_vec)
# data = tf.data.Dataset(data)
# print(data)

# history = model.fit(
#                 data,
#                 y_vec,
#                 #validation_data = validation_full,
#                 verbose = 1
#                 #MAYBE SAMPLE WEIGHT. 
#                 )

# ret = model.predict(testing_data)

# print(ret)
# print(y_vec)
