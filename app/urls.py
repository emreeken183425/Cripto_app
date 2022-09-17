from django.urls import path
from .views import home,delete_coin


urlpatterns = [
    path('',home,name='home'),
    path('delete/<int:id>',delete_coin,name="delete")
]