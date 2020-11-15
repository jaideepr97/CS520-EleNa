from django.urls import path
from .views import get_input_form

urlpatterns = [
    path('', get_input_form)
]
