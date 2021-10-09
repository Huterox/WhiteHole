
from django.shortcuts import render
from django.utils.safestring import mark_safe

'''
    该函数的目的只是插入alert提示，在模板相应位置插入{{tips}}
    
'''

def TipsAlert(request,htmlcontext,tips):
    tips = """ <script>alert("%s")</script> """%tips
    tips = mark_safe(tips)
    data = {
        "tips": tips
    }
    return render(request, htmlcontext, context=data)

def TipsAlertData(request,htmlcontext,tips,data):
    tips = """ <script>alert("%s")</script> """%tips
    data["tips"]=tips
    return render(request, htmlcontext, context=data)