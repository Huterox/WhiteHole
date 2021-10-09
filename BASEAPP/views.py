from django.core.paginator import Paginator
from django.http import HttpResponse,Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from Tools.Verify import *
from Tools.IsPassVerify import IsPassVerify
from Tools.IsPassVerifyPost import IsPassVerifyPost
from BASEAPP.models import User,UserPic
from Tools.TipsAlart import TipsAlert,TipsAlertData
from BASEAPP.froms import UserPicForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from Tools.Base.Mine.UserInfoDefault import UserinfoDeault
from Tools.Base.Mine.BloglistPaginator import BloglistPageinator
from Blog.models import Bolg

def index(request):

    try:
        usermsg  = request.session.get("usermsg",None)
        usermsg = dict(usermsg)

    except:
        usermsg = {
            "username": "",
            "userpic": "",
            "password":"",
        }
    picpath = usermsg.get("userpic")
    userpic = """ <a href="/Base/Mine/"><span  class="btn" style="border: none"><img src="%s" style="height: 60px;height: 60px;border-radius:30px;"></span></a>  """ % (
        picpath)
    userpic = mark_safe(userpic)

    data = {
        "userpic": userpic,
        "flag":request.session.get("flag")
    }

    Response = render(request, "index.html", context=data)
    tips = request.session.get("tips",None)
    if tips:
        Response.delete_cookie("tips")
        del request.session["tips"]
        return TipsAlert(request,"index.html",tips)

    return Response

def regirst(request):
    '''
    :param request:
    :return:
    这里的思路是当用户访问是先给定当前路径，然后跳转验证页面
    当验证页面通过后，在验证页面进行跳转回来
    '''
    if request.method == "GET":

        return IsPassVerify(request,"Regirst.html","Huterox","Base:regirst")

    if request.method == "POST":
        result = IsPassVerifyPost(request,"Regirst.html","Huterox","Base:regirst")
        if result[0]:

            try:
                username = request.POST.get("username")
                password = request.POST.get("password")
                useremail = request.POST.get("useremail")

            except:
                return redirect(reverse("Base:verify"))
            user = User()
            if(User.objects.filter(username=username).exists()):
                    return TipsAlert(request,"Regirst.html","用户名重复")
            else:
                user.username = username
                user.password = password
                user.useremail = useremail
                user.save()

            return redirect(reverse("index"))
        else:
            return result[1]


def verify(request):
    """

    :param request:
    :return:
    这部分是负责验证的
    """

    if request.method == "GET":

        return render(request,"verify.html")
    elif request.method == "POST":

        post_code = request.POST.get("Get_code")
        verify_code = request.session.get("verify_code")
        try:
            To_path = request.get_signed_cookie("To",salt="Huterox")
        except Exception as e:
            To_path = "index"
            return redirect(reverse("index"))
        if (post_code.lower() != verify_code.lower()):

            return render(request,"verify.html")

        request.session["verify_code_post"] = post_code
        return redirect(reverse(To_path))


def Get_code_img(request):
    code_img = Send_code_img(request)
    return HttpResponse(code_img, content_type='image/png')


def login(request):
    if request.method == "GET":
        return IsPassVerify(request, "login.html", "Huterox", "Base:login")
    if request.method == "POST":
        IsPassVerifyPost(request, "login.html", "Huterox", "Base:login")
        '''
        验证账户密码，成功后返回首页，首页显示头像链接
        
        '''
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")

        except:
            TipsAlert(request,"login.html","出现异常请重新进入登录页面！")

        user = User.objects.filter(username=username).filter(password=password).first()
        if user:
            # 现在的user系统做的差不多了头像功能ok
            try:
                userpic = user.userpic_set.all().last().userpic.url
            except:
                userpic = "/static/image/knowledge-1.jpg"
            # print(userpic)
            if not (userpic):
                userpic = "/static/image/knowledge-1.jpg"
            userpic = userpic.replace("media","static")
            usermsg = {

                "username": username,
                "userpic": userpic,
                "password": password,
                "userinfo":user.userinfo

            }

            '''
            这里搞一个安全加密扰乱，后面在Tools里面定义一个安全方法类，进行安全保护!
            对应的是安全加密识别，恶心ZZH！
            '''
            request.session["usermsg"] = usermsg

            return redirect(reverse("index"))

        else:
            return TipsAlert(request,"login.html","用户名或者密码不对")


def Mine(request):
    # 这里还有一个有个模板没有做
    usermsg = request.session.get("usermsg", None)
    wirter = request.GET.get("wirter",None) #查看作者

    if not usermsg:
        #本来是没有必要的，但是为了防止某些人抓包还是有必要的！
        #是否登录，并且在查看别的用户
        tips = "请先登录"
        request.session["tips"]=tips
        return redirect(reverse("index"))
    else:
        if usermsg:
            username = usermsg.get("username")
            usermsg = dict(usermsg)
            if not wirter:
                #显示默认信息
                return UserinfoDeault(request,usermsg,username)
            else:
                if username==wirter:
                    return UserinfoDeault(request, usermsg, username)
                else:
                    #已经登录查看的用户不是自己
                    user_wirter = User.objects.filter(username=wirter).first()
                    if user_wirter:
                        try:
                            userpic = user_wirter.userpic_set.all().last().userpic.url
                        except:
                            userpic = "/static/image/knowledge-1.jpg"
                        # print(userpic)
                        if not (userpic):
                            userpic = "/static/image/knowledge-1.jpg"
                        userpic = userpic.replace("media", "static")

                        data = {
                            'userpic':userpic,
                            'username':wirter,
                            'userinfo':user_wirter.userinfo
                        }
                        return render(request, "Mine_show.html", context=data)
                    else:
                        raise Http404("小伙子别乱改字段，你已被纳入可疑名单")
        else:
            #没有登录，但是有查询，为了反爬我决定还是做恶心一点必须登录
            tips = "请先登录"
            request.session["tips"] = tips
            return redirect(reverse("index"))


