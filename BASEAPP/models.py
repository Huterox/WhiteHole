from django.db import models
from django.core import validators
# Create your models here.
#
class WhiteManager(models.Manager):
	def get_queryset(self):
		return super(WhiteManager,self).get_queryset().filter(is_delete=False)


class User(models.Model):
    username = models.CharField(max_length=32,unique=True)
    #目前测试是明文加密密码，后面功能完成后系统大升级
    password  = models.CharField(max_length=128,null=False)
    userinfo = models.CharField(max_length=512)
    useremail = models.CharField(max_length=64)
    is_delete = models.BooleanField(default=False)  # 0没有1已删除
    objects = WhiteManager()

    def delete(self):
        self.is_delete = True
        self.save()
    class Meta:
        db_table="User"

class UserPic(models.Model):
    userpic = models.ImageField(upload_to="userpic/%Y%m",
                                validators=[validators.FileExtensionValidator
                                            (["jpg", "jpeg", "gif", "png", "bmp", "webp"],
                                             message='文件类型不对')])
    pic_user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)  # 0没有1已删除
    objects = WhiteManager()
    def delete(self):
        self.is_delete = True
        self.save()
    class Meta:
        db_table = "UserPic"
