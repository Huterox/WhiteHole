from django.shortcuts import render
def UserinfoDeault(request,usermsg,username):
    # 自己登录查看
    picpath = usermsg.get("userpic")
    userinfo = usermsg.get("userinfo")
    if not userinfo:
        userinfo = "貌似什么也没写......"
    data = {
        'userpic': picpath,
        'username': username,
        'userinfo': userinfo
    }
    return render(request, "Mine.html", context=data)