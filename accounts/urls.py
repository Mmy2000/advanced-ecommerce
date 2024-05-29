from django.urls import path
from . import views
from. import api_view
urlpatterns = [
    path('' , views.profile , name="profile" ),
    path('register/' , views.register , name="register" ),
    path('login/' , views.login , name="login" ),
    path('logout/' , views.logout , name="logout" ),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('change_password/' , views.change_password , name='change_password'),
    path('profile/' , views.profile , name="profile" ),
    path('dashboard/' , views.dashboard , name="dashboard" ),
    path('orders/' , views.orders , name="orders" ),
    path('order_detail/<int:order_id>/' , views.order_detail , name="order_detail" ),
    path('favourite/' , views.favourite , name="favourite" ),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    #api 
    path('api/register/', api_view.register, name='api_register'),
    path('api/login/', api_view.LoginAPIView.as_view(), name='api_login'),
    path('api/forgot-password/', api_view.forgot_password_api, name='forgot-password-api'),
    path('api/reset-password/', api_view.reset_password_api, name='reset-password-api'),
    path('api/reset-password-validate/<uidb64>/<token>/', api_view.resetpassword_validate_api, name='resetpassword_validate_api'),
    path('api/change_password_api/', api_view.change_password_api, name='change_password_api'),
    path('api/profile/', api_view.ProfileAPIView.as_view(), name='profile-api'),
    path('api/profile/edit/', api_view.EditProfileAPIView.as_view(), name='edit-profile-api'),
    path('api/favourite/', api_view.FavouriteAPIView.as_view(), name='favourite-api'),
]
