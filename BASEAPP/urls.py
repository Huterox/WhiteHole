
from django.conf.urls import url
from BASEAPP import views

urlpatterns = [
    url(r"^regirst/", views.regirst,name="regirst"),
    url(r"^verify/",views.verify,name="verify"),
    url(r"^get_code_img/",views.Get_code_img,name="get_code_img"),
    url(r"^login/",views.login,name="login"),
    url(r"^Mine/",views.Mine,name="Mine"),
    url(r"^userpic",views.userpicsave,name="userpic"),
    url(r"^submitinfo/",views.submitinfo,name="submitinfo"),
    url(r"^bloglist/",views.bloglist,name="bloglist"),
    url(r"^viewblog/",views.viewblog,name="viewblog"),
]
