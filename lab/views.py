from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import time
from django.template import Context, RequestContext
from django.views.generic import ListView, View
import markdown
from lab.models import Article, Member
from django.core.urlresolvers import reverse


def index_view(request):
    return HttpResponseRedirect(
        reverse('blog_index', args=[1])
    )


def index_view_page(request,i):
    i=int(i)

    #按照最后一次的修改时间来排序
    articles = Article.objects.order_by("last_modified_time").all()

    #根据页数i，一个html获取四个article，
    start = (i-1)*4
    end = i*4
    article_4 = articles[start:end]

    #获取总的文章数量
    numOfarticles = articles.__len__()

    #总页数
    pagenum = int(numOfarticles/4)+1
    if i < pagenum:
        pages = [-1,i+1,i+2,i+3]
    else:
        pages = [pagenum-3,pagenum-2,pagenum-1,-1]
    prev = i-1
    next = i+1
    final = pagenum

    articles_rank1 = rank("-likes")
    articles_rank2 = rank("-views")

    return render(request, 'blog/blog_index.html', {"articles": article_4,
                                                    "pages": pages,
                                                    "prev": prev,
                                                    "next": next,
                                                    "final": final,
                                                    "articles_rank1": articles_rank1,
                                                    "articles_rank2": articles_rank2,
                                                    })


#condition (likes => 点赞量 views => 浏览量) (排序方式是从小到大，请加上“-”)
def rank(condition):
    articles = Article.objects.order_by(condition).all()
    article_4 = articles[0:4]
    return article_4


def upload_view(request):
    articles_rank1 = rank("-likes")
    articles_rank2 = rank("-views")
    return render(request, 'blog/blog_upload.html',{
        "articles_rank1": articles_rank1,
        "articles_rank2": articles_rank2,
    })


def upload_action(request):
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

                body = ""
                for line in file:
                    line = str(line.decode("utf-8"))
                    line = line.split("\r")
                    for listitem in line:
                        body += str(listitem).split('\r\n')[0]

                if abstract == '' or len(abstract) == 0:
                    abstract = body[0:54]

                # 信息写入数据库
                if topped == "on":
                    topped = True
                Member.objects.get(name=user_name).articles.create(title=title,
                                       body=body,
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
