import joblib
from django.conf import settings
import os

def load_sklearn_model(week):
    # Local Path
    # model_path = os.path.join('C:\\Users\\Kaushik\\NFLWebApp', 'nfl_predictions', 'nflpredapp', 'resources', f'model_week{week}.pkl') 
    # Production Path
    model_path = os.path.join('nflpredapp', 'resources', f'model_week{week}.pkl')
    with open(model_path, 'rb') as file:
        model = joblib.load(file)
    return model