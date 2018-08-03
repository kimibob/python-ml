from StateMachine import StateMachine

"""
地址级别要素表 
要素级别   
对应类别         对应要素特征字集合 
0          国家             中国，中华人民共和国， 
1          省、直辖市       省、特别行政区、自治区、市 
2          省会、地级市     市、盟、州 
3          区县            区、县、旗、市、州、林区、新区 
4          街道、乡镇       公所、镇、乡、苏木、办事处、居委会、社区、街道 
5          道路片区         村、组、队、里、园、庄、弄、舍、头、桥、口、田、农场、沟、屯、坡、荡、佃、堡、洼、旗、庄、套、垛、町、甸、冈、河、店、岛、集、坊、庄、路、大道、道、街、巷、胡同、条、里、村委会 
6          POI             大厦、广场、饭店、中心、大楼、场、馆、酒店、宾馆、市场、花园、招待所、中心、大学、厂、局、宿舍 
7          街道号、村组     组,队,园,弄,舍,桥,口,田,沟,坡,荡,佃,洼,套,垛,町,冈,巷,胡同,村委会,号,馆,趟,居,寓,苑墅,小区,公寓,号院,花园,大厦,广场,中心 
8          详细地址         单元,层,室,栋,号楼,幢,座,楼,斋,房间 
"""
def getIndex(doc,substr):
    try:
        index = doc.index(substr)
    except ValueError:
        return -1
    return index


def start_transitions(doc,detailList=[]):
    #detailList = []
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    for i,char in enumerate(doc):
        # find it
        if char in ("省","市","区"):
            breakIndex = i
            if char in ("省","区"): # 新疆维吾尔自治区昌吉回族自治州昌吉市昌吉市建国西路甜蜜家园9-1-301
                newState = "province_state"
            else:
                newState = "city_state"
            break

    if breakIndex != -1:
        restStr = doc[breakIndex+1:]
        detailList.append((newState,doc[:breakIndex+1]))

    return (newState,restStr,detailList)

def province_transitions(doc,detailList):

    breakIndex = -1
    newState = "error_state"
    restStr = ""
    for i,char in enumerate(doc):
        if char in ("市","县","区","州"):
            breakIndex = i
            if char == "市":
                newState = "city_state"
                break
            elif char == "州" and i >= 2:
            #elif char == "州" and detailList[-1][-1][-1].encode("utf8") == "区":
                newState = "state_state"
                break
            elif char in ("县","区"): # 县|区
                newState = "region_state"
                break

    if breakIndex != -1:
        restStr = doc[breakIndex+1:]
        detailList.append((newState,doc[:breakIndex + 1]))

    return (newState,restStr,detailList)

def state_transitions(doc,detailList):
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    for i,char in enumerate(doc):
        if char in ("市"):
            breakIndex = i
            newState = "city_state"
            break

    if breakIndex != -1:
        restStr = doc[breakIndex+1:]
        detailList.append((newState,doc[:breakIndex + 1]))

    return (newState,restStr,detailList)


def city_transitions(doc,detailList):
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    for i,char in enumerate(doc):
        if char in ("路","街","区","县","市"):
            breakIndex = i
            if char in ("区","县"):
                newState = "region_state"
            elif char == "市":
                newState = "city_state"
            else:
                newState = "street_state"
            break

    if breakIndex != -1:
        restStr = doc[breakIndex+1:]
        detailList.append((newState,doc[:breakIndex + 1]))

    return (newState,restStr,detailList)


def region_transitions(doc,detailList):
    breakIndex = -1
    newState = "error_state"
    restStr = ""

    for i,char in enumerate(doc):
        if char in ("路","街","区","镇","村"):
            breakIndex = i
            if char in ("路","街"):
                newState = "street_state"
            elif char in ("镇","村"):
                newState = "town_state"
            else:
                newState = "region_state"
            break

    if breakIndex != -1:
        restStr= doc[breakIndex+1:]
        detailList.append((newState,doc[:breakIndex + 1]))

    return (newState,restStr,detailList)

def street_transitions(doc,detailList):
    breakIndex = -1
    newState = "street_state"
    restStr = ""

    for i,char in enumerate(doc):
        char = char.encode("utf8")
        if char == "号":
            breakIndex = i
            newState = "doorplate_state"
            break

    if breakIndex != -1:
        restStr = doc[breakIndex+1:]
        detailList.append((newState,doc[:breakIndex + 1]))

    return (newState,restStr,detailList)

def town_transitions(doc,detailList):
    breakIndex = -1
    newState = "error_state"
    restStr = ""

    for i,char in enumerate(doc):
        char = char.encode("utf8")
        if char in ("路","街","村"):
            breakIndex = i
            if char in ("路","街"):
                newState = "street_state"
            else:
                newState = "town_state"
            break

    if breakIndex != -1:
        restStr = doc[breakIndex+1:]
        detailList.append((newState,doc[:breakIndex + 1]))
    return (newState,restStr,detailList)



if __name__ == "__main__":
    m = StateMachine()
    m.add_state("start_state",start_transitions)
    m.add_state("province_state",province_transitions)
    m.add_state("city_state",city_transitions)
    m.add_state("region_state",region_transitions)
    m.add_state("state_state",state_transitions)
    m.add_state("town_state",town_transitions,end_state=1)
    m.add_state("street_state",street_transitions,end_state = 1)
    m.add_state("doorplate_state",None,end_state = 1)

    m.set_start("start_state")

    #m.process("浙江杭州市西湖区城区文三路黄龙国际G座18层")
    m.process("浙江省杭州市西湖区城区文三路黄龙国际G座18层")
    #m.process("北京市北三环东路8号静安中心大厦")
    #m.process("黑龙江省哈尔滨市呼兰区南京路美兰家园5栋2单元303")
    #m.process("广东省深圳市罗湖区金稻田路1228号理想新城9栋A单元301室")
    #m.process("新疆维吾尔自治区昌吉回族自治州昌吉市昌吉市建国西路甜蜜家园9-1-301")
    #m.process("北京市北京市大兴区黄村镇海子角海悦公馆41号楼4单元602")
    #m.process("陕西省宝鸡市千阳县南关路粮食小区")
    #m.process("黑龙江省鸡西市虎林市黑龙江省虎林市公安南街276号")
    #m.process("辽宁省大连市金州区站前街道生辉第一城物业")
    #m.process("安徽省芜湖市无为县高沟镇龙庵街道")
    #m.process("广东省深圳市南山区科兴科学园A3单元12楼")
    #m.process("湖北省黄冈市浠水县散花镇涂墩村七组")
    #for x in open("sample_address.txt"):
    #    m.process(x.strip("\n"))
