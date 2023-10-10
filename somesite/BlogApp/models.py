from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=40)


class Tag(models.Model):
    name = models.CharField(max_length=20)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete= models.CASCADE)
    categoty = models.ForeignKey(Category, on_delete= models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def get_absolut_url(self):
        return reverse('blogapp:article', kwargs={'pk':self.pk})