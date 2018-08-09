"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from accounts import views as account_views
from django.contrib.auth import views as auth_views
from article import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', account_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^$', views.home, name='home'),
    path('private/', views.privateHome, name='private_home'),
    path('write_article/',views.createArticle, name='write_article'),
    path('write_markdown/', views.writeMakrdown, name='write_markdown'),
    path('article/<int:article_id>', views.viewMarkdown, name='view_markdown'),
    path('article/edit/<int:article_id>', views.editArticle, name='edit_markdown'),
    path('article/delete/<int:article_id>', views.deleteArticle, name='delete_article'),
    path('article/tag/create/', views.createArticleTag, name='create_article_tag'),
    path('article/class/create/', views.createArticleClass, name='create_article_class'),
    path('image/upload', views.uploadImage, name='upload_image'),

    re_path(r'^reset/$',
    auth_views.PasswordResetView.as_view(
    template_name='password_reset.html',
    email_template_name='password_reset_email.html',
    subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),

    re_path(r'^reset/done/$',
    auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
    name='password_reset_done'),

    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    name='password_reset_confirm'),

    re_path(r'^reset/complete/$',
    auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    name='password_reset_complete'),

    re_path(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),

    re_path(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
]
