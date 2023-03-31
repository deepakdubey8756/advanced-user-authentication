from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/password_confirm/<slug:token>', views.confirmPass, name='confirmPass'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('accounts/reset/', views.reset_view, name='reset'),
    path('accounts/resetconfirm/<slug:token>', views.reset_confirm, name='resetconfirm')
]
