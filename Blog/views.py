from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, Http404
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.urls import reverse
from BASEAPP.models import User
from Blog.models import Bolg,Comment
from Tools.TipsAlart import TipsAlert
import os
import  markdown
import time
import uuid


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@cache_page(60)
def Editor(request):
    #博客编辑
    usermsg = request.session.get("usermsg", None)
    if not usermsg:
        tips = "请先登录"
        request.session["tips"]=tips
        return redirect(reverse("index"))
    return render(request,"editor.html")


def Save(request):
    #博客保存
    if request.method == "POST":
        usermsg = request.session.get("usermsg", None)
        if not usermsg:
            return redirect(reverse("index"))
        usermsg = dict(usermsg)
        username = usermsg.get("username")
        password = usermsg.get("password")

        blogtitle=request.POST.get("blogname")
        blogbody = request.POST.get("blogbody")
        #直接在这里先把它转换为HTMl代码方便后面直接拿数据展示
        blogbody = markdown.markdown(blogbody,
                          extensions=[
                              'markdown.extensions.extra',
                              'markdown.extensions.codehilite',
                              'markdown.extensions.toc',
                          ])

        user = User.objects.filter(username=username).filter(password=password).first()
        blog = Bolg.objects.filter(blog_user=user).filter(title=blogtitle).first()
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if blog:
            blog.body = blogbody
            blog.date = time_now
            blog.save()
        else:
            blog = Bolg()
            blog.title = blogtitle
            blog.body = blogbody
            blog.blog_user = user
            blog.date = time_now
            blog.save()

    return TipsAlert(request,"editor.html","发布成功！")


@csrf_exempt
@xframe_options_sameorigin
def Upload(request):

    #博客图片的保存
    if request.method == "POST":
        if request.method == "POST":
            obj = request.FILES.get('editormd-image-file')

            file_name = time.strftime('%Y%m%d%H%M%S') + str(uuid.uuid1().hex) + '.' + obj.name.split('.')[
                -1]  # 图片文件名
            data_path = time.strftime('%Y%m')
            print(data_path)
            dir_path = os.path.join(BASE_DIR, 'static', 'upload', data_path)  # 保存的文件目录
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            img_path = os.path.join(dir_path, file_name)  # 存储的完整图片路径（绝对路径）
            f = open(img_path, 'wb')
            for chunk in obj.chunks():
                f.write(chunk)
            f.close()
            data = {"success": 1, "message": "上传成功", "url": '/static/upload/' + data_path + '/' + file_name}
            return JsonResponse(data)

        else:
            return JsonResponse({"success": 0, "message": "上传失败"})

@csrf_exempt
def comment(request):
    #想要评论就必须要登录，并且严格核实用户身份
    usermsg = request.session.get("usermsg", None)
    if not usermsg:
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    wirter = request.GET.get("wirter")
    title = request.GET.get("title")
    usermsg = dict(usermsg)
    comment_people_name = usermsg.get("username")
    comment_peple = User.objects.filter(username=comment_people_name).first()
    if not comment_peple:
        raise Http404("请别篡改参数，你将被纳入可疑名单")
    wirter_user = User.objects.filter(username=wirter).first()
    if not wirter_user:
        raise Http404("请别篡改参数，你将被纳入可疑名单")
    blog_c = wirter_user.bolg_set.filter(title=title).first()
    if not blog_c:
        raise Http404("请别篡改参数，你将被纳入可疑名单")
    comment_u = request.POST.get("comment")
    comment_c = Comment()
    comment_c.comment = comment_u
    comment_c.comment_user = comment_peple
    comment_c.comment_blog = blog_c
    comment_c.save()

    return redirect(reverse("Base:viewblog")+"?title="+title+"&username="+wirter+"&tips=Great")