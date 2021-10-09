from django.conf.urls import url
from Channel import views

urlpatterns = [
    url(r"^create/",views.create,name="create"),
    url(r"^channellist/",views.channellist,name="channellist"),
    url(r"^viewchannel",views.viewchannel,name="viewchannel"),
    url(r"^bloglist/",views.bloglist,name="bloglist"),
    url(r"^addblog/",views.addblog,name="addblog"),
    url(r"^removeblog",views.removeblog,name="removeblog"),
    url(r"^bloglistremove",views.bloglistremove,name="bloglistremove"),
    url(r"^indexchannellist/",views.indexchannellist,name="indexchannellist"),
    url(r"^indexchannelsearch/",views.indexchannelsearch,name="indexchannelsearch")

]