def bloglist(request):
    usermsg = request.session.get("usermsg", None)
    wirter = request.GET.get("wirter", None)  # 查看作者,当别的用户访问当前用户的时候需要的参数
    print(wirter)
    if not usermsg:
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    else:
        usermsg = dict(usermsg)
        if usermsg:

            username = usermsg.get("username")
            if not wirter:
                page_blog = BloglistPageinator(request,usermsg,username)
                data = {
                    'page_object': page_blog[0],
                    'page_range': page_blog[1],
                }
                return render(request, "Blogs_ifrom.html", context=data)
            else:

                if username==wirter:

                    page_blog = BloglistPageinator(request, usermsg, username)
                    data = {
                        'page_object': page_blog[0],
                        'page_range': page_blog[1],
                        'wirter': wirter
                    }

                    return render(request, "Blogs_ifrom.html", context=data)
                else:
                    user = User.objects.filter(username=wirter).first()
                    if user:
                        page_blog = BloglistPageinator(request, usermsg, username,user)
                        data = {
                            'page_object': page_blog[0],
                            'page_range': page_blog[1],
                            'wirter': wirter
                        }
                        return render(request, "Blogs_ifrom.html", context=data)
                    else:
                        raise Http404("小伙子别乱改字段，你已被纳入可疑名单")
        else:
            tips = "请先登录"
            request.session["tips"] = tips
            return redirect(reverse("index"))



def viewblog(request):
    #还是做的恶心一点不登陆不给看，并且防范恶意篡改
    usermsg = request.session.get("usermsg", None)
    blogtitle = request.GET.get("title")
    wirter = request.GET.get("username")

    if not usermsg:
        # 本来是没有必要的，但是为了防止某些人抓包还是有必要的！
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    else:
        usermsg = dict(usermsg)
        username = usermsg.get("username")
        if wirter:
            if username == wirter:
                user = User.objects.filter(username=username).first()
                blog  = user.bolg_set.filter(title=blogtitle).first()
                try:
                    comments = blog.comment_set.all()
                except Exception as e :
                    # print(e)
                    comments = None
                if not blog:
                    raise Http404("页面不存在")

                title = blog.title
                context = blog.body
                data = {
                    'title':title,
                    'blog':context,
                    'username':wirter,
                    'comments':comments,
                }
                tips  = request.GET.get("tips")

                if tips=="Great":
                    tips = "评论成功"
                    return TipsAlertData(request,"viewblog.html",tips,data)
                return render(request,"viewblog.html",context=data)
            else:
                user = User.objects.filter(username=wirter).first()
                if user:
                    blog = user.bolg_set.filter(title=blogtitle).first()
                    try:
                        comments = blog.comment_set.all()
                    except:
                        comments = None

                    if not blog:
                        raise Http404("页面不存在")

                    title = blog.title
                    context = blog.body
                    data = {
                        'title': title,
                        'blog': context,
                        'username': wirter,
                        'comments': comments,
                    }
                    tips = request.GET.get("tips")
                    if tips == "Great":
                        tips = "评论成功"
                        return TipsAlertData(request, "viewblog.html", tips, data)
                    return render(request, "viewblog.html", context=data)
        else:
            raise Http404("朋友别乱搞！")


@csrf_exempt
@xframe_options_sameorigin
def userpicsave(request):
    form = UserPicForm(request.POST, request.FILES)
    if form.is_valid():
        usermsg = request.session.get("usermsg", None)
        if not usermsg:
            return HttpResponse(" ")
        usermsg = dict(usermsg)
        username = usermsg.get("username")
        password = usermsg.get("password")
        userinfo = usermsg.get("userinfo")
        user = User.objects.filter(username=username).filter(password=password).first()
        user_pic = form.save(False)
        user_pic.pic_user = user
        user_pic.save()

        userpic = user.userpic_set.last().userpic.url
        userpic = userpic.replace("media", "static")
        #更新usermsg的信息
        usermsg = {
            'userpic': userpic,
            'username': username,
            "password": password,
            "userinfo":userinfo,
        }
        request.session["usermsg"] = usermsg
    else:
        return HttpResponse(" ")
        pass
        # print(form.errors.get_json_data())
    return redirect(reverse("Base:Mine"))

@csrf_exempt
def submitinfo(request):
    userinfo = request.POST.get("userinfo")
    usermsg = request.session.get("usermsg", None)
    if not usermsg:
        # 本来是没有必要的，但是为了防止某些人抓包还是有必要的！
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    username = usermsg.get("username")
    password = usermsg.get("password")
    user = User.objects.filter(username=username).filter(password=password).first()
    user.userinfo = userinfo
    try:
        userpic = user.userpic_set.last().userpic.url
        userpic = userpic.replace("media", "static")
    except:
        userpic = "/static/image/knowledge-1.jpg"
    user.save()
    usermsg = {
        'userpic': userpic,
        'username': username,
        "password": password,
        "userinfo": userinfo,
    }
    request.session["usermsg"] = usermsg
    return redirect(reverse("Base:Mine"))


