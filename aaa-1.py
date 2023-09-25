import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask
from sklearn.model_selection import train_test_split
import serial
import time

app = Flask(__name__)

df= pd.read_csv(r"C:\Users\Zribi Ahmed\Desktop\pcd\Data_for_UCI_named.csv")

df['stabf']=df['stabf'].replace(['unstable','stable'],['0','1'])

from sklearn.linear_model import LogisticRegression 
X = df.drop(['stabf', 'stab'], axis=1)
Y=df['stabf']
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Create an instance of the RandomForestClassifier class with desired hyperparameters
rfc = RandomForestClassifier(n_estimators=50, min_samples_split=5, min_samples_leaf=2, max_features='sqrt', max_depth=None)

# Fit the model
rfc.fit(X_train, y_train)
ser = serial.Serial('COM4', 115200, timeout=1)
ser.flush()
@app.route('/',methods=['GET'])
def Output(): 
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            powers = data.split(',')
            if len(powers) >= 3 and powers[0] != '' and powers[1] != '' and powers[2] != '':
                power1 = float(powers[0])
                power2 = float(powers[1])
                power3 = float(powers[2])
                print("Power 1: ", power1, "mW")
                print("Power 2: ", power2, "mW")
                print("Power 3: ", power3, "mW")
                new_data = [[0.82,5.42,9.43,2.48,3.04, -power1/200, -power2/200, -power3/40,0.702, 0.1160, 0.57,0.578]]

                # Make a prediction using the pre-fitted model
                prediction = rfc.predict(new_data)

                # Print the predicted target value
                print("Predicted target value:", prediction)
                
                # Return the predicted target value as a response to the HTTP GET request
                return str(prediction.tolist())
            
        

if __name__ == '__main__':
  from waitress import serve
  serve(app, host='0.0.0.0', port=3000)
