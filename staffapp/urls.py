from django.urls import path

from staffapp.views import index

app_name = 'staffapp'

urlpatterns = [
    path('', index, name='index'),
    path('staff/<int:pk>', index, name='index')
]
