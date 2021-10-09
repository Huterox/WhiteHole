from django.shortcuts import render,redirect
from django.urls import reverse
def IsLogin(request):
    #如果没登录返回0和跳转，反正返回（1，usermsg）
    usermsg = request.session.get("usermsg", None)
    if not usermsg:
        tips = "请先登录"
        request.session["tips"] = tips
        return (0,redirect(reverse("index")))
    else:
        return (1,usermsg)