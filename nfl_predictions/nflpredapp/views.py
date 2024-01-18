from django.shortcuts import render
from .models import GameStats
from .resources.load_model import load_sklearn_model


def show_predictions(request):
    return render(request, 'nflpreds.html')


def prepare_data(game_stats):
    return [
        game_stats.ewma_dynamic_rush_off_home,
        game_stats.ewma_dynamic_pass_off_home,
        game_stats.ewma_dynamic_rush_def_home,
        game_stats.ewma_dynamic_pass_def_home,
        game_stats.ewma_dynamic_rush_off_away,
        game_stats.ewma_dynamic_pass_off_away,
        game_stats.ewma_dynamic_rush_def_away,
        game_stats.ewma_dynamic_pass_def_away,
    ]


def load_week_data(request, week):
    # Load the model
    model = load_sklearn_model(week)

    # Fetch the data for the selected week
    data = GameStats.objects.filter(week=week)

    # Process data through the model and collect predictions
    prepared_data = [prepare_data(item) for item in data]  
    predictions = model.predict(prepared_data)
    data_with_predictions = zip(data, predictions)

    # Pass the predictions to the template
    return render(request, 'week_data.html', {'data_with_predictions': data_with_predictions})