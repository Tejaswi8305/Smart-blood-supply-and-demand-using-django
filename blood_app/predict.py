import pickle
import numpy as np

# load trained model
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'ml_model', 'blood_model.pkl')

model = pickle.load(open(model_path, 'rb'))

def predict_demand(month, blood_group, collected, supplied):
    
    input_data = np.array([[month, blood_group, collected, supplied]])
    
    prediction = model.predict(input_data)
    
    return int(prediction[0])