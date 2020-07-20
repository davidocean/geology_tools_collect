from globe_const import *
from fractions import Fraction


# 以字符串的方式展示经纬度
def show_dms(data):
    if decimal_to_dms(data) == False:
        return False
    else:
        dms_dic = decimal_to_dms(data)
        result_string = DMS_FORMAT % (dms_dic[ANGLE_DEGREE], str(dms_dic[ANGLE_MINUTE]).zfill(2), str(dms_dic[ANGLE_SECOND]).zfill(2))
        return result_string


# 以小数点后6位的方式展示 十进制角度
def show_demical(d, m, s):
    result = dms_to_decimal(d, m, s)
    if result == False:
        return False
    else:
        # 保留六位小数
        result_string = DECIMAL_DMS_BAOLIU.format(result)
        return result_string

# 计算图幅号，并以列表的形式返回图幅号列表
def show_tfh(lon, lat):
    result_dic = get_tfh(lon, lat)
    result_list = []
    if not result_dic:
        return False
    else:
        for k, v in result_dic.items():
            result_list.append(TFH_FORMAT % (aligns(TFH_SCALE_NAME[k]), v))
    return result_list

# 计算图幅号的四角坐标，并以列表的方式返回：
def show_tfh_to_jwd(tfh):
    result_dic = get_jwd(tfh)
    result_list = []
    for k,v in result_dic.items():
        if not k.endswith(LON_LAT_ENDWITH_DD):
            # v中的数值为分数，因此需要进行float化，并使用round(v,6)限定小数点不超过6位
            temp_string = LON_LAT_SHOW_FORMAT%(LON_LAT_CN_DIC[k], round(float(v),6),result_dic[k+LON_LAT_ENDWITH_DD])
            result_list.append(temp_string)
    return result_list

# 十进制转经纬度
def decimal_to_dms(data):
    if not is_number(data):
        return False
    else:
        # data = float(data)
        d = int(data)
        m = int((data - d) * 60)
        s = int(((data - d) * 60 - m) * 60)
        result_dic = {ANGLE_DEGREE: d, ANGLE_MINUTE: m, ANGLE_SECOND: s}
        return result_dic


# 度分秒转化为十进制
def dms_to_decimal(d, m, s):
    if not is_number(d):
        return False
    elif not is_number(m):
        return False
    elif not is_number(s):
        return False
    elif float(d) < 0 or float(d) > 360:
        return False
    elif float(m) < 0 or float(m) > 60:
        return False
    elif float(s) < 0 or float(s) > 60:
        return False
    else:
        result_float = int(d) + float(m) / 60 + float(s) / 3600
        return result_float


# 判断是否为数值
def is_number(data):
    try:
        float(data)
        return True
    except ValueError:
        return False


# 计算图幅号 根据输入经纬度获取图幅号
def get_tfh(lon, lat):
    if not is_number(lon):
        return False
    elif not is_number(lat):
        return False
    else:
        lon = float(lon)
        lat = float(lat)
        if not is_lon_lat_in_china(lon, lat):
            return False

    # 开始计算分幅
    scale_100w_tfh = get_tfh_100w(lon, lat)
    tfh_dic = {}
    # 开始计算
    for k, v in TFH_LAT_LON_GAP.items():
        scale = k
        lon_temp = int((lon % 6) / v[1]) + 1
        lat_temp = int(4 / v[0]) - int((lat % 4) / v[0])
        if scale == "A":
            lon_num = TFH_KONG
            lat_num = TFH_KONG
            scale = ""
        elif scale == "R":
            scale = str(lon_temp + 6 * (lat_temp - 1)).zfill(2)
            lon_num = TFH_KONG
            lat_num = TFH_KONG
        elif scale in ["K", "J"]:
            lon_num = str(lon_temp).rjust(4, "0")
            lat_num = str(lat_temp).rjust(4, "0")
        else:
            lon_num = str(lon_temp).rjust(3, "0")
            lat_num = str(lat_temp).rjust(3, "0")

        tfh_temp = scale_100w_tfh + scale + lat_num + lon_num
        tfh_dic[k] = tfh_temp
    return tfh_dic


# 判断经纬度是否在中国范围内
def is_lon_lat_in_china(lon, lat):
    if not (70 <= lon <= 150):
        return False
    elif not (0 <= lat <= 56):
        return False
    else:
        return True


# 计算百万分幅
def get_tfh_100w(lon, lat):
    lon_temp = int(lon / 6) + 31
    lat_temp = int(lat / 6) + 1

    lon_num = str(lon_temp)
    lat_num = chr(lat_temp + 64)

    tfh_temp = lat_num + lon_num
    return tfh_temp


