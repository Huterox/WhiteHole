
# whitehole

[TOC]

# 项目说明

本项目基于Django3.x版本，用于学习和交流，本项目当前版本为V0.51具备基础功能的可测试版本，后期将不断更新~

当前 v0.5x所具有的功能简介如下：https://www.bilibili.com/video/BV1GQ4y1B7Ct#reply5555363226（给个三连哟）

联系作者：

>1.B站，如上链接
>
>2.CSDN 博主 Huterox留言
>
>3.本人QQ：3139541502

相关依赖为

```python
asgiref            3.4.1
DateTime           4.3
defusedxml         0.7.1
diff-match-patch   20200713
Django             3.2.6
django-mdeditor    0.1.18
et-xmlfile         1.1.0
importlib-metadata 4.8.1
Markdown           3.3.4
MarkupPy           1.14
odfpy              1.4.1
openpyxl           3.0.9
Pillow             8.3.1
pip                10.0.1
Pygments           2.10.0
PyMySQL            1.0.2
pytz               2021.1
PyYAML             5.4.1
setuptools         39.1.0
sqlparse           0.4.1
tablib             3.0.0
typing-extensions  3.10.0.0
xlrd               2.0.1
xlwt               1.3.0
zipp               3.5.0
zope.interface     5.4.0

```





# 已有接口说明

## 首页

首页的url的反向解析地址为```index```

具体的在本地的访问路径（8000端口下）

```127.0.0.1:8000```

接受参数：

> Get参数：
>
> ​	?flag
>
> 作用：用于搜索功能的参数接受，由于处于安全考虑，搜索功能先使用psot请求获取flag作为安全验证的钥匙后通过浏览器将再次发送get请求从服务端获取搜索数据。相关受影响路径：/Channel/indexchannelsearch (Channel:indexchannelsearch)

请求要求：

> 无，或者 Get请求的flag参数

首页view参数设置

> 1.userpic 用户头像
>
> 2.tips 首页消息提示，通过session进行设置，当从不同的页面跳转回主页时可以同过设置``` request.session['tips']=tips``
>
> 进行消息设置。

**返回的session，cookie 无，参数无**

## 注册

反向解析地址：Base:regirst

对应views为 BASE.views.regirst

请求要求：

> Get：通过验证后的验证证明（钥匙），如果缺少则跳转至验证页面，传入验证页面所需的验证参数（以cookie传入）
>
> Post：对应的用户信息表单

成功后返回首页，首页显示默认头像。

## 登录

反向解析地址： Base:login

对应views为：BASE.views.login

请求要求：

> Get：通过验证后的验证证明（钥匙），如果缺少则跳转至验证页面，传入验证页面所需的验证参数（以cookie传入）
>
> Post：对应的用户信息表单

成功后返回首页，首页显示默认头像/用户自己的头像。



## 验证

反向解析地址： Base:verify

对应views为：BASE.views.verify

所需参数：

> cookie：需要验证的验证的页面（验证通过后自动跳转至验证后需要前往的页面）

接受请求：

> Get / Post

对应views还需要额外请求获取验证码的接口。

## 获取验证码

反向解析地址： Base:get_code_img

对应views为：BASE.views.get_code_img

所需参数：无

返回

```python
 content_type='image/png'
```



## 个人页面

反向解析地址： Base:Mine

对应views为：BASE.views.Mine

参数要求：

>cookie（session）：登录成功的验证参数。
>
>否：
>
>跳转回主页

此页面主要负责加载对应用户的所有信息。

## 用户头像上传

此页面也需登录

反向解析地址： Base:userpic

对应views为：BASE.views.userpicsave

不满足参数要求返回空

（由于接口较为敏感，在未来如果不满足参数要求用户将被跟踪）

## 用户跟人信息上传



此页面也需登录

反向解析地址： Base:submitinfo

对应views为：BASE.views.submitinfo

不满足参数要求返回空

（由于接口较为敏感，在未来如果不满足参数要求用户将被跟踪）

## 用户博客列表加载

此页面也需登录

反向解析地址： Base:bloglist

对应views为：BASE.views.bloglist

参数要求

>Get:
>
>​	?wirter=
>
>当其他用户查看当前用户时需要提供参数。

不满足参数要求返回404

（由于接口较为敏感，在未来如果不满足参数要求用户将被跟踪）



## 用户频道博客查看

此页面也需登录

反向解析地址： Base:viewblog

对应views为：BASE.views.viewblog

参数要求

>Get:
>
>​	?wirter=
>
>​	&
>
>​	title=
>
>​	&
>
>​	username=
>
>当其他用户查看当前用户时需要提供参数。

```python
    blogtitle = request.GET.get("title")
    wirter = request.GET.get("username")
