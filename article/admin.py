from django.contrib import admin
from .models import Article
from .models import ArticleTagRelationship
from .models import ArticleClass
from .models import Tag
# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleTagRelationship)
admin.site.register(ArticleClass)
admin.site.register(Tag)