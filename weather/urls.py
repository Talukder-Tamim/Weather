from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('/delete/<str:ct_name>', views.delete_state, name="delete-state")
]