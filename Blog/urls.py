from django.conf.urls import url
from Blog import views

urlpatterns = [
    url(r"^Editor/",views.Editor,name="Editor"),
    url(r"^Save/",views.Save,name="Save"),
    url(r"^Upload/",views.Upload,name="Upload"),
    url(r"^comment/",views.comment,name="comment"),
]
