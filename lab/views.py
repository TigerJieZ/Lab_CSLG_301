from django.shortcuts import render

# Create your views here.
from django.template import Context
from django.views.generic import ListView, View
import markdown
from lab.models import Article, Member


class BlogIndexView(ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        """
        过滤数据，获取已发布文章列表，并转为html格式
        Returns:

        """
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown.markdown(article.body, )
        return article_list


def login(request):
    return render(request, 'member/login.html')


def loginAction(request):
    # 读取表单输入的Email和Password
    post_data = dict(request.POST)
    # 通过Key获取到的是list，[0]转换成字符串
    email = post_data['inputEmail'][0]
    password = post_data['inputPassword'][0]

    # 查询登录是否成功
    try:
        member = Member.objects.get(email=email, password=password)
    except Exception as e:
        member = None

    if member is None:
        return login(request)
    else:
        # 登录成功将user_name存入上下文中
        request.session['user_name'] = member.name
        # 用户个人首页
        return memberIndexView(request)


# 用户个人首页
def memberIndexView(request):
    name = request.session['user_name']
    context = Context({'name': name})

    return render(request, 'member/index.html', context)

def register(request):
    return render(request,'member/register.html')

def registerAction(request):
    return memberIndexView(request)
