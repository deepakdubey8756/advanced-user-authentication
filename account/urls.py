from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('password_confirm/<slug:token>', views.confirmPass, name='confirmPass'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('reset/', views.reset_view, name='reset'),
    path('resetconfirm/<slug:token>', views.reset_confirm, name='resetconfirm')
]
