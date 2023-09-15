from django.urls import path
from .views import ArticlelistView

app_name = 'blogapp'

urlpatterns = [
    path('', ArticlelistView.as_view(), name = 'list'),
]