from django.db.models.base import Model
from django.utils.safestring import SafeText
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import Article

class ArticlelistView(ListView):
    template_name = 'blogapp/article_list.html'
    model = Article
    context_object_name = 'article'
    queryset = (Article.objects.
                select_related('author').
                prefetch_related('tags').
                defer('content').filter(pub_date__isnull = False)
                .order_by('-pub_date'))


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blogapp/article_detail.html'


class LatestArticleFeed(Feed):
    title = 'Blog articles (latest)'
    description = 'Update on changes and addition blog articles'
    link = reverse_lazy('blogapp:articles')

    def items(self):
        return (
            Article.objects.
                select_related('author').
                prefetch_related('tags').
                defer('content').filter(pub_date__isnull = False)
                .order_by('-pub_date')[:5]
            )
    
    def item_title(self, item: Model) -> SafeText:
        return item.title

    def item_description(self, item: Model) -> str:
        return item.content[:50:]