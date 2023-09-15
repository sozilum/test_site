from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article

class ArticlelistView(ListView):
    template_name = 'blogapp/article_list.html'
    model = Article
    context_object_name = 'article'
    queryset = (Article.objects.
                select_related('author').
                prefetch_related('tags').
                defer('content'))