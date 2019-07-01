from StateMachine import StateMachine
import re

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

fujian_city = ['福州','厦门','泉州','漳州','莆田','三明','龙岩','南平','宁德']


def getIndex(doc,substr):
    try:
        index = doc.index(substr)
    except ValueError:
        return -1
    return index

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName,encoding='utf-8')
    for line in fr.readlines():
        dataMat.append(line.replace('\n',''))
    return dataMat

# 省
def province_transitions(doc,detailList=[],current_state=""):
    #detailList = []
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    # for i,char in enumerate(doc):
    #     # find it
    #     if char in "省":
    #         breakIndex = i
    #         if char in "省": # 新疆维吾尔自治区昌吉回族自治州昌吉市昌吉市建国西路甜蜜家园9-1-301
    #             newState = "city_state"
    #         else:
    #             newState = "region_state"
    #         break
    # if breakIndex != -1:
    #     restStr = doc[breakIndex+1:]
    #     detailList.append((current_state,doc[:breakIndex+1]))
    # else:
    #     detailList.append((current_state,"福建省"))
    #     restStr = doc.replace("福建","")
    #     newState = "city_state"

    #固定福建省

    if doc.startswith('福建省'):
        restStr = doc.replace('福建省','',1)
    elif doc.startswith('福建'):
        restStr = doc.replace('福建','',1)
    else:
        restStr = doc
    newState = "city_state"
    detailList.append((current_state, "福建省"))
    return (newState,restStr,detailList)

# 市
def city_transitions(doc,detailList,current_state):
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    # for i,char in enumerate(doc):
    #     if char in "市":
    #         breakIndex = i
    #         if char == "市":
    #             newState = "region_state"
    #             break
            # elif char == "州" and i >= 2:
            # #elif char == "州" and detailList[-1][-1][-1].encode("utf8") == "区":
            #     newState = "town_state"
            #     break
            # elif char in ("县","区"): # 县|区
            #     newState = "state_state"
            #     break
            # elif char in "道": # 厦门集美区杏滨街道
            #     newState = "building_state"
            #     break

    # if breakIndex != -1:
    #     restStr = doc[breakIndex+1:]
    #     detailList.append((current_state,doc[:breakIndex + 1]))
    # else:
    #     for city in fujian_city:
    #         if doc.find(city) >=0:
    #             detailList.append((current_state, city+"市"))
    #             restStr = doc.replace(city, "")
    #     newState = "region_state"
    for city in fujian_city:
        if doc.startswith(city):
            restStr = doc.replace(city,'',1)
            if restStr.startswith("市"):
                restStr = restStr.replace("市",'',1)
            detailList.append((current_state, city))
            break
    if restStr=='':
        restStr = doc
        detailList.append((current_state, ""))

    newState = "region_state"
    return (newState,restStr,detailList)


# 区、县
def region_transitions(doc,detailList,current_state):
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    # for i,char in enumerate(doc):
    #     if char in ("路","街","区","县","市"):
    #         breakIndex = i
    #         if char in ("区","县"):
    #             newState = "state_state"
    #         elif char == "市":
    #             newState = "state_state"
    #         else:
    #             newState = "building_state"
    #         break
    for region in fujian_region:
        index = doc.find(region)
        if index >= 0:
            restStr = doc.replace(region,'')
            detailList.append((current_state, doc[:index + len(region)]))
            break
    if restStr == '': #说明没有出现地市，该级置空
        restStr = doc
        detailList.append((current_state, ""))
    # if breakIndex != -1:
    #     restStr = doc[breakIndex+1:]
    #     detailList.append((current_state,doc[:breakIndex + 1]))
    newState = "state_state"
    return (newState,restStr,detailList)

