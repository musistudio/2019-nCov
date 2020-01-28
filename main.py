import requests
import re
import json


Position = {}

# 获取csv数据
def getOldData():
    with open('2019-nCov.csv', 'r') as f:
        datas = f.read().split('\n')
    datas = datas[1:-1]
    for data in datas:
        dt = data.split(',')
        Position[dt[2]] = dt[4][1:] + ',' + dt[5][:-1]
    print(Position)


# 从丁香园获取数据
def getDatas():
    url = 'https://3g.dxy.cn/newh5/view/pneumonia?from=timeline&isappinstalled=0'
    res = requests.get(url)
    data = res.content.decode('utf8')
    datas = re.findall('window.getAreaStat =(.*?)}c', data, re.S)[0]
    datas = json.loads(datas)
    genCSV(datas)

# 生成CSV数据
def genCSV(datas):
    with open('2019-nCov.csv', 'w') as f:
        f.write('省份,确诊人数,城市,城市确诊人数,经纬度\n')
    for data in datas:
        print('{}共确诊{}例'.format(data['provinceName'], data['confirmedCount']))
        cities = data['cities']
        if len(cities) == 0:
            try:
                position = Position[data['provinceName']]
            except:
                position = getPosition(data['provinceName'])
            fileData = '{},{},{},{},"{}"'.format(data['provinceName'], data['confirmedCount'], data['provinceName'], data['confirmedCount'], position)
            with open('2019-nCov.csv', 'a+') as f:
                f.write(fileData + '\n')
        for city in cities:
            if '外地来' in city['cityName']:
                name = data['provinceName']
            else:
                name = city['cityName']
            try:
                position = Position[name]
            except:
                position = getPosition(name)
            fileData = '{},{},{},{},"{}"'.format(data['provinceName'], data['confirmedCount'], city['cityName'], city['confirmedCount'], position)
            with open('2019-nCov.csv', 'a+') as f:
                f.write(fileData + '\n')


# 获取地址经纬度
def getPosition(name):
    print('{}获取请求'.format(name))
    # 地址名称转换：转换成高德可识别的地址名称
    if name == '恩施州':
        name = '恩施土家族苗族自治州'
    if name == '秀山县':
        name = '秀山土家族苗族自治县'
    if name == '陵水县':
        name = '陵水黎族自治县'
    if name == '黔南州':
        name = '黔南布依族苗族自治州'
    if name == '石柱县':
        name = '石柱土家族自治县'
    if name == '湘西自治州':
        name = '湘西土家族苗族自治州'
    if name == '甘孜州':
        name = '甘孜藏族自治州'
    if name == '呼伦贝尔牙克石市':
        name = '牙克石市'
    if name == '黔西南州':
        name = '黔西南布依族苗族自治州'
    if name == '凉山州':
        name = '凉山彝族自治州'
    if name == '锡林郭勒盟锡林浩特':
        name = '锡林浩特'
    if name == '鄂尔多斯东胜区':
        name = '鄂尔多斯市'
    if name == '呼伦贝尔满洲里':
        name = '满洲里市'
    if name == '兴安盟乌兰浩特':
        name = '乌兰浩特市'
    if name == '通辽市经济开发区':
        name = '通辽市'
    if name == '锡林郭勒盟二连浩特':
        name = '二连浩特'
    if name == '鄂尔多斯鄂托克前旗':
        name = '鄂托克前旗'
    if name == '呼伦贝尔牙克石':
        name = '牙克石'
    if name == '赤峰市松山区':
        name = '松山区'
    if name == '包头市东河区':
        name = '东河区'
    if name == '琼中县':
        name = '琼中黎族苗族自治县'
    if name == '包头市昆都仑区':
        name = '昆都仑区'
    if name == '赤峰市林西县':
        name = '林西县'
    url = 'https://restapi.amap.com/v3/config/district?keywords=%s&subdistrict=0&key=605d8d5427b389a86a69288df1c24a0c' % name
    result = requests.get(url).json()
    try:
        if result['status'] == '1':
            return result['districts'][0]['center']
        else:
            return False
    except:
        pass


# 获取ip地址
def getIp():
    url = "http://2000019.ip138.com/"
    res = requests.get(url).text
    ip = re.findall('您的IP地址是：\[(.*?)\] 来自', res, re.S)[0]
    province = re.findall('来自：(.*?)</p>', res, re.S)[0]
    province = province.replace('\r\n', '')
    provinces = province.split('省')
    if len(province) > 1:
        province = provinces[0] + '省'
    return {"ip": ip, "province": province}

# getIp()

getOldData()

getDatas()
