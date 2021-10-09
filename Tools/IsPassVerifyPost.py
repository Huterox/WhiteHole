from django.shortcuts import render
def IsPassVerifyPost(request,htmltext,salt,tourl):
    '''
    对同一页面的Post请求进行验证
    :param request:
    :param htmltext:
    :param salt:
    :param tourl: this url is to reverse!
    :return:
    '''

    renders = render(request, htmltext)
    try:
        verifypass = request.get_signed_cookie("To", salt=salt)
        verify_code = request.session.get("verify_code").lower()
        verify_post = request.session.get("verify_code_post").lower()
    except Exception as e:
        verifypass = None
        verify_code = 1
        verify_post = -1

    if verifypass and (verify_code == verify_post) and verify_code:
        renders.delete_cookie("To")
        request.session.flush()
        return (1,1) #验证通过返回（1，1）
    else:

        renders_v = render(request, "verify.html")
        renders_v.set_signed_cookie("To", tourl, salt=salt)
        return (0,renders_v) # 验证不通过返回