# 判断是否为图幅号
def is_tfh(data):
    data = str(data).upper()  # 转化为大写字符串
    # 判断长度为3的图幅号，则为100万图幅号
    if len(data) == 3:
        if 86 >= ord(data[0]) >= 65:  # 判断 百万分幅在A~V之间
            if is_number(data[1:3]):
                return True

    # 判断长度为5的图幅号，则为20万图幅号
    if len(data) == 5:
        if 86 >= ord(data[0]) >= 65:  # 判断 百万分幅在A~V之间
            if is_number(data[1:3]):
                if is_number(data[3:5]):
                    if 0 < int(data[3:5]) <= 36:  # 20万比例尺末两位值不超过36
                        return True

    # 判断长度为12的图幅号，则为大于1：2000比例尺的图幅号
    if len(data) == 12:
        if 86 >= ord(data[0]) >= 65:  # 判断 百万分幅在A~V之间
            if is_number(data[1:3]):
                if data[3] in TFH_12_LIST:
                    if is_number(data[4:]):
                        return True

    # 正常的10位图幅号的判断情况
    if len(data) != 10:
        return False
    elif data[3] not in TFH_10_LIST:
        return False
    elif not ord(data[0]) < 86 and ord(data[0]) > 65:
        return False
    elif not is_number(data[1:3]) and is_number(data[4:7]) and is_number(data[7:10]):
        return False
    else:
        return True


# 补全空格，格式统一
def aligns(data, length=25):
    difference = length - len(data)
    if difference == 0:
        return data
    elif difference < 0:
        return False
    new_string = TFH_KONG
    for i in data:
        codes = ord(i)
        if codes > 126:  # 当为中文时，退一个
            # new_string = new_string + chr(codes + 65248)
            difference = difference - 1
    return data + "-" * (difference)

# 通过图幅号获取经纬度
def get_jwd(tfh):
    tfh = tfh.upper()
    if not is_tfh(tfh):
        return False

    hundred_dic = get_100w_jwd(tfh[:3])

    if len(tfh) == 3:# 百万分幅图幅号时
        return hundred_dic
    elif len(tfh) == 5:# 1:20万图幅号时
        result_dic = get_20w_jwd(tfh)
        return result_dic

    else:
        scale_code = tfh[3]
        if scale_code in TFH_12_LIST:
            num_left = int(tfh[4:8])
            num_right = int(tfh[8:12])
        else:
            num_left = int(tfh[4:7])
            num_right = int(tfh[7:10])

        #左下角
        x_min = hundred_dic[LON_MIN] + (num_right -1) * TFH_LAT_LON_GAP[scale_code][1]
        x_min_dd = show_dms(x_min)
        y_min = hundred_dic[LAT_MIN] + (int(4/TFH_LAT_LON_GAP[scale_code][0])- num_left) * TFH_LAT_LON_GAP[scale_code][0]
        y_min_dd = show_dms(y_min)

        #右上角
        x_max = x_min + TFH_LAT_LON_GAP[scale_code][1]
        x_max_dd = show_dms(x_max)
        y_max = y_min + TFH_LAT_LON_GAP[scale_code][0]
        y_max_dd = show_dms(y_max)

        dic_jwd = {
            LON_MIN: x_min,
            LON_MIN_DD: x_min_dd,
            LON_MAX: x_max,
            LON_MAX_DD: x_max_dd,
            LAT_MIN: y_min,
            LAT_MIN_DD: y_min_dd,
            LAT_MAX: y_max,
            LAT_MAX_DD: y_max_dd
        }
        return dic_jwd

# 100万图幅号计算
def get_100w_jwd(tfh):
    hundred_a = ord(tfh[0]) - 64
    hundred_b = int(tfh[1:3])
    # 左下角坐标
    x_min = (hundred_b - 31) * 6
    x_min_dd = show_dms(x_min)
    y_min = (hundred_a - 1) * 4
    y_min_dd = show_dms(y_min)
    # 右上角坐标
    x_max = x_min + 6
    x_max_dd = show_dms(x_max)
    y_max = y_min + 4
    y_max_dd = show_dms(y_max)

    dic_jwd = {
        LON_MIN: x_min,
        LON_MIN_DD: x_min_dd,
        LON_MAX: x_max,
        LON_MAX_DD: x_max_dd,
        LAT_MIN: y_min,
        LAT_MIN_DD: y_min_dd,
        LAT_MAX: y_max,
        LAT_MAX_DD: y_max_dd
    }
    return dic_jwd

# 1:20万图幅号经纬度计算
def get_20w_jwd(tfh):
    scale_code = "R"
    dic_100w = get_100w_jwd(tfh[:3])  # 获取到百万分幅
    # 百万分幅左上角
    hundred_x_min = dic_100w[LON_MIN]
    hundred_y_max = dic_100w[LAT_MAX]

    # 20万分幅的数值
    twenty_num = int(tfh[3:])
    # 左下角
    x_min = hundred_x_min + ((twenty_num % 6) * TFH_LAT_LON_GAP[scale_code][1] - TFH_LAT_LON_GAP[scale_code][1])
    x_min_dd = show_dms(x_min)
    y_min = hundred_y_max - (int(twenty_num / 6) + 1) * TFH_LAT_LON_GAP[scale_code][0]
    y_min_dd = show_dms(y_min)
    # 右上角
    x_max = x_min + TFH_LAT_LON_GAP[scale_code][1]
    x_max_dd = show_dms(x_max)
    y_max = y_min + TFH_LAT_LON_GAP[scale_code][0]
    y_max_dd = show_dms(y_max)

    dic_jwd = {
        LON_MIN: x_min,
        LON_MIN_DD: x_min_dd,
        LON_MAX: x_max,
        LON_MAX_DD: x_max_dd,
        LAT_MIN: y_min,
        LAT_MIN_DD: y_min_dd,
        LAT_MAX: y_max,
        LAT_MAX_DD: y_max_dd
    }
    return dic_jwd

