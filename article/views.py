from django.shortcuts import render

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Article
from .models import ArticleTagRelationship
from .models import Tag
from .models import ArticleClass
import json
import sys
import os
from .forms import ArticleForm

def get_all_tags():
    '''
    获取当前所有可用的标签
    :return: list
    '''
    articleTags = Tag.objects.all()
    tag_arr = []
    for tag in articleTags:
        temp_dict = {
            'id': tag.id,
            'name': tag.tag_name
        }
        tag_arr.append(temp_dict)
    return tag_arr

def get_all_class():
    '''
    获取当前所有的类别
    :return: list
    '''
    articleClasses = ArticleClass.objects.all()
    resultArr = []
    for c in articleClasses:
        resultArr.append({
            'id': c.id,
            'class': c.class_name
        })
    return resultArr

def get_article_tags(article_id):
    '''
    获取某个文章的所有标签
    :param article_id: 文章ID
    :return:
    '''
    article_tags = ArticleTagRelationship.objects.filter(article_id=article_id)
    resultArr = []
    for t in article_tags:
        temp_dict = {}
        temp_dict['id']=t.tag_id.id
        temp_dict['name']=t.tag_id.tag_name
        resultArr.append(temp_dict)
    return resultArr


def home(request):
    article_arr = []
    articles = Article.objects.all()
    for article in articles:
        article_info = {
            'id': article.id,
            'title': article.title,
            'date': article.date,
            'username': article.username
        }
        article_class = ArticleClass.objects.get(id=article.class_id.id)
        tags_id = ArticleTagRelationship.objects.filter(article_id=article.id)
        tags = Tag.objects.filter(tag_id__in=tags_id)
        tags_name = list(map(lambda t: t.tag_name, tags))
        article_info['class'] = article_class.class_name
        article_info['tags'] = tags_name

        article_arr.append(article_info)

        # print(request.user) # 可以访问已登录用户
    template_data = {'articles': article_arr}
    if request.user == 'admin':
        template_data['admin'] = True
    # return HttpResponse(json.dumps(article_arr), content_type="application/json")
    return render(request, 'home.html', template_data)

@login_required
def privateHome(request):
    article_arr = []
    #articles = Article.objects.all()
    if request.user.username == 'admin':
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(username=request.user)
    for article in articles:
        article_info = {
            'id':article.id,
            'title': article.title,
            'date': article.date,
            'username':article.username
        }
        article_class = ArticleClass.objects.get(id=article.class_id.id)
        tags_id = ArticleTagRelationship.objects.filter(article_id=article.id)
        tags = Tag.objects.filter(tag_id__in=tags_id)
        tags_name = list(map(lambda t: t.tag_name, tags))
        article_info['class'] = article_class.class_name
        article_info['tags'] = tags_name

        article_arr.append(article_info)

        #print(request.user) # 可以访问已登录用户
    template_data = {'articles':article_arr}
    if request.user == 'admin':
        template_data['admin'] = True
    #return HttpResponse(json.dumps(article_arr), content_type="application/json")
    return render(request, 'article_home.html', template_data)

def createArticle(request):
    if request.method == 'POST':
        print(json.loads(request.body))
        return HttpResponse('ok',content_type="application/json")
    else:
        articleForm = ArticleForm()
        return render(request, 'article_form.html', {'form':articleForm})

@login_required
def writeMakrdown(request):
    if request.method == 'POST':
        markdown_info = json.loads(request.body)
        article_id = markdown_info.get('article_id')
        if article_id is not None:
            article = Article.objects.get(id=article_id)
            if article is None:
                raise Http404
            username = article.username
        else:
            username = request.user.username
            article = Article()
        article.title = markdown_info['title']
        article.content = markdown_info['markdown_html']
        article.origin_md = markdown_info['markdown_md']
        article.class_id = ArticleClass.objects.get(id=markdown_info['class_id'])
        article.username = username
        article.save()

        # 为文章的每个标签在 标签-文章 关联表中增加一条记录
        tags_id = markdown_info.get('tags')
        if tags_id is not None:
            for tag_id in tags_id:
                tag_article_relation = ArticleTagRelationship()
                cur_tag = Tag.objects.get(id=int(tag_id))
                if cur_tag is None:
                    continue
                tag_article_relation.tag_id = cur_tag
                tag_article_relation.article_id = article
                tag_article_relation.save()

        return HttpResponse('ok')
    else:
        resultDict = {
            'class_data': get_all_class(),
            'tags': get_all_tags()
        }
        return render(request, 'markdown_edit.html', resultDict)

def viewMarkdown(request, article_id):
    article = Article.objects.get(id=article_id)
    if article is None:
        raise Http404
    content = article.content
    content = content.replace('\n','')
    article_info = {
        'article_markdown_content':content,
        'origin_markdown_content':article.origin_md,
        'article_title':article.title,
        'article_id':article.id,
        'username':article.username
    }
    return render(request, 'article_read.html', article_info)

@login_required
def editArticle(request, article_id):
    article = Article.objects.get(id=article_id)
    if article is None:
        raise Http404
    content = article.content
    content = content.replace('\n', '')


    data = {
        'article_markdown_content': content,
        'origin_markdown_content': article.origin_md,
        'article_title': article.title,
        'article_id': article.id,
        'class_data': get_all_class(),
        'article_tags': get_article_tags(article.id),
        'tags': get_all_tags()
    }
    return render(request, 'markdown_edit.html', data)

@login_required
def deleteArticle(request, article_id):
    Article.objects.filter(id=article_id).delete()
    return HttpResponse('ok')

@login_required
def createArticleTag(request):
    tag_info = json.loads(request.body)
    tag_name = tag_info.get('tag_name')
    tag = Tag()
    tag.tag_name = tag_name
    tag.save()
    tag_arr = Tag.objects.all()

    result = {
        'tag_data':[{'id':tag.id,'name':tag.tag_name} for tag in tag_arr]
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def createArticleClass(request):
    class_info = json.loads(request.body)
    class_name = class_info.get('class_name')
    articleClass = ArticleClass()
    articleClass.class_name = class_name
    articleClass.save()

    result = {
        'class_data':get_all_class()
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

def uploadImage(request):
    image = request.FILES.get('editormd-image-file')
    imagepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploadImage')
    with open(os.path.join(imagepath, image.name), 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)

    result = {
        "success" : 1, #0表示上传失败;1表示上传成功
        "message" : "success",
        "url"     : "http://localhost:8000/static/uploadImage/" + image.name
    }
    return HttpResponse(json.dumps(result), content_type="application/json")