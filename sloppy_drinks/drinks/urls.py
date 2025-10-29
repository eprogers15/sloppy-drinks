from django.urls import include, path
from django.contrib.auth import views as auth_views
from drinks import views
from drinks.forms import CustomLoginForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(
        authentication_form=CustomLoginForm
    ), name='login'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm
    ), name='password_reset'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        form_class=CustomPasswordChangeForm
    ), name='password_change'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.drink_index, name='drink_index'),
    path('search/', views.drink_index_partial, name='drink_index_partial'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('<slug:slug>/', views.drink_detail, name='drink_detail'),
]