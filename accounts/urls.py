from django.urls import path
from . import views
urlpatterns = [
    path('' , views.profile , name="profile" ),
    path('register/' , views.register , name="register" ),
    path('login/' , views.login , name="login" ),
    path('logout/' , views.logout , name="logout" ),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('profile/' , views.profile , name="profile" ),
    path('dashboard/' , views.dashboard , name="dashboard" ),
    path('favourite/' , views.favourite , name="favourite" ),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
