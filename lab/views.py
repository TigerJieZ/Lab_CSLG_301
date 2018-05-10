from django.shortcuts import render
<<<<<<< HEAD
from django.shortcuts import render_to_response
from django.views.generic import ListView
import markdown
from django.http import HttpResponse
from lab.models import Article
import os
import time

# Create your views here.
=======

# Create your views here.
from django.template import Context
from django.views.generic import ListView, View
import markdown
from lab.models import Article, Member
>>>>>>> master


class BlogIndexView(ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
<<<<<<< HEAD
            article.body = markdown.markdown(article.body,)
        return article_list


def uploadactcle(request):
    return render(request, 'blog/upload.html')


def uploadresult(request):
    message = "erqerqreq"
    if request.method == "POST":
        try:
            title = request.POST['title']
            file = request.FILES.get("body")
            status = request.POST['status']
            abstract = request.POST['abstract']
            topped = request.POST['topped']

            if title != "" and not file and file.name.find(".md") == -1:
                message = "请选择正确的MarkDown文件"
                return render(request, "blog/upload_result.html", {"message": message})
            else:
                #文件写入本地
                path="E:\\upload"
                if not os.path.isdir(path):
                    os.makedirs(path)
                destination = open(os.path.join(path, file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
                for chunk in file.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                #信息写入数据库
                if topped == "on":
                    topped = True
                Article.objects.create(title=title,
                                       body=path+file.name,
                                       created_time=time.time(),
                                       last_modified_time=time.time(),
                                       status=status,
                                       abstract=abstract,
                                       views=0,
                                       likes=0,
                                       topped=topped,
                                       category_id=1
                                       )
                return render(request, "blog/upload_result.html", {"message": message})

        except Exception as e:
            print(e)
            return HttpResponse('Some error happend ,please review')





=======
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
>>>>>>> master
