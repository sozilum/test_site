from django.urls import path
from .views import some_base_func, user_form, handle_upload_file

appname = 'requestrequestdataapp'

urlpatterns =[
    path('get/', some_base_func, name = 'get-view'),
    path('bio/', user_form, name = 'user-form'),
    path('upload/', handle_upload_file, name ='upload-file')
]