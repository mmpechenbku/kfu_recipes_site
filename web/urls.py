from django.urls import path
from web.views import home_view, registration_view, auth_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('sign_up/', registration_view, name='sign_up'),
    path("sign_in/", auth_view, name="sign_in"),
    path("sign_out/", logout_view, name="sign_out"),
]