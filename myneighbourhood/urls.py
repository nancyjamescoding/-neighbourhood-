from django.urls import path, include
from django.urls import re_path
from . import views
from django.conf import settings
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth.views import LogoutView
from .views import (
    NeighbourhoodListView,
    profile,
    addneighbourhood,
    home,
)
from django.conf.urls.static import static

urlpatterns=[
    path('', home, name='home'),
    path('profile', profile, name = 'profile'),
    path('neighbourhoods', NeighbourhoodListView.as_view(), name = 'neighbourhoods'),
    path('add-neighbourhood', addneighbourhood, name="add-neighbourhood"),
    path('accounts/register/', RegistrationView.as_view(success_url='/neighbourhoods'), name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]