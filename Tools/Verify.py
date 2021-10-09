import random
from io import BytesIO

from PIL import Image,ImageFont,ImageDraw

def GetCode():
    source = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    code = ""
    for i in range(4):
        code += random.choice(source)
    return code


def Set_Color():
    return random.randrange(255)

def Send_code_img(request):
    Img_Width = 400
    Img_Height = 400
    color_bg = (Set_Color(), Set_Color(), Set_Color())
    image = Image.new("RGB", size=(Img_Height,Img_Width), color=color_bg)

    imagedraw = ImageDraw.Draw(image, "RGB")

    font = ImageFont.truetype("/static/Font/ALGER.TTF",120)
    YanZhen_code = GetCode()
    imagedraw.text(xy=(30,150), text=YanZhen_code, font=font, fill=(255, 255, 255))

    request.session["verify_code"]=YanZhen_code

    for i in range(1000):
        # 绘制干扰点
        imagedraw.point(xy=(random.randrange(Img_Width), random.randrange(Img_Height)), fill=(Set_Color(), Set_Color(), Set_Color()))

    # image.show()
    fp = BytesIO()
    image.save(fp,"png")
    return fp.getvalue()

if __name__=="__main__":
    pass
