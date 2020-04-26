import requests
import json
import os
import random

#网站操作根目录
root_url = "http://victor.czu.cn/api/"
#伪造头
headers={
    "Host":"victor.czu.cn",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "http://victor.czu.cn",
    "Referer": "http://victor.czu.cn/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
#相信大家都没病，所以目前支持修改的地方只有体温和地点
post_data = {
	"masterId": 6,
	"details": [{
		"questionNo": "0",
		"title": "今日体温",
		"value": ""
	}, {
		"questionNo": "05",
		"title": "目前所在地",
		"value": ""
	}, {
		"questionNo": "10",
		"title": "今日是否跨市流动",
		"value": "否"
	}, {
		"questionNo": "11",
		"title": "出发日期"
	}, {
		"questionNo": "12",
		"title": "出发城市"
	}, {
		"questionNo": "13",
		"title": "到达日期"
	}, {
		"questionNo": "14",
		"title": "到达城市"
	}, {
		"questionNo": "15",
		"title": "交通工具"
	}, {
		"questionNo": "16",
		"title": "班次、车次、车牌号或其他说明"
	}, {
		"questionNo": "20",
		"title": "身体状态",
		"value": "健康"
	}, {
		"questionNo": "21",
		"title": "身体状况说明"
	}, {
		"questionNo": "30",
		"title": "同住人员身体状况",
		"value": "健康"
	}, {
		"questionNo": "31",
		"title": "同住人员身体状况说明"
	}, {
		"questionNo": "40",
		"title": "14天内到访重点疫情防控地区情况",
		"value": "无"
	}, {
		"questionNo": "41",
		"title": "到访重点疫情防控地区日期"
	}, {
		"questionNo": "50",
		"title": "14天内接触重点疫情防控地区情况",
		"value": "无"
	}, {
		"questionNo": "51",
		"title": "接触重点疫情防控地区日期"
	}, {
		"questionNo": "60",
		"title": "备注"
	}]
}

#学号
userid = ""
#密码
password = ""
#登录成功的身份验证标识
token = ""
#是否已经保存用户名和密码
saved = False
#用户信息
userdata = {}

#0为体温，1为所在地
def set_value(index, value):
    post_data["details"][index]["value"] = value

#0为体温，1为所在地
def get_value(index):
    return post_data["details"][index]["value"]

#保存数据
def save_data():
    with open('./postdata.json', "w", encoding="utf-8") as f:
        f.write(json.dumps(post_data, ensure_ascii=False))

#保存数据
def read_data():
    with open('./postdata.json', "r", encoding="utf-8") as f:
        global post_data
        post_data = json.loads(f.read())

#登录
def login(userid, password):
    login_data = {
        "username": userid,
        "password": password, #居然用明文密码，笑了
        "type":"student"
    }
    res = requests.post(url=root_url + "user/login", json=login_data, headers=headers)
    data = json.loads(res.text)
    return (data["error"] == "0", data)

def fuck_school():
    #随机体温
    if(get_value(0) == "-1"):
        temp = random.randint(1, 10) / 10 + 36
        print(temp)
        set_value(0, str(temp))
    #加入身份验证
    headers["authorization"] = "Bearer " + token
    #中文必须以utf-8编码发送，这是个坑
    res = requests.post(url=root_url + "answer", data=json.dumps(post_data, ensure_ascii=False).encode(encoding="utf-8"), headers=headers)
    data = json.loads(res.text)
    return data["error"] == "0"

#判断是否保存了账号密码
saved = os.path.exists("./userdata.json")
if(saved):
    with open('./userdata.json', "r") as f:
        userdata = json.loads(f.read())
        userid = userdata["userid"]
        password = userdata["password"]
else:
    print("请输入学号")
    userid = input()
    print("请输入密码")
    password = input()

result = login(userid, password)
while(not result[0]):
    #辱骂白痴
    print("wdnmd，学号或者密码错了，重输！")
    userid = input()
    password = input()
    result = login(userid, password)
token = result[1]["data"]["token"]

if(not saved):
    print("是否保存用户名和密码？请输入Y(Yes)/N(No)")
    yn = input()
    saved = (yn == "Y" or yn == "y")
    if(saved):
        with open('./userdata.json', "w") as f:
            userdata["userid"] = userid
            userdata["password"] = password
            f.write(json.dumps(userdata, ensure_ascii=False))
    else:
        #妥协
        print("彳亍")

if(not os.path.exists("./postdata.json")):
    print("检测到第一次运行，请输入必要的数据")
    print("0: 体温，建议36.1~37, 输入-1则在这个范围里面随机")
    temp = input()
    print("1: 目前所在地，格式为 省/市/县，即你填表的时候选择的 第一个地点/第二个地点/第三个地点")
    place = input()
    set_value(0, temp)
    set_value(1, place)
else:
    read_data()
    print("是否需要修改数据？请输入Y(Yes)/N(No)")
    yn = input()
    if(yn == "Y" or yn == "y"):
        print("请输入要修改的部分的编号，0：今日体温，1：目前所在地(省/市/县)，2：不修改")
        cid = input()
        while(cid != "2"):
            value = input()
            #应用修改的值
            set_value(int(cid), value)
            print("修改成功")
            print("请输入要修改的部分的编号，0：今日体温，1：目前所在地(省/市/县)，2：不修改")
            cid = input()

#保存数据
save_data()

print("是否提交？请输入Y(Yes)/N(No)")
yn = input()
if(yn == "Y" or yn == "y"):
    if(fuck_school()):
        print("成功")
    else:
        print("好像失败了，联系作者吧")
elif(yn == "N" or yn == "n"):
    #进行羞♂辱
    print("不提交你点开这个程序点您🐎呢?")
    exit()
else:
    #善意の劝退
    print("醉了，就Y/N这两个字母都不会输，回家种田吧")
    exit()