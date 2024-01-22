from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import show_predictions, load_week_data

urlpatterns = [
    path('', show_predictions, name='show_predictions'),
    path('load_week_data/<int:week>/', load_week_data, name='load_week_data'),
]
