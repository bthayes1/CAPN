from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product_mnt_create', views.Product_mntCreateView.as_view(), name='product_mnt_create'),
    path('contact_mnt_create', views.Contact_mntCreateView.as_view(), name='contact_mnt_create'),
    path('part_numberQuery', views.part_numberQuery, name='part_numberQuery'),
]