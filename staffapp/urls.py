from django.urls import path

from staffapp.views import index, staff_details

app_name = 'staffapp'

urlpatterns = [
    path('', index, name='index'),
    path('staff/<int:pk>', staff_details, name='staff_info')
]
