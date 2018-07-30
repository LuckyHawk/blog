from django.db import models
from django.utils import timezone


class ArticleClass(models.Model):

    class_name = models.CharField(max_length=32, unique=True)

    def __repr__(self):
        return self.class_name

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    date = models.DateTimeField(auto_now_add=True)#auto_now_add=True, default=timezone.now
    update = models.DateTimeField(auto_now=True)
    content = models.TextField()
    origin_md = models.TextField()
    class_id = models.ForeignKey(ArticleClass, null=True, on_delete=models.SET_NULL,related_name='article_class')

    def __repr__(self):
        return self.title


class Tag(models.Model):

    tag_name = models.CharField(max_length=32, unique=True)

    def __repr__(self):
        return self.tag_name



class ArticleTagRelationship(models.Model):

    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_id')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_id')