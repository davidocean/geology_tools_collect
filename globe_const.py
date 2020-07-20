# 引入分数的概念
from fractions import Fraction

# 度分秒
ANGLE_DEGREE = "D"
ANGLE_MINUTE = "M"
ANGLE_SECOND = "S"

# 经纬度转十进制 错误信息
DMS_DECIMAL_ERROR = "错误，请检查经纬度数值是否正确。"
# 十进制转经纬度 错误信息
DECIMAL_DMS_ERROR = "错误，请检查数值是否正确。"
# 保留小数点后6位
DECIMAL_DMS_BAOLIU = "{:.6f}"
# DMS展示形式
DMS_FORMAT = "%s°%s′%s″"

# 图幅号计算
# 字典中包含比例尺和对应的纬度和经度间隔
TFH_LAT_LON_GAP = {
    "A": [4, 6],
    "B": [2, 3],
    "C": [1, Fraction(3 / 2)],
    "R": [Fraction(2 / 3), 1],
    "D": [Fraction(1, 3), 1 / 2],
    "E": [Fraction(1, 6), 1 / 4],
    "F": [Fraction(1, 12), Fraction(1, 8)],
    "G": [Fraction(1, 24), Fraction(1, 16)],
    "H": [Fraction(1, 48), Fraction(1, 32)],
    "I": [Fraction(1, 144), Fraction(1, 96)],
    "J": [Fraction(1, 288), Fraction(1, 192)],
    "K": [Fraction(1, 576), Fraction(1, 384)]
}

# 记录比例尺标记和对应比例尺的字典
TFH_SCALE_NAME = {
    "A": "1:100万",
    "B": "1:50万",
    "C": "1:25万",
    "R": "1:20万",
    "D": "1:10万",
    "E": "1:5万",
    "F": "1:2.5万",
    "G": "1:1万",
    "H": "1:5千",
    "I": "1:2千",
    "J": "1:1千",
    "K": "1:5百"
}

# kong
TFH_KONG = ""
TFH_SPACE = " "  # 空格
# 图幅号格式
TFH_FORMAT = "%s%s"
# 图幅号弹出框错误信息
TFH_MESSAGE_TITLE = "ERROR"
TFH_MESSAGE_INFO = "输入错误，请检查是否输入正确经纬度，经度范围（70~150），纬度范围（0~56）。"
# 图幅号展示table的Header
TFH_TABLE_HEADER = ["比例尺", "分幅标号", "图幅号"]
# 图幅号为12位的比例尺代码数组
TFH_12_LIST = ["J", "K"]
# 图幅号为10位的比例尺代码数组
TFH_10_LIST = ["B", "C", "D", "E", "F", "G", "H"]

# 经纬度最大最小值代码
LON_MIN = "lon_min"
LON_MIN_DD = "lon_min_dd"
LON_MAX = "lon_max"
LON_MAX_DD = "lon_max_dd"
LAT_MIN = "lat_min"
LAT_MIN_DD = "lat_min_dd"
LAT_MAX = "lat_max"
LAT_MAX_DD = "lat_max_dd"
# 中文名字典
LON_LAT_CN_DIC = {
    "lon_min": "经度最小值",
    "lon_max": "经度最大值",
    "lat_min": "纬度最小值",
    "lat_max": "纬度最大值",
    "lon_min_dd": "经度最小值(度分秒)",
    "lon_max_dd": "经度最大值(度分秒)",
    "lat_min_dd": "纬度最小值(度分秒)",
    "lat_max_dd": "纬度最大值(度分秒)"
}
# 展示出来的经纬度信息
LON_LAT_SHOW_FORMAT = "%s : %s (%s)"
# 后缀为dd结尾的
LON_LAT_ENDWITH_DD = "_dd"
