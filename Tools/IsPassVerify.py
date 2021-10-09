from django.shortcuts import render
def IsPassVerify(request,htmltext,salt,tourl):
    '''

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

    if verifypass and (verify_code == verify_post):
        # renders.delete_cookie("To")
        # request.session.flush()
        return renders
    else:

        renders_v = render(request, "verify.html")
        renders_v.set_signed_cookie("To", tourl, salt=salt)
        return renders_v