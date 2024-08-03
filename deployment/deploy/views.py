from django.http import HttpResponse
from django.shortcuts import render
from joblib import load
import os
import dotenv
import numpy as np
from sklearn.preprocessing import StandardScaler


dotenv.load_dotenv()
model_directory = os.getenv('Model_Dir')
KMeansPick = os.getenv('KMeansPick')
KMeansDrop = os.getenv('KMeansDrop')
model_name = os.getenv('Model_Name')
scaler_name = os.getenv('ScalerName')

cluster_pick_path = os.path.join(model_directory, KMeansPick)
cluter_pick_model = load(cluster_pick_path)

cluster_drop_path = os.path.join(model_directory, KMeansDrop)
cluster_drop_model = load(cluster_drop_path)

model_path = os.path.join(model_directory, model_name)
model = load(model_path)

scaler_path = os.path.join(model_directory, scaler_name)
scaler = load(scaler_path)


def form(request):
    return render(request, 'index.html')



def result(request):
    
    jfk_distance = request.GET['jfk_distance']
    distance = request.GET['distance']
    month = request.GET['month']
    car_condition = request.GET['car_condition']
    day = request.GET['day']
    year = request.GET['year']
    month = request.GET['month']
    clusters = [0,1,2,3,4]
    cluster_pick = cluter_pick_model.predict([[request.GET['pickup_longitude'], request.GET['pickup_latitude']]])
    cluster_drop = cluster_drop_model.predict([[request.GET['dropoff_longitude'], request.GET['dropoff_latitude']]])
    car_cond = {
        'Excellent' : 3,
        'Very Good' : 2,
        'Good' : 1,
        'Bad' : 0
    }
    
    scaled_month = scaler.transform([[int(month)]])[0][0]
    
    data = []
    data.append(np.sqrt(float(jfk_distance)))
    data.append(np.sqrt(np.sqrt(float(distance))))
    data.append(int(day))
    data.append(int(year))
    data.append(np.sin(2 * np.pi * scaled_month / 12))
    data.append(car_cond[car_condition])
    data.extend([1 if cluster == cluster_pick else 0 for cluster in clusters])
    data.extend([1 if cluster == cluster_drop else 0 for cluster in clusters])
    print(data)
    
    value = round(model.predict([data])[0], 2)
    
    
    return render(request, 'result.html', {'value' : value})