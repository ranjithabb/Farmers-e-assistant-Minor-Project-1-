# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:01:06 2020

@author: ranju
"""

'''# organize dataset into a useful structure
from os import makedirs
from os import listdir
from shutil import copyfile
# create directories
dataset_home = 'D:/minor project 4th sem/finalize_dataset/'
# create label subdirectories
labeldirs = ['healthy/', 'unhealthy/']
for labldir in labeldirs:
	newdir = dataset_home + labldir
	makedirs(newdir, exist_ok=True)
# copy training dataset images into subdirectories
src_directory = 'D:/minor project 4th sem/dataset'
for file in listdir(src_directory):
	src = src_directory + '/' + file
	if file.startswith('unh'):
		dst = dataset_home + 'unhealthy/'  + file
		copyfile(src, dst)
	elif file.startswith('h'):
		dst = dataset_home + 'healthy/'  + file
		copyfile(src, dst)'''
        


# save the final model to file
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

# define cnn model
def define_model():
	# load model
	model = VGG16(include_top=False, input_shape=(224, 224, 3))
	# mark loaded layers as not trainable
	for layer in model.layers:
		layer.trainable = False
	# add new classifier layers
	flat1 = Flatten()(model.layers[-1].output)
	class1 = Dense(128, activation='relu', kernel_initializer='he_uniform')(flat1)
	output = Dense(1, activation='sigmoid')(class1)
	# define new model
	model = Model(inputs=model.inputs, outputs=output)
	# compile model
	opt = SGD(lr=0.001, momentum=0.9)
	model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
	return model

# run the test harness for evaluating a model
def run_test_harness():
# define model
	model = define_model()
	# create data generator
	datagen = ImageDataGenerator(featurewise_center=True)
	# specify imagenet mean values for centering
	datagen.mean = [123.68, 116.779, 103.939]
	# prepare iterator
	train_it = datagen.flow_from_directory('D:/minor project 4th sem/finalize_dataset/',
		class_mode='binary', batch_size=10, target_size=(224, 224))
	# fit model
	model.fit_generator(train_it, steps_per_epoch=len(train_it), epochs=10, verbose=0)
	# save model
	model.save('model.h5')

# entry point, run the test harness
run_test_harness()