# 乡镇、街道
def state_transitions(doc,detailList,current_state):
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    street_flag = False
    if doc.find("街道") >= 0:
        street_flag=True
    for i,char in enumerate(doc):
        if char in ("镇","村","道"):#取消匹配"路"，"区"
            breakIndex = i
            if char in "道": # 处理街道，此处匹配道
                newState = "street_state"
            # elif char in "路":
            #     newState = "community_state"
            elif char in ("镇","村"):
                newState = "street_state"
            else:
                newState = "state_state"
            break
        # elif char in "街" and not street_flag: # 处理街道，此处单独匹配只有"街"
        #     breakIndex = i
        #     newState = "community_state"
        #     break

    if breakIndex != -1:
        restStr= doc[breakIndex+1:]
        current_addr = doc[:breakIndex + 1]
        t = (current_state, current_addr)
        already_exist = False
        for part in detailList:
            state,value = part
            if value == current_addr:
                already_exist = True
                break
        if not already_exist:
            detailList.append(t)
    else:
        restStr = doc
        newState = "street_state"
        detailList.append((current_state, ""))
    return (newState,restStr,detailList)

# 道路
def street_transitions(doc,detailList,current_state):
    breakIndex = -1
    newState = "error_state"
    restStr = ""
    for i,char in enumerate(doc):
        if char in ("道","路","街"):# 取消"村"，村与路平级;"道"对应解析"xx大道"
            breakIndex = i
            if char in ("道","路","街"):# 取消"村"，村与路平级
                newState = "community_state"
            # else:
            #     newState = "street_state"
            break

    if breakIndex != -1:
        restStr = doc[breakIndex+1:]
        detailList.append((current_state,doc[:breakIndex + 1]))
    else:
        #很多地址省略了道路直接从乡镇到小区，默认解析不出道路也进行下一步小区名的提取
        #福建省漳州市龙海市角美镇东山龙泉绿苑9号楼1单元16层1601
        newState = "community_state"
        restStr = doc
        detailList.append((current_state, ""))
    return (newState,restStr,detailList)

# 社区
def community_transitions(doc,detailList,current_state):
    #doc = '文三路(6号)黄龙国际G座18层'
    # newState = "error_state"
    restStr = ""
    # pattern = re.compile("(\d*号|社区)*([^0-9]*)(\w+)(号|幢|座|栋|#)")
    pattern = re.compile("(^\d*号|社区)*([^A-Za-z0-9]*)([A-Za-z0-9]+)(号|幢|座|栋|#|T|-)")
    # 解决小区中出现xx A区的问题
    # 福建省福州市台江区新港街道五一南路189号金色维也纳A区2#1T10层1006
    doc = re.sub(r"[A-Za-z0-9]区", '', doc)
    match = pattern.match(doc)
    # print("community_transitions:"+doc)
    # print("1:"+match.group(1))
    # print("2:"+match.group(2))
    # print(match.group(3))
    # print("4:"+match.group(4))
    # try:
    if match and match.group(2)!='':
        keyword = match.group(2)
        restStr = doc[doc.index(keyword)+len(keyword):]
        newState = "building_state"
        detailList.append((current_state, keyword))
        # print("1:"+match.group(1))
        # print("2:"+match.group(2))
        # print("3:"+match.group(3))
        # print("4:"+match.group(4))
    # except Exception as e:
    #     print("sss")
        # import traceback
        # traceback.print_exc()
        # verified = False
    else:
        # 福州市台江茶亭街道五一中路132号锦颐大酒店北楼18层1816
        # ^\d*号-\d* 对应 66号-14香樟林城市花园C#1T6层602
        # ^\d*-\d*号 对应 1-1号中海寰宇天下二期20号32层3207
        pattern = re.compile("(^\d*号-\d*|^\d*-\d*号|^\d*号|社区)*([^A-Za-z0-9]*)([A-Za-z0-9]+)")
        match = pattern.match(doc)
        if match:
            keyword = match.group(2)
            restStr = doc[doc.index(keyword) + len(keyword):]
            newState = "building_state"
            detailList.append((current_state, keyword))
        else:
            restStr = doc
            detailList.append((current_state, ''))
            # 即使没识别到小区名也继续识别楼号层号房号
            newState = "building_state"

    return (newState, restStr, detailList)

