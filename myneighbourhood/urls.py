from django.urls import path, include
from django.urls import re_path
from . import views
from django.conf import settings
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

urlpatterns=[
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('accounts/register/', RegistrationView.as_view(success_url='/profile'), name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('neighbourhood', views.neighbourhood, name='neighbourhood'),
    path('add-neighbourhood', views.addneighbourhood, name="addneighbourhood"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    re_path(r'^detail/(?P<neighbourhood_id>\d+)/$' , views.neighbourhood_details, name='detail' ),
    re_path(r'^new_business/(?P<pk>\d+)$',views.new_business,name='new_business'),
    re_path(r'^new_post/(?P<pk>\d+)$',views.new_post,name='new_post'),
    re_path(r'^search/',views.search_hoods,name='search_hoods'),
]