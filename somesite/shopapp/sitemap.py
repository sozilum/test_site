from django.contrib.sitemaps import Sitemap

from .models import Product

class ShopSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def item(self):
        return (
            Product.objects.
            select_related('user').
            filter(archived = False).
            order_by('-created_at')[:1:]
        )

    def lastmode(self, obj:Product):
        return obj.pk