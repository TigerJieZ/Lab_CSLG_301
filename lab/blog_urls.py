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
<<<<<<< HEAD

    url('index.html',views.BlogIndexView.as_view()),

    url('upload',views.uploadactcle),
    url('result',views.uploadresult),

    url('', views.BlogIndexView.as_view())

=======
    url('index.html',views.BlogIndexView.as_view()),
    url('upload.html',views.uploadactcle),
    url('upload_result',views.uploadresult),
    url('', views.BlogIndexView.as_view())
>>>>>>> f2edd6f8d7bfdc594c5ff6786ce9ceef2540a80b
]