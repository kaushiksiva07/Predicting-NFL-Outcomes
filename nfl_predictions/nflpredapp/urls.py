from django.urls import path

from .views import show_predictions, load_week_data

urlpatterns = [
    path('', show_predictions, name='show_predictions'),
    path('load_week_data/<int:week>/', load_week_data, name='load_week_data'),
]
