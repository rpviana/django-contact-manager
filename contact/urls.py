from django.urls import path
from contact import views
import forms

app_name = 'contact'

urlpatterns = [
    path('<int:contact_id>', views.contact, name='contact'),
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('create/', forms.create, name = "create"),
    path('<int:contact_id>/update', forms.update, name="update"),
    path('<int:contact_id>/delete', forms.delete, name="delete"),
    path('user/create', forms.register,name="register")
]
