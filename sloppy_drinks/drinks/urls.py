from django.urls import include, path
from drinks import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.drink_index, name='drink_index'),
    path('search/', views.drink_index_partial, name='drink_index_partial'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('<slug:slug>/', views.drink_detail, name='drink_detail'),
]