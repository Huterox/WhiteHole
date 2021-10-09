from BASEAPP.models import User
from django.core.paginator import Paginator
def BloglistPageinator(request,usermsg,username,user_in=None):

    if user_in:
        user = user_in
    else:
        password = usermsg.get("password")
        user = User.objects.filter(username=username).filter(password=password).first()
    show = user.bolg_set.filter(blog_user=user).all().order_by("-id")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 8))
    paginator = Paginator(show, per_page)
    page_object = paginator.page(page)
    result = (page_object,paginator.page_range)
    return result