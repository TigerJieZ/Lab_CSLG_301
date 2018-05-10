from django.shortcuts import render
from django.views.generic import ListView
import markdown
from django.http import HttpResponse
from lab.models import Article
import os
import time

# Create your views here.


class IndexView(ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown.markdown(article.body,)
        return article_list


def uploadactcle(request):
    return render(request,'blog/upload.html')


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





