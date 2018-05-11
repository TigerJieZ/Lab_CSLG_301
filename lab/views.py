from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import ListView
import markdown
from django.http import HttpResponse
from lab.models import Article
import os
import time

# Create your views here.

# Create your views here.
from django.template import Context, RequestContext
from django.views.generic import ListView, View
import markdown
from lab.models import Article, Member


class BlogIndexView(ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
<<<<<<< HEAD
            article.body = markdown.markdown(article.body,)
=======
            article.body = markdown.markdown(article.body, )
>>>>>>> f2edd6f8d7bfdc594c5ff6786ce9ceef2540a80b
        return article_list


def uploadactcle(request):
    return render(request, 'blog/upload.html')


def uploadresult(request):
    message = "上传成功"
    if request.method == "POST":
        try:
            user_name = request.session["user_name"]
            title = request.POST['title']
            file = request.FILES.get("body")
            status = request.POST['status']
            abstract = request.POST['abstract']
            topped = request.POST['topped']

            if title != "" and not file and file.name.find(".md") == -1:
                message = "请选择正确的MarkDown文件"
                return render(request, "blog/result.html", {"message": message})
            else:
                # 文件写入本地
                path = "E:\\upload"
                if not os.path.isdir(path):
                    os.makedirs(path)
                destination = open(os.path.join(path, file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
                for chunk in file.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                # 信息写入数据库
                if topped == "on":
                    topped = True
<<<<<<< HEAD
                Member.objects.get(name=user_name).articles.create(title=title,
                                       body=path+file.name,
=======
                Article.objects.create(title=title,
                                       body=path + file.name,
>>>>>>> f2edd6f8d7bfdc594c5ff6786ce9ceef2540a80b
                                       created_time=time.time(),
                                       last_modified_time=time.time(),
                                       status=status,
                                       abstract=abstract,
                                       views=0,
                                       likes=0,
                                       topped=topped,)

                return render(request, "blog/result.html", {"message": message})

        except Exception as e:
            print(e)
            return HttpResponse('Some error happend ,please review')

<<<<<<< HEAD

def reeditacticle(request):
    title = "ttt"
    abstract = ""
    return render(request, 'blog/reedit.html', {"title": title, "abstract": abstract })


def reeditresult(request):
    print("")


=======
        article.body = markdown.markdown(article.body, )
    return article_list
>>>>>>> f2edd6f8d7bfdc594c5ff6786ce9ceef2540a80b


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
        member = Member.objects.get(email=email,password=password)
    except Exception as e:
        member = None

    if member is None:
        return login(request)
    else:
        # 登录成功将user_name存入上下文中
        request.session['user_name'] = member.name
        request.session['studentID']=member.studentID

        # 用户个人首页
        return memberIndexView(request)


# 用户个人首页
def memberIndexView(request):
    try:
        name = request.session['user_name']
        context = Context({'name': name})
        return render(request, 'member/index.html', context)
    except Exception as e:
        return render(request, 'member/index.html')




def register(request):
    return render(request, 'member/register.html')


def registerAction(request):
    # 读取表单输入的Email和Password
    post_data = dict(request.POST)
    name=post_data['InputName'][0]
    email=post_data['InputEmail'][0]
    password=post_data['InputPassword'][0]
    password2=post_data['InputPassword2'][0]
    studentID=post_data['InputStudentID'][0]
    gender=post_data['InputGender'][0]
    birthday=post_data['InputBirthday'][0]
    academy=post_data['InputAcademy'][0]
    profession=post_data['InputProfession'][0]

    if not password[0] == password2[0]:
        return register(request)

    Member.objects.create(name=name,email=email,password=password,
                          studentID=studentID,gender=gender,birthday=birthday,
                          academy=academy,profession=profession).save()

    request.session['user_name']=name
    request.session['studentID']=studentID
    return memberIndexView(request)
