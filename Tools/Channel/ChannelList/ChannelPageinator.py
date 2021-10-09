from BASEAPP.models import User
from django.core.paginator import Paginator
def ChannelPageinator(request,usermsg,username,parmer = None):

    if parmer:
        user = User.objects.filter(username=username).first()
    else:
        password = usermsg.get("password")
        user = User.objects.filter(username=username).filter(password=password).first()
    show = user.channel_set.filter(channel_user=user).all().order_by("-id")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page",5))
    paginator = Paginator(show, per_page)
    page_object = paginator.page(page)
    result = (page_object,paginator.page_range)
    return result