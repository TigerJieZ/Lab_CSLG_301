from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import time
from django.template import Context
from lab.models import Article, Member, Tag,Category,BlogComment,Suggest
from django.urls import reverse
import MySQLdb
import markdown as mk
import re




def index_view(request):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    return HttpResponseRedirect(
        reverse('blog_index', args=[1])
    )


def index_view_page(request,i):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    i=int(i)

    #按照最后一次的修改时间来排序
    articles = Article.objects.order_by("-last_modified_time").all()

    #根据页数i，一个html获取四个article，
    start = (i-1)*4
    end = i*4
    article_4 = articles[start:end]

    #获取总的文章数量
    numOfarticles = articles.__len__()

    #总页数
    pagenum = int(numOfarticles/4)+1
    prev = i-1
    next = i+1
    final = pagenum

    articles_rank1 = rank("-likes")
    articles_rank2 = rank("-views")

    return render(request, 'blog/blog_index.html', {"articles": article_4,
                                                    "prev": prev,
                                                    "next": next,
                                                    "final": final,
                                                    "articles_rank1": articles_rank1,
                                                    "articles_rank2": articles_rank2,
                                                    })


def user_index(request):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    return HttpResponseRedirect(
        reverse('blog_user_index', args=[1])
    )


def user_index_view(request,i):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    try:
        user_name = request.session['user_name']
        i = int(i)
        # 按照最后一次的修改时间来排序获取当前用户的文章
        articles = Article.objects.all().filter(member=Member.objects.get(name=user_name))

        #articles = Article.objects.all().order_by("-last_modified_time").filter(user_name=user_name)

        # 根据页数i，一个html获取四个article，
        start = (i - 1) * 4
        end = i * 4
        article_4 = articles[start:end]

        # 获取总的文章数量
        numOfarticles = articles.__len__()

        # 总页数
        pagenum = int(numOfarticles / 4) + 1

        prev = i - 1
        next = i + 1
        final = pagenum
        return render(request, "blog/blog_user_index.html",
                      {"articles": article_4,
                       "prev": prev,
                       "next": next,
                       "final": final,
                       })
    except Exception as e:
        return HttpResponse(e)



#condition (likes => 点赞量 views => 浏览量) (排序方式是从小到大，请加上“-”)
def rank(condition):
    articles = Article.objects.order_by(condition).all()
    article_4 = articles[0:4]
    return article_4


def upload_view(request):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    #更新页面
    category = Category.objects.all()
    articles_rank1 = rank("-likes")
    articles_rank2 = rank("-views")

    try:
        message = request.session["upload_error_message"]
        del request.session["upload_error_message"]
    except Exception as e:
        message=""

    tags =Tag.objects.all()
    return render(request, 'blog/blog_upload.html',{
        "category": category,
        "articles_rank1": articles_rank1,
        "articles_rank2": articles_rank2,
        "tags": tags,
        "message":message,
    })


def upload_action(request):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj
    if request.method == "POST":
        try:
            user_name = request.session["user_name"]
            title = request.POST['title']
            file = request.FILES.get("body")
            status = request.POST['status']
            abstract = request.POST['abstract']
            topped = request.POST['topped']
            category = request.POST['category']
            tags = request.POST.getlist(key="tags")

            if not file or file.name.find(".md") == -1:
                request.session["upload_error_message"]="请选择正确的markdown文件"
                return HttpResponseRedirect(
                    reverse('blog_upload')
                )
            else:

                #对正文进行格式转化,去掉转义字符，例如\r\n，这时就转化为str（\r\n）
                #body = MySQLdb.escape_string(file.read()).decode("utf-8")

                body = mk.markdown(file.read().decode("utf-8"))



                #如果简介为空，则取正文钱54个字
                if abstract == '' or len(abstract) == 0:
                    #abstract = body[0:54]
                    abstract = re.sub("<.*?>", "", body, 0)[0:54]

                # 判断是否置顶，格式转化
                if topped == "on":
                    topped = True
                else:
                    topped = False

                a=Article.objects.create(
                    title=title,
                    body=body,
                    created_time=time.time(),
                    last_modified_time=time.time(),
                    status=status,
                    abstract=abstract,
                    views=0,
                    likes=0,
                    topped=topped,
                    category=Category.objects.get(name=category),
                    member=Member.objects.get(name=user_name),

                )
                for tag in tags:
                    a.tags.add(Tag.objects.get(name=tag))

                articles_rank1 = rank("-likes")
                articles_rank2 = rank("-views")

                return render(request, "blog/blog_result.html",
                              {"message": "上传成功",
                               "articles_rank1": articles_rank1,
                               "articles_rank2": articles_rank2,
                               })

        except Exception as e:
            return HttpResponse(e)


