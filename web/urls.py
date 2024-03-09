from django.urls import path
from web.views import home_view, registration_view

urlpatterns = [
    path('', home_view, name='home'),
    path('sign_up', registration_view, name='sign_up'),
]