from django.db import models
from BASEAPP.models import WhiteManager
from BASEAPP.models import User
from mdeditor.fields import MDTextField

class Bolg(models.Model):
    # 用户博客
    title = models.CharField(max_length=128,null=False)
    body = MDTextField()
    blog_user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)  # 0没有1已删除
    date = models.DateTimeField(null=True)
    objects = WhiteManager()
    def delete(self):
        self.is_delete = True
        self.save()
    class Meta:
        db_table = "Blog"

class Comment(models.Model):
    # 评论
    comment = models.CharField(max_length=512)
    comment_user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_blog = models.ForeignKey(Bolg,on_delete=models.CASCADE)

    class Meta:
        db_table = "Comment"