def article_view(request):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj
    try:
        request.encoding = "utf-8"
        title = request.GET.get("title")
        last_modified_time = request.GET.get("last_modified_time")

        #the article must return just one!
        article = Article.objects.get(title=title,
                                      last_modified_time__contains=last_modified_time
                                      )

        #从mysql中取出的是str类型，我们用replace替换\r\n，注意要去掉转义
        #替换为\n后，在html界面可以用{{value|linebreaksbr}}过滤器，将value中的"\n"将被<br/>替代
        #这个<br>是适应html格式的，可以显示出效果，而不是单纯的文本
        #body = article.body.replace("\\r\\n","\n")
        body = article.body


        #取出评论
        #comment = BlogComment.objects.order_by("-created_time").get(article=article)
        comments = BlogComment.objects.all().order_by("-created_time").filter(article=article)

        # 更新rank
        category = Category.objects.all()
        articles_rank1 = rank("-likes")
        articles_rank2 = rank("-views")


        return render(request,"blog/blog_article.html",
                      {"article": article,
                       "body": body,
                       "comments": comments,
                       "articles_rank1": articles_rank1,
                       "articles_rank2": articles_rank2,
                       })
    except Exception as e:
        print(e)


def reedit_view(request):
    # 登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    try:
        request.encoding = "utf-8"
        title = request.GET.get("title")
        last_modified_time = request.GET.get("last_modified_time")

        # the article must return just one!
        article = Article.objects.get(title=title,
                                      last_modified_time__contains=last_modified_time
                                      )

        request.session['old_title'] = title
        request.session['old_modified_time'] = last_modified_time

        tags_checked = Tag.objects.all().filter(article=article)

        # 更新rank
        articles_rank1 = rank("-likes")
        articles_rank2 = rank("-views")

        category = Category.objects.all()
        tags = Tag.objects.all()

        return render(request, 'blog/blog_reedit.html', {
            "article": article,
            "category": category,
            "articles_rank1": articles_rank1,
            "articles_rank2": articles_rank2,
            "tags": tags,
            "tags_checked": tags_checked,
        })
    except Exception as e:
        print(e)


def reedit_view2(request):
    # 登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    try:
        print("in reedit_view2")
        title = request.session["old_title"]
        last_modified_time = request.session["old_modified_time"]
        message = request.session["reedit_error_message"]
        del request.session["reedit_error_message"]

        # the article must return just one!
        article = Article.objects.get(title=title,
                                      last_modified_time__contains=last_modified_time
                                      )

        tags_checked = Tag.objects.all().filter(article=article)

        # 更新rank
        articles_rank1 = rank("-likes")
        articles_rank2 = rank("-views")

        category = Category.objects.all()
        tags = Tag.objects.all()

        return render(request, 'blog/blog_reedit.html', {
            "article": article,
            "category": category,
            "articles_rank1": articles_rank1,
            "articles_rank2": articles_rank2,
            "tags": tags,
            "tags_checked": tags_checked,
            "message":message,
        })
    except Exception as e:
        print(e)


