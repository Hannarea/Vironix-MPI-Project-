# -*- coding: utf-8 -*-
"""classification_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NhECI87T9fOQcOMh5sO2PocykB4dWByO

# Needs comments 
# 96% accuracy on test set
"""

# imports 
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import random as rnd
import csv
import requests

"""# Generate Data Function """

def generate_data(cases, col, prob):
    '''
    
    Parameters
    ----------
    cases : A matrix of cases where each row is an individual 
    and each column is a feature 
    col : The column of the feature we are generating values for
    prob : the probability that an individual has the feature represented 
    in column col given their severity (note the severity is prespecified) OR 
    a negative number specifying which normal distribution to use. 
    Returns
    -------
    A matrix of cases where each row is an individual 
    and each column is a feature.  
    '''
    # we traverse through the matrix columns
    
    if prob == -1: #37.6470588% smokers(2), 49.4117647% ex_smokers(1), and 12.9411765% not smokers(0)
        for i in range(len(cases[:,0])):
            rand = rnd.random()
            if rand <= 0.129411765:
                cases[i,col] = 0
            elif rand <= 0.129411765 + 0.494117647:
                cases[i,col] = 1
            else:
                cases[i, col] = 2
 
    elif prob == -2: #28.5714286% smokers(2), 54.7619048% ex_smokers(1), and 16.6666666% never smoked(0)
        for i in range(len(cases[:,0])):
            rand = rnd.random()
            if rand <= 0.166666666:
                cases[i,col] = 0
            elif rand <= 0.166666666 + 0.547619048:
                cases[i,col] = 1
            else:
                cases[i, col] = 2
             
    else:
        for i in range(len(cases[:,0])):
            rand = rnd.random()
            if rand <= prob:
                cases[i,col] = 1
            else:
                cases[i,col] = 0
        
    return cases

"""# Parameters and Probabilites """

# Number of cases for each severity :
mild = 80
severe = 80

# Number of features we are considering
n = 12
y = []
count = 0
X = []

# Probabilities of having the feature given the severity 
# Severe cases
female_s = 0.2
smoker_s = -1 # we will generate 37.6470588% smokers, 49.4117647% ex_smokers, and 12.9411765% never smoked
wheezing_s = 0.894117647
congestion_s = 0.494117647
rhinorrhea_s = 0.388235294
sore_throat_s = 0.223529412
sputum_s = 0.576470588
fever_s = 0.164705882
headache_s = 0.317647059
muscle_pain_s = 0.188235294
hoarse_s = 0.4
steroids_preadmission_s = 0.576470588
# Not Severe cases
female = 0.095238095
smoker = -2 # we will generate 28.5714286% smokers, 54.7619048% ex_smokers, and 16.6666666% never smoked
wheezing = 0.523809524
congestion = 0.214285714
rhinorrhea = 0.238095238
sore_throat = 0.023809524
sputum = 0
fever = 0.095238095
headache = 0.023809524
muscle_pain = 0.30952381
hoarse = 0.30952381
steroids_preadmission = 0.547619048

# Probability matrix for feature bases on severity:
# prob[i,j] will be the probability of having feature j given you have severity i
prob = np.array([
    [female, smoker, wheezing, congestion, rhinorrhea, sore_throat, sputum, fever, headache, muscle_pain, hoarse, steroids_preadmission],
    [female_s, smoker_s, wheezing_s, congestion_s, rhinorrhea_s, sore_throat_s, sputum_s, fever_s, headache_s, muscle_pain_s, hoarse_s, steroids_preadmission_s]
    ])

"""#Generate Data """

# Here we generate the mild cases set
mild_cases = np.zeros((mild, n))
for i in range(n):
    generate_data(mild_cases, i, prob[0,i])

    
# Here we generate the severe cases set
severe_cases = np.zeros((severe, n))
for i in range(n):
    generate_data(severe_cases, i, prob[1,i])

# make testing case 
test_set1 = np.zeros((mild, n))
for i in range(n):
  generate_data(test_set1, i, prob[0,i])

# make testing case 
test_set2 = np.zeros((severe, n))
for i in range(n):
  generate_data(test_set2, i, prob[1,i])

X = []
y = []

for i in range(mild):
  X.append(severe_cases[i].tolist())
  y.append(1)
  X.append(mild_cases[i].tolist())
  y.append(0)

test_X = []
test_y = []

for i in range(mild):
  test_X.append(severe_cases[i].tolist())
  test_y.append(1)
  test_X.append(mild_cases[i].tolist())
  test_y.append(0)

#print("Mild Cases:")
#print(mild_cases)

#print("Severe Cases:")
#print(severe_cases)
#print(y)

"""# Here we have a Neural Network Model"""

# create model
model = Sequential()
model.add(Dense(12, input_dim=12, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(X, y, epochs=150, batch_size=10)
# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

model.evaluate(test_X, test_y)

"""# Here is a logistic model"""

# write to file

filename = "population_160_people.csv"
fields = ["severity","female", "smoke", "wheezing", "congestion", "rhinorrhea", "sore throat", "sputum", "fever", "headache", "muscle pain", "hoarse voice", "steroids"]


with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    rows = []
    for i in range(mild):
      row = ["0"]
      for j in range(12):
        row.append(mild_cases[i][j])
      rows.append(row)

    for i in range(mild):
      row = ["1"]
      for j in range(12):
        row.append(severe_cases[i][j])
      rows.append(row)
    
    csvwriter.writerows(rows)