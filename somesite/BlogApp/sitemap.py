from django.contrib.sitemaps import Sitemap

from .models import Article


class BlogSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def item(self):
        return (Article.objects.
                select_related('author').
                prefetch_related('tags').
                defer('content').filter(pub_date__isnull = False)
                .order_by('-pub_date'))
    
    def lastmode(self, obj:Article):
        return obj.pk