from flask import Flask, render_template, request
from flask import render_template
from app.main.dbapi import *
from decimal import *
from datetime import timedelta
import app.main.FaceDetect.faceDetect as face
import base64
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=1)
@app.route('/')
def demo():
    return render_template("index.html")




'''
1.保存照片到本地
2.上传并进行人脸检测
3.人脸检测返回值为user_info，为一个列表：
            如果找到了已经存在的用户，返回形如list[True,False,user_id,name,gender,age,phone_number]的列表
            如果图片中有多张人脸，则返回[True,True],提示重新拍照
            若没有找到则返回list[False,True,user_id],user_id为新创建的用户的id
            若检测失败(因为网络问题或者没有检测到人脸)，则返回list[False,False]
'''
@app.route('/upload', methods=['GET', 'POST'])
def upload_test():
    print('uploading!')
    # 获取图片文件并保存
    if request.method == 'POST':  # 当以post方式提交数据时
        print('PostRequest!')
        data=request.form['data_url']
        # data = request.get_data()
        # print(data[22:])
        data=data[22:]

        #将base64解码生成图片文件并保存
        imgdata = base64.b64decode(data)
        file = open('FaceDetect/faces/face.jpg', 'wb')
        file.write(imgdata)
        file.close()

        #识别人脸数据并返回信息
        user_info = face.face_search('FaceDetect/faces/face.jpg')
        if (user_info[0]):
            if(user_info[1]):
                #图片中人脸太多，重新拍照
                return "照片中人脸多于1张，请重新拍摄！"
            else:
                # 找到了已经注册的用户
                return "\n搜索到已存在用户！\n该用户信息为 user_id: %s\n           name: %s\n" \
                      "           gender: %s\n           age: %s\n           phone_number: %s" \
                      % (user_info[2], user_info[3], user_info[4], user_info[5], user_info[6])

        elif(user_info[1]):
            # 用户未注册，创建新用户
            return "\n未搜索到已存在用户！\n新创建的用户信息为 user_id: %s\n其他信息为空！ " \
                   % (user_info[2])
        else:
            # 检测失败(因为各种各样的原因)
            return "人脸检测失败！ 请检查网络连接和照片是否包含人脸。"


    # if request.method == 'GET':  # 当以post方式提交数据时

    return ''

'''
1.注册信息接收
2.查询商品信息和价格发送给前台
'''
@app.route('/login', methods=["GET", "POST"])
def login():
    #获取id,name,price字段
    u = [(good.good_id, good.name, good.price) for good in query_goods()]
    goodnum = len(u)
    testlist = []
    '''
    1.信息转换成字符串发送到前台
    '''
    for i in range(goodnum):
        testlist.append([])
        testlist[i].append(str(u[i][0]))
        testlist[i].append(u[i][1].replace(" ", ""))
        m = str(Decimal(u[i][2]).quantize(Decimal('0.0')))
        testlist[i].append(m)
    new=[]
    for i in range(goodnum):
        new.append(" ".join(testlist[i]))
    final = " ".join(new)
    print(final)
    if request.method == "POST":
        data = request.get_json()
        for key in data:
            print(key + ':' + data[key])
        return(final)
    else:
        return render_template("login.html")

'''
1.用户购买信息接收
2.保存购买信息到数据库
'''
@app.route('/goods', methods=["GET", "POST"])
def savePurchase():
    if request.method == "POST":
        data = request.get_json()
        num=len(data)
        for i in range(num):
            for key in data[i]:
                if (key == "user_id"):
                    user_id=data[i][key]
                if (key == "good_id"):
                    good_id=data[i][key]
                if (key == "purchase_date"):
                    purchase_date = data[i][key]
                if (key == "total_price"):
                    total_price = data[i][key]
                if (key == "count"):
                    count=data[i][key]
            add_purchase_history(int(user_id), int(good_id), int(count), total_price, purchase_date)
        return("success")
    else:
        return render_template("login.html")
'''
1.接收用户ID
2.调用用户分析模块（预留）
3.根据用户分析购买推荐，返回给前台购买推荐信息
'''
@app.route('/recom', methods=["GET", "POST"])
def transReco():
    if request.method == "POST":
        #data获取用户id
        data = request.get_json()
        #userid作为用户行为分析模块的入参
        for key in data:
            userid=data[key]
        #预留调用用户分析模块
        return ("hello")
    else:
        return render_template("login.html")
if __name__ == '__main__':
    app.run(debug=True)


