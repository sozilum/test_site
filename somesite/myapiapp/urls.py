from django.urls import path

from .views import (hello_world_api, GroupListView)

app_name = 'myapiapp'


urlpatterns = [
    path('hello/', hello_world_api, name = 'hellow_world'),
    path('groups/', GroupListView.as_view(), name = 'groups'),
]