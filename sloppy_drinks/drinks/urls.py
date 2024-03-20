from django.urls import path
from drinks import views

urlpatterns = [
    path('', views.drink_index, name='drink_index'),
    path('search/', views.drink_index_partial, name='drink_index_partial'),
    path("<slug:slug>/", views.drink_detail, name="drink_detail"),
]