def reedit_action(request):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj
    if request.method == "POST":
        try:
            user_name = request.session["user_name"]
            title = request.POST['title']
            file = request.FILES.get("body")
            status = request.POST['status']
            abstract = request.POST['abstract']
            topped = request.POST['topped']
            category = request.POST['category']
            tags = request.POST.getlist(key="tags")

            old_title =request.session["old_title"]
            old_modified_time =request.session['old_modified_time']

            if not file or file.name.find(".md") == -1:
                request.session["reedit_error_message"] = "请选择正确的markdown文件"
                return HttpResponseRedirect(
                    reverse('blog_reedit2')
                )
            else:

                # 对正文进行格式转化,去掉转义字符，例如\r\n，这时就转化为str（\r\n）
                #body = MySQLdb.escape_string(file.read()).decode("utf-8")

                body = mk.markdown(file.read().decode("utf-8"))

                #如果简介为空，则取正文钱54个字
                if abstract == '' or len(abstract) == 0:
                    abstract = body[0:54]

                # 判断是否置顶，格式转化
                if topped == "on":
                    topped = True
                else:
                    topped = False

                # 信息写入数据库
                a = Article.objects.all().filter(title=old_title,last_modified_time__contains=old_modified_time)
                a_t = Article.objects.all().get(title=old_title,last_modified_time__contains=old_modified_time)
                a.update(
                    title=title,
                    body=body,
                    last_modified_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),
                    status=status,
                    abstract=abstract,
                    topped=topped,
                    category=Category.objects.get(name=category),
                    member=Member.objects.get(name=user_name),
                )

                del request.session['old_title']
                del request.session['old_modified_time']

                for tag in tags:
                    a_t.tags.add(Tag.objects.get(name=tag))

                articles_rank1 = rank("-likes")
                articles_rank2 = rank("-views")

                return render(request, "blog/blog_result.html",
                              {"message": "修改成功",
                               "articles_rank1": articles_rank1,
                               "articles_rank2": articles_rank2,
                               })

        except Exception as e:
            print(e)


def delete_action(request):
    # 登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj

    try:
        request.encoding = "utf-8"
        title = request.GET.get("title")
        last_modified_time = request.GET.get("last_modified_time")
        Article.objects.filter(title=title, last_modified_time__contains=last_modified_time).delete()
        return HttpResponseRedirect(
            reverse('blog_user_index',args=[1])
        )
    except Exception as e:
        print(e)



# 这个页面用来显示登录超时
def show_message(request):
    return render(request,"blog/message.html")


# 获取session中的user_name，如果为空则跳转到/member/login界面
def login_confirm(request):
    try:
        user_name = request.session['user_name']
    except KeyError as e:
        return HttpResponseRedirect("/member/login")


def suggest_view(request):
    # 登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj
    return render(request,"blog/blog_suggest.html")


def suggest_result(request):
    if request.method == "POST":
        try:
            suggest = request.POST["suggest"]
            Suggest.objects.create(suggest=suggest)
            return HttpResponseRedirect("/blog/index")

        except Exception as e:
            return HttpResponse(e)


def exit(request):
    # 登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj
    try:
        del request.session["user_name"]
        return HttpResponseRedirect("/member/login")
    except Exception as e:
        return HttpResponse(e)


def search(request):
    #登录核对
    renderObj = login_confirm(request)
    if renderObj != None:
        return renderObj
    try:
        keyword = request.POST['keyword']
        if keyword!="":
            request.session["keyword"]= keyword
    except Exception as e:
        return HttpResponse(e)
    return HttpResponseRedirect(
        reverse('blog_search', args=[1])
    )


def search_view(request,i):

    try:
        keyword = request.session['keyword']
        del request.session['keyword']
        # 按照最后一次的修改时间来排序获取当前用户的文章
        articles = Article.objects.filter(body__icontains=keyword)
        print(articles)

        # 根据页数i，一个html获取四个article，
        i = int(i)
        start = (i - 1) * 4
        end = i * 4
        article_4 = articles[start:end]

        # 获取总的文章数量
        numOfarticles = articles.__len__()

        # 总页数
        pagenum = int(numOfarticles / 4) + 1

        prev = i - 1
        next = i + 1
        final = pagenum
        return render(request, "blog/blog_search.html",
                      {"articles": article_4,
                       "prev": prev,
                       "next": next,
                       "final": final,
                       })
    except Exception as e:
        print(e)
        return HttpResponse(e)


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
        #return memberIndexView(request)
        return index_view(request)


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
