import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog,QMessageBox
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from homepage import Ui_MainWindow
from degree_change import Ui_Dialog as degree_change_dialog
from tfh_calc_dialog import Ui_Dialog as tfh_dialog
from tools_collect import *
from globe_const import *


# 主界面
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# 十进制与度分秒互相转化的功能界面
class degress_change_window(QDialog, degree_change_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.dms2decimal)
        self.pushButton.clicked.connect(self.decimal2dms)

    #经纬度转十进制
    def dms2decimal(self):
        d = self.lineEdit_3.text()
        m = self.lineEdit_4.text()
        s = self.lineEdit_5.text()
        result = show_demical(d,m,s)
        if not result:
            self.lineEdit_6.setText(DMS_DECIMAL_ERROR)
        else:
            self.lineEdit_6.setText(result)
        # 控制重绘
        self.repaint()

    #十进制转经纬度
    def decimal2dms(self):
        temp = self.lineEdit.text()
        result = show_dms(temp)
        if not result :
            self.lineEdit_2.setText(DECIMAL_DMS_ERROR)
        else:
            self.lineEdit_2.setText(result)

        #控制重绘
        self.repaint()


# 图幅号计算功能界面
class tfh_calc_window(QDialog, tfh_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.tfh_calc)#计算图幅号方法
        self.pushButton_2.clicked.connect(self.coordinate_calc)#根据图幅号计算四角坐标方法

    #根据 经纬度计算图幅号
    def tfh_calc(self):
        self.plainTextEdit.clear()
        lon = self.lineEdit.text()
        lat = self.lineEdit_2.text()
        result = show_tfh(lon,lat)
        if not result:
            self.plainTextEdit.setPlainText(TFH_MESSAGE_INFO)
        else:
            for i in result:
                self.plainTextEdit.appendPlainText(i)
        self.repaint()

    #根据图幅号计算四角坐标
    def coordinate_calc(self):
        self.plainTextEdit_2.clear()
        tfh = self.lineEdit_3.text()
        result_list = show_tfh_to_jwd(tfh)
        for i in result_list:
            self.plainTextEdit_2.appendPlainText(i)
        self.repaint()





# 展示角度转换工具
def show_degree(self):
    window_degreee_change.show()


# 展示图幅号计算工具
def show_tfh_calc_tool(self):
    window_tfh_calc.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    # 初始化经纬度计算界面
    window_degreee_change = degress_change_window()
    window.pushButton.clicked.connect(show_degree)
    # 初始化图幅号计算界面
    window_tfh_calc = tfh_calc_window()
    window.pushButton_2.clicked.connect(show_tfh_calc_tool)

    sys.exit(app.exec_())
