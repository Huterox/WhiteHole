from django.db import models
from django.db import models
from BASEAPP.models import WhiteManager
from BASEAPP.models import User
from Blog.models import Bolg
# Create your models here.

class Channel(models.Model):
    channel_name = models.CharField(max_length=64,null=False)
    channel_desc = models.CharField(max_length=128,null=True)
    channel_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    channel_blog = models.ManyToManyField(Bolg,null=True)
    is_delete = models.BooleanField(default=False)  # 0没有1已删除
    objects = WhiteManager()
    def delete(self):
        self.is_delete = True
        self.save()
    class Meta:
        db_table = "Channel"