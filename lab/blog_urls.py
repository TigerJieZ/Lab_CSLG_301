"""Lab_CSLG_301 URL Configuration

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
from django.conf.urls import url
from lab import views

urlpatterns = [

    url(r'^index$', views.index_view,),
    url(r'^index/(\d+)$', views.index_view_page,name= "blog_index"),

    url(r'^user_index$', views.user_index),
    url(r'^user_index/(\d+)$', views.user_index_view,name= "blog_user_index"),

    url(r'^article$', views.article_view),

    url(r'^upload$', views.upload_view),
    url(r'^upload_result$', views.upload_action),

    url(r'^reedit$', views.reedit_view),
    url(r'^reedit_result$', views.reedit_action),

    url(r'^message$', views.show_message),

]