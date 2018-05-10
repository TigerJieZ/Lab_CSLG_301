from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
import markdown
from lab.models import Article


class IndexView(ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        """
        过滤数据，获取已发布文章列表，并转为html格式
        Returns:

        """
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown.markdown(article.body,)
        return article_list