#楼栋
def building_transitions(doc,detailList,current_state):
    newState = "error_state"
    restStr = ""
    # pattern = re.compile("(\w+)(号楼|幢|座|栋|#)")
    pattern = re.compile("[^0-9]*([A-Za-z0-9]+)(楼|号楼|幢|座|栋|#|T|-)")
    match = pattern.match(doc)
    if match:
        building_number = match.group(1)
        building_keyword = match.group(2)
        restStr = doc[doc.index(building_keyword) + len(building_keyword):]
        newState = "floor_state"
        detailList.append((current_state, building_number))
    else:
        restStr = doc
        detailList.append((current_state, ''))
        # 即使没识别到楼栋号也继续识别层号房号
        newState = "floor_state"
    return (newState, restStr, detailList)

#楼层
def floor_transitions(doc,detailList,current_state):
    newState = "error_state"
    pattern = re.compile("(\d+)(层|F)(\d*)")
    match = pattern.search(doc)
    floor=""
    room=""
    if match:
        floor = match.group(1)
        room_number = match.group(3)
        if len(room_number) == 3:
            floor = room_number[0:1]
            room = room_number[1:3]
        elif len(room_number) == 4:
            floor = room_number[0:2]
            room = room_number[2:4]
    else:
        pattern = re.compile("(\d+)(室|$)")
        match = pattern.search(doc)
        if match:
            room_number = match.group(1)
            if len(room_number) == 3:
                floor = room_number[0:1]
                room = room_number[1:3]
            elif len(room_number) == 4:
                floor = room_number[0:2]
                room = room_number[2:4]
    if floor=='' or room=='': # 1梯402层
        pattern = re.compile("(\d+)(层)")
        match = pattern.search(doc)
        if match:
            room_number = match.group(1)
            if len(room_number) == 3:
                floor = room_number[0:1]
                room = room_number[1:3]
            elif len(room_number) == 4:
                floor = room_number[0:2]
                room = room_number[2:4]

    restStr = doc
    newState = "end_state"
    detailList.append((current_state, floor))
    detailList.append(("ROOM_STATE", room))
    return (newState, restStr, detailList)


if __name__ == "__main__":
    fujian_region = loadDataSet("region.txt")

    m = StateMachine()
    m.add_state("province_state",province_transitions)
    m.add_state("city_state",city_transitions)
    m.add_state("region_state",region_transitions)
    m.add_state("state_state",state_transitions)
    m.add_state("street_state",street_transitions)
    m.add_state("community_state", community_transitions)
    m.add_state("building_state", building_transitions)
    m.add_state("floor_state", floor_transitions)
    m.add_state("end_state", None, end_state=1)

    m.set_start("province_state")

    # address="福建省福州市仓山区建新镇冠浦路6号福晟钱隆金山10#1101"
    # print(m.process("1",address.replace(' ','').replace('/','')))
    address = "福建省福州市晋安区茶园街道六一北路166号东南花园C#1T-3F301室"
    address = "福建省福州市闽侯县上街镇高新大道1-1号中海寰宇天下二期20号32层3207"
    address = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]|（.*?\\）", "", address).replace("\n", "")
    print(m.process("1",address.replace(' ','').replace('/','')))

    # print(m.process("1","福建省福州仓山区建新镇冠浦路6号福晟钱隆金山78座11F1102"))

    # fujian_state = loadDataSet("state.txt")
    # print(fujian_state)

    outfile = open('C:\\Users\\zq\\Desktop\\output.txt', 'w',encoding='utf-8')
    for x in open("C:\\Users\\zq\\Desktop\\wireless_addr.txt",encoding='utf-8'):
        id = x.split(",")[0]
        addr = x.split(",")[1].replace(' ','').replace('/','')
        addr = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]|（.*?\\）", "", addr).replace("\n", "")
        str = m.process(id, addr)
        outfile.write(str+"\n")
    outfile.close()