```

不满足参数要求返回404

（由于接口较为敏感，在未来如果不满足参数要求用户将被跟踪）

## 博客编辑

此页面也需登录

反向解析地址： Blog:Editor

对应views为：Blog.views.Editor

如果不满足参数要求将返回主页

## 博客上传

此页面也需登录

反向解析地址： Blog:Save

对应views为：Blog.views.Save

如果不满足参数要求将返回主页

此接口将保存将markdown文档转换为html文档

## 博客图片上传

反向解析地址： Blog:Upload

对应views为：Blog.views.Upload

返回参数：

```json
{"success": 1, "message": "上传成功", "url": '/static/upload/' + data_path + '/' + file_name}
```

```json
{"success": 0, "message": "上传失败"}
```

## 博客评论

此页面也需登录

反向解析地址： Blog:comment

对应views为：Blog.views.comment

不满足参数要求返回 404 

（在未来将被监控）

## 创建频道接口

此页面也需登录

反向解析地址：Channel:create

对应views为：Channel.views.create

不满足参数要求返回主页

接受请求：

> Get/Post

## 展示频道列表接口



此页面也需登录

反向解析地址：Channel:channellist

对应views为：Channel.views.channellist

参数要求（不可为空）：

>```url
>?wirter=
>```

用于其他用户查看当前用户频道

不满足参数要求返回主页

## 查看频道

此页面也需登录

反向解析地址：Channel:viewchannel

对应views为：Channel.views.viewchannel

参数要求（不可为空）：

>```url
>?channel_name=
>&channel_wirter=
>
>```

```python
channel_name = request.GET.get("channel_name")
channel_wirter = request.GET.get("channel_wirter")
```

用于其他用户查看当前用户频道

不满足参数要求返回主页

## 频道博客列表显示

此页面也需登录

反向解析地址：Channel:bloglist

对应views为：Channel.views.bloglist

参数要求（不可为空）：

> ？wirter=
>
> &channelname=

```python
wirter = request.GET.get("wirter", None)  # 查看作者
channelname = request.GET.get("channelname")
```

## 频道添加博客

此页面也需登录

反向解析地址：Channel:addblog

对应views为：Channel.views.addblog

参数要求（不可空）：

```python
blogname = request.GET.get("title")
wirter = request.GET.get("username")
channelname = request.GET.get("channelname")
```

## 频道移除博客

此页面也需登录

反向解析地址：Channel:removeblog

对应views为：Channel.views.removeblog

参数要求（不可空）：

```python
blogname = request.GET.get("title")
wirter = request.GET.get("username")
channelname = request.GET.get("channelname")
```

## 频道移除博客列表

此页面也需登录

反向解析地址：Channel:bloglistremove

对应views为：Channel.views.bloglistremove

参数要求（不可空）：

```python
wirter = request.GET.get("wirter", None)  # 查看作者
channelname = request.GET.get("channelname")
```

## 首页频道列表显示

此页面不需登录

反向解析地址：Channel:indexchannellist

对应views为：Channel.views.indexchannellist



## 首页频道搜索

此页面也需登录

反向解析地址：Channel:indexchannelsearch

对应views为：Channel.views.indexchannelsearch

接受请求

> Get/Post

# 工具类说明

工具类分为几大块，一个是通用的，另一个是专用的，专门为某个views设计的。

这里主要说明DeFine这个工具包是未来的防御功能的主要实现。当前版本暂时没有~

由于代码本身很好理解这里不作赘述。

# 当前项目结构
>>>>>>> c8e5848 ( 可测试的基础版本V0.51)
>>>>>>> 92e3b0d (可测试的基础版本V0.51)
