import numpy as np
import pandas as pd
from data_processor import process_training_testing_folders
import torch

data = process_training_testing_folders(r"./data")

patient_559_train = data['training'][0]
glucose_df = patient_559_train['glucose']

glucose_array = glucose_df['glucose'].values
min_glucose_val = min(glucose_array)
max_glucose_val = max(glucose_array)
normalized_glucose_array = []
for i in glucose_array:
    normalized_glucose_array.append((i-min_glucose_val)/(max_glucose_val - min_glucose_val))

lookback = 12 # it represents 1 hr of data
horizon = 6 # next half and hour of data

x_train = []
y_train = []
for i in range(len(normalized_glucose_array) -(lookback + horizon)):
    x_train.append(normalized_glucose_array[i:i+lookback])
    y_train.append(normalized_glucose_array[i+lookback:i+lookback+horizon])

x_train = np.array(x_train, dtype=np.float32)
y_train = np.array(y_train, dtype=np.float32)

print(normalized_glucose_array[:20])
print(x_train[:5])
print(y_train[:5])

# the model architecture
l1 = torch.nn.Linear(12, 128)
l2 = torch.nn.Linear(128, 128)
l3 = torch.nn.Linear(128, 128)
l4 = torch.nn.Linear(128, 6)
relu = torch.nn.ReLU()

# .sequential is a container module that sequences modules together.
model = torch.nn.Sequential(l1, relu, l2, relu, l3, relu, l4)

print(model)