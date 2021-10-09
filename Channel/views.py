from django.core.paginator import Paginator
from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from Tools.TipsAlart import TipsAlert,TipsAlertData
from Tools.Useridentifiy import IdentifyUser
from BASEAPP.models import User
from Channel.models import Channel
# Create your views here.
from django.urls import reverse
from Tools.Channel.ChannelList.ChannelPageinator import ChannelPageinator

@csrf_exempt
def create(request):
    if request.method == "GET":
        #检验是否登录
        islog = IdentifyUser.IsLogin(request)
        if not islog[0]:
            return islog[1]
        else:
            return render(request,"channelifrom.html")
    if request.method == "POST":
        islog = IdentifyUser.IsLogin(request)
        if not islog[0]:
            return islog[1]
        usermsg = islog[1]
        usermsg = dict(usermsg)
        username = usermsg.get("username")
        password = usermsg.get("password")
        channel_name = request.POST.get("name")
        channel_desc = request.POST.get("desc")
        user = User.objects.filter(username=username).filter(password=password).first()
        channel = Channel.objects.filter(channel_user=user).filter(channel_name=channel_name).first()
        if channel:
            channel.channel_desc = channel_desc
            channel.save()
        else:
            channel = Channel()
            channel.channel_name = channel_name
            channel.channel_desc = channel_desc
            channel.channel_user = user
            channel.save()
        return HttpResponse("创建成功")


def channellist(request):
    usermsg = request.session.get("usermsg", None)
    wirter = request.GET.get("wirter", None)
    if not usermsg:
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    else:
        if usermsg:
            usermsg = dict(usermsg)
            username = usermsg.get("username")
            if not wirter:
                page_channel_blog = ChannelPageinator(request,usermsg,username)

                data = {
                    'page_object': page_channel_blog[0],
                    'page_range': page_channel_blog[1],
                    'wirter':wirter,
                }
                return render(request, "Channelslist.html", context=data)
            else:
                if username == wirter:
                    page_channel_blog = ChannelPageinator(request, usermsg, username)

                    data = {
                        'page_object': page_channel_blog[0],
                        'page_range': page_channel_blog[1],
                        'wirter': wirter,
                    }
                    return render(request, "Channelslist.html", context=data)
                else:

                    page_channel_blog = ChannelPageinator(request, usermsg,wirter,1)

                    data = {
                        'page_object': page_channel_blog[0],
                        'page_range': page_channel_blog[1],
                        'wirter': wirter,
                    }
                    return render(request, "Channelslist.html", context=data)
        else:
            tips = "请先登录"
            request.session["tips"] = tips
            return redirect(reverse("index"))


def viewchannel(request):
    channel_name = request.GET.get("channel_name")
    channel_wirter = request.GET.get("channel_wirter")
    channel_wirter = User.objects.filter(username=channel_wirter).first()
    if channel_wirter:
        channel = channel_wirter.channel_set.filter(channel_name=channel_name).first()
        if not channel:
            raise HttpResponse("该频道不存在！请不要篡改参数！")
        try:
            userpic = channel_wirter.userpic_set.last().userpic.url
        except:
            userpic = "/static/image/knowledge-1.jpg"
        try:
            blogs = channel.channel_blog.all().order_by("-id")
        except:
            blogs=None
        if not (userpic):
            userpic = "/static/image/knowledge-1.jpg"
        userpic = userpic.replace("media", "static")

        data={
            "wirter":channel_wirter.username,
            "userpic":userpic,
            "channelblogs":blogs,
            "channelname":channel_name,
        }

        return render(request,"viewchannel.html",context=data)
    else:
        raise Http404("请不要篡改参数!")


def bloglist(request):
    #展示博客列表
    usermsg = request.session.get("usermsg", None)
    wirter = request.GET.get("wirter", None)  # 查看作者
    channelname = request.GET.get("channelname")
    if not usermsg and not wirter:
        # 本来是没有必要的，但是为了防止某些人抓包还是有必要的！
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    else:
        if usermsg:
            usermsg = dict(usermsg)
            username = usermsg.get("username")
            if not wirter:

                raise Http404("朋友别乱搞！")
            else:
                if username == wirter:
                    password = usermsg.get("password")
                    user = User.objects.filter(username=username).filter(password=password).first()
                    #在这个系统里面不存在用户名和密码一样的用户，用这种方式查询如果有结果那就是同一个用户，也就是
                    #修改频道的就是频道所有者。
                    if user:
                        show_channel = user.bolg_set.filter(blog_user=user).all().order_by("-id")
                        page = int(request.GET.get("page", 1))
                        per_page = int(request.GET.get("per_page",5))
                        paginator = Paginator(show_channel, per_page)
                        page_object = paginator.page(page)
                        data = {
                            'page_object': page_object,
                            'page_range': paginator.page_range,
                            'channelname':channelname,
                            'wirter':wirter,
                        }
                        tips = request.GET.get("tips")
                        if tips=="Great":
                            return TipsAlertData(request,"channelifromlist.html","添加成功",data)

                        return render(request, "channelifromlist.html", context=data)
                    else:
                        return render(request, "NoPower.html")
                else:

                    return render(request, "NoPower.html")
        else:
            tips = "请先登录"
            request.session["tips"] = tips
            return redirect(reverse("index"))


