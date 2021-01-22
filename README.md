# Minor-Project-1
Farmers' e-assistant : A web application to detect leaf diseases in plant

The application was built using Flask 1.1- python web framework. It takes image of infected leaf of banana plant captured in natural environment as input and does the classification and displays the results back to the user.

model.py - This file is used to define cnn model(VGG-16 transfer learning model from keras) and save to a file (.h5). This binary classification model was trained using processed images of banana plant leaves belonging to diseased and not diseased(bacterial wilt and black sigatoka) categories. 

download complete project here, https://drive.google.com/file/d/15Z5kJvOLIuDiB3qSTuDWV3AWtSfhVs8X/view?usp=sharing

A web application designed to detect 2 major leaf diseases in banana plant(using CNN) from image uploaded by farmers & provides suggestions to recover from that disease.Tech stack:Python 3,Keras2.4 & Tensorflow2.2,Flask1.1,libraries:openCV,Numpy, PIL
