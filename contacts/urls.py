from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('part_numberQuery', views.part_numberQuery, name='part_numberQuery'),
]