def addblog(request):
    # 这部分的验证方式和先前显示那个博客的验证方式一样
    usermsg = request.session.get("usermsg", None)
    blogname = request.GET.get("title")
    wirter = request.GET.get("username")
    channelname = request.GET.get("channelname")
    if not usermsg:
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    else:
        usermsg = dict(usermsg)
        username = usermsg.get("username")
        if username == wirter:
            user = User.objects.filter(username=username).first()
            #与博客一样同一个用户的频道名字不会重复
            channel = user.channel_set.filter(channel_name=channelname).first()
            blog = user.bolg_set.filter(title=blogname).first()
            if channel and blog:
                # 正常情况下这两个东西是可以对的上的，但是一旦出现恶意篡改就不可能对的上
                channel.channel_blog.add(blog)
                channel.save()
                tips="Great"
                return redirect(reverse("Channel:bloglist")+"?channelname="+channelname
                                +"&wirter="+wirter+"&tips="+tips)
            else:
                raise Http404("请不要篡改参数")
        else:
            raise Http404("当前用户没有权限")


def bloglistremove(request):
    usermsg = request.session.get("usermsg", None)
    wirter = request.GET.get("wirter", None)  # 查看作者
    channelname = request.GET.get("channelname")
    if not usermsg and not wirter:
        # 本来是没有必要的，但是为了防止某些人抓包还是有必要的！
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    else:
        if usermsg:
            usermsg = dict(usermsg)
            username = usermsg.get("username")
            if not wirter:

                raise Http404("朋友别乱搞！")
            else:
                if username == wirter:
                    password = usermsg.get("password")
                    user = User.objects.filter(username=username).filter(password=password).first()
                    #在这个系统里面不存在用户名和密码一样的用户，用这种方式查询如果有结果那就是同一个用户，也就是
                    #修改频道的就是频道所有者。
                    if user:
                        show_channel = user.bolg_set.filter(blog_user=user).all().order_by("-id")
                        page = int(request.GET.get("page", 1))
                        per_page = int(request.GET.get("per_page",5))
                        paginator = Paginator(show_channel, per_page)
                        page_object = paginator.page(page)
                        data = {
                            'page_object': page_object,
                            'page_range': paginator.page_range,
                            'channelname':channelname,
                            'wirter':wirter,
                        }
                        tips = request.GET.get("tips")
                        if tips=="Great":
                            return TipsAlertData(request,"channelifomlistdel.html","移除成功",data)

                        return render(request, "channelifomlistdel.html", context=data)
                    else:
                        return render(request,"NoPower.html")
                else:

                    return render(request, "NoPower.html")
        else:
            tips = "请先登录"
            request.session["tips"] = tips
            return redirect(reverse("index"))



def removeblog(request):
    usermsg = request.session.get("usermsg", None)
    blogname = request.GET.get("title")
    wirter = request.GET.get("username")
    channelname = request.GET.get("channelname")
    if not usermsg:
        tips = "请先登录"
        request.session["tips"] = tips
        return redirect(reverse("index"))
    else:
        usermsg = dict(usermsg)
        username = usermsg.get("username")
        if username == wirter:
            user = User.objects.filter(username=username).first()
            #与博客一样同一个用户的频道名字不会重复
            channel = user.channel_set.filter(channel_name=channelname).first()
            blog = user.bolg_set.filter(title=blogname).first()
            if channel and blog:
                # 正常情况下这两个东西是可以对的上的，但是一旦出现恶意篡改就不可能对的上
                channel.channel_blog.remove(blog)
                channel.save()
                tips="Great"
                return redirect(reverse("Channel:bloglistremove")+"?channelname="+channelname
                                +"&wirter="+wirter+"&tips="+tips)
            else:
                raise Http404("请不要篡改参数")
        else:
            raise Http404("当前用户没有权限")


def indexchannellist(request):
    channels = Channel.objects.all().order_by("-id")
    # 访问频道详情需要的参数如下 channel_name channel_wirter
    #分页器干活

    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page",6))
    paginator = Paginator(channels, per_page)
    page_object = paginator.page(page)
    data = {
        'page_object': page_object,
        'page_range': paginator.page_range,
    }

    return render(request,"IndexChannelList.html",context=data)

@csrf_exempt
def indexchannelsearch(request):

    if request.method=="GET":
        flag = request.session.get("flag")
        if not flag:
            return  render(request,"channelsearchget.html")
        else:
            request.session["flag"]=""
            channels = Channel.objects.filter(channel_name__istartswith=flag).all()
            page = int(request.GET.get("page", 1))
            per_page = int(request.GET.get("per_page",3))
            paginator = Paginator(channels, per_page)
            page_object = paginator.page(page)
            data = {
                'page_object': page_object,
                'page_range': paginator.page_range,
            }

            return render(request, "IndexChannelList.html", context=data)

    if request.method == "POST":
        usermsg = request.session.get("usermsg", None)
        if not usermsg:
            request.session['tips']="请先登录"
            return redirect(reverse("index"))

        parmes = request.POST.get("search")
        print(parmes)
        request.session["flag"]=parmes
        return redirect(reverse("index")+"?flag="+parmes)