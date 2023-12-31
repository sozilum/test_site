from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (cookie_get, set_cookie, 
                    get_session, set_session, 
                    MyLogoutView, AboutMeView,
                    RegisterView, FooBarView,
                    UsersListView, HelloView)

app_name = 'authapp'

urlpatterns = [
    path('login/', 
        LoginView.as_view(template_name = 'myauthapp/login.html',
                        redirect_authenticated_user = True), 
                        name = 'login'),
    path('logout/',MyLogoutView.as_view(), name = 'logout'),
    path('hello/', HelloView.as_view(), name = 'hello'),
    
    path('cookie/get/', cookie_get, name = 'cookie-get'),
    path('cookie/set/', set_cookie, name = 'cookie-set'),

    path('session/get/', get_session, name = 'session-get'),
    path('session/set/', set_session, name = 'session-set'),

    path('users/', UsersListView.as_view(), name = 'users_list'),
    path('registration/', RegisterView.as_view(), name = 'register'),
    path('about_me/<int:pk>/', AboutMeView.as_view(), name = 'about_me'),

    path('foo-bar/', FooBarView.as_view(), name = 'foo-bar')
]