import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from os import getenv
from configparser import ConfigParser  # ini 파일 모듈
from urllib.request import urlopen  # 서버

# appdata 불러오기
appdatafolder = getenv('localappdata') + "/whatclockisit/"
appdatafolder = appdatafolder.replace("\\", "/").replace("\\", "/").replace("\\", "/").replace("\\", "/")
appdata = appdatafolder + "data/data.ini"
appfont = appdatafolder + "font/"
appimage = appdatafolder + "image/"
applog = appdatafolder + "log/"
apptemp = appdatafolder + "temp/"

# data.ini 불러오기
config = ConfigParser()
config.read(appdata)
data = config['main']


# ini 변경 함수
def iniup(ini_key, ini_value):
    data[ini_key] = ini_value
    with open(appdata, 'w') as main:
        config.write(main)


def check_live():
    iniup('live_check', 'check')
    time.sleep(1)
    if data['live_check'] == "check":
        return "live"
    else:
        return "dead"

if check_live() == "live":
    print("살아있음")
else:
    print("죽어있음")


class wcii_clock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        G_wall = QImage("resource/gui_wallpaper.png")
        G_palette = QPalette()
        G_palette.setBrush(10, QBrush(G_wall))
        self.setPalette(G_palette)

        grid = QGridLayout()
        grid.addWidget(self.wcii_groupbox(), 0, 0, 1, 1)
        grid.addWidget(self.custom_groupbox(), 0, 1, 3, 1)
        grid.addWidget(self.other_groupbox(), 1, 0, 2 ,1)

        self.setLayout(grid)

        status = QStatusBar().showMessage("조금만 기다려 주세요")

        self.setWindowTitle('지금몇시계 베타')
        # self.setWindowIcon(QIcon('resource/whatclockisit_ico.png'))
        self.setWindowIcon(QIcon('resource/wcii_icon2.png'))
        self.setFixedSize(800, 500)
        self.center()
        self.show()

    def wcii_groupbox(self):

        groupbox = QGroupBox('지금몇시계')

        wcii_box = QVBoxLayout()

        # 지금 몇시계 활성화
        clock_on_label = QLabel("시계 활성화", self)
        clock_on_group = QButtonGroup(self)

        self.clock_on_rb = QRadioButton("활성화")
        self.clock_off_rb = QRadioButton("비활성화")
        clock_on_group.addButton(self.clock_on_rb)
        clock_on_group.addButton(self.clock_off_rb)

        if check_live() != "live":
            self.clock_off_rb.setChecked(True)
        else:
            self.clock_on_rb.setChecked(True)

        self.clock_on_rb.clicked.connect(self.clock_on)
        self.clock_off_rb.clicked.connect(self.clock_off)

        clock_box = QHBoxLayout()
        clock_box.addWidget(clock_on_label)
        clock_box.addWidget(self.clock_on_rb)
        clock_box.addWidget(self.clock_off_rb)

        wcii_box.addLayout(clock_box)

        # 문구 표시 활성화
        text_on_label = QLabel("문구 표시", self)
        text_on_group = QButtonGroup(self)
        text_on = QRadioButton("활성화")
        text_off = QRadioButton("비활성화")
        text_on_group.addButton(text_on)
        text_on_group.addButton(text_off)
        if data['text_on'] == "off":
            text_off.setChecked(True)
        else:
            text_on.setChecked(True)

        text_on.clicked.connect(self.text_on)
        text_off.clicked.connect(self.text_off)

        text_box = QHBoxLayout()
        text_box.addWidget(text_on_label)
        text_box.addWidget(text_on)
        text_box.addWidget(text_off)

        wcii_box.addLayout(text_box)
        #

        groupbox.setLayout(wcii_box)

        return groupbox

    def clock_on(self):  # 시계 켜기
        if check_live() != "live":
            QMessageBox.information(self, "코어가 꺼져있어요", "지금몇시계 코어를 실행해주세요!")
            self.clock_off_rb.setChecked(True)
        else:
            iniup("clock_on", "oning")
            time.sleep(0.1)

    def clock_off(self):  # 시계 대기 상태
        if check_live() != "live":
            QMessageBox.information(self, "코어가 이미 꺼져있어요", "코어가 이미 꺼져있어요")
        else:
            iniup("clock_on", "offing")
            time.sleep(0.1)

    def text_on(self):
        iniup("text_on", "on")
        self.reflesh()

    def text_off(self):
        iniup("text_on", "off")
        self.reflesh()

    def custom_groupbox(self):
        groupbox = QGroupBox('커스텀마이징')

        self.wallpaper_lable = QLabel("배경사진")
        self.wallpaper_url = QLineEdit(data['wallpaper_source'])
        self.wallpaper_button = QPushButton("파일 선택")
        self.wallpaper_button.clicked.connect(self.select_wallpaper)

        wallpaper_box = QHBoxLayout()
        wallpaper_box.addWidget(self.wallpaper_lable)
        wallpaper_box.addWidget(self.wallpaper_url)
        wallpaper_box.addWidget(self.wallpaper_button)

        font_url = data['fontfolder'] + "/" + data['fontfile']
        self.font_lable = QLabel("폰트")
        self.font_url = QLineEdit(font_url)
        self.font_button = QPushButton("파일 선택")
        self.font_button.clicked.connect(self.select_font)

        font_box = QHBoxLayout()
        font_box.addWidget(self.font_lable)
        font_box.addWidget(self.font_url)
        font_box.addWidget(self.font_button)

        self.clock_position_label = QLabel("시계 위치(중앙으로부터)", self)

        self.clock_position_X = QSpinBox()
        self.clock_position_X.setRange(-4096, 4096)
        self.clock_position_X.setValue(int(data['clock_position_X']))
        self.clock_position_X.valueChanged.connect(self.clock_pos_X_set)

        self.clock_position_Y = QSpinBox()
        self.clock_position_Y.setRange(-2160, 2160)
        self.clock_position_Y.setValue(int(data['clock_position_Y']))
        self.clock_position_Y.valueChanged.connect(self.clock_pos_Y_set)

        clock_position_box = QHBoxLayout()
        clock_position_box.addWidget(self.clock_position_label)
        clock_position_box.addWidget(self.clock_position_X)
        clock_position_box.addWidget(self.clock_position_Y)

        self.fontsize_label = QLabel("폰트 크기")
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(10, 200)
        self.fontsize_spin.setValue(int(data['fontsize']))
        self.fontsize_spin.valueChanged.connect(self.fontsize_set)

        fontsize_box = QHBoxLayout()
        fontsize_box.addWidget(self.fontsize_label)
        fontsize_box.addWidget(self.fontsize_spin)

        textalign_label = QLabel("글씨 정렬", self)  # 아직 지원하지 않음
        textalign_left = QRadioButton("왼쪽 정렬")
        textalign_center = QRadioButton("가운데 정렬")
        textalign_right = QRadioButton("오른쪽 정렬")

        if data['text_align'] == "left":
            textalign_left.setChecked(True)
        elif data['text_align'] == "right":
            textalign_right.setChecked(True)
        else:
            textalign_center.setChecked(True)

        textalign_left.clicked.connect(self.ta_l)
        textalign_center.clicked.connect(self.ta_c)
        textalign_right.clicked.connect(self.ta_r)

        textalign_box = QHBoxLayout()
        textalign_box.addWidget(textalign_label)
        textalign_box.addWidget(textalign_left)
        textalign_box.addWidget(textalign_center)
        textalign_box.addWidget(textalign_right)
        #

        self.screensize_label = QLabel("화면크기(너비x높이)")
        self.screensize_W = QSpinBox()
        self.screensize_W.setRange(100, 4096)
        self.screensize_W.setValue(int(data['screen_W']))
        self.screensize_W.valueChanged.connect(self.screen_W_set)

        self.screensize_H = QSpinBox()
        self.screensize_H.setRange(100, 2160)
        self.screensize_H.setValue(int(data['screen_H']))
        self.screensize_H.valueChanged.connect(self.screen_H_set)

        screensize_box = QHBoxLayout()
        screensize_box.addWidget(self.screensize_label)
        screensize_box.addWidget(self.screensize_W)
        screensize_box.addWidget(self.screensize_H)

        custom_box = QVBoxLayout()
        custom_box.addLayout(wallpaper_box)
        custom_box.addLayout(font_box)
        custom_box.addLayout(clock_position_box)
        custom_box.addLayout(fontsize_box)
        custom_box.addLayout(textalign_box)
        custom_box.addLayout(screensize_box)

        groupbox.setLayout(custom_box)
        return groupbox

    def clock_pos_X_set(self):
        val = self.clock_position_X.value()
        iniup('clock_position_x', str(val))

    def clock_pos_Y_set(self):
        val = self.clock_position_Y.value()
        iniup('clock_position_y', str(val))

    def fontsize_set(self):
        iniup('fontsize', str(self.fontsize_spin.value()))

    def ta_l(self):
        iniup('text_align', 'left')
        self.reflesh()

    def ta_c(self):
        iniup('text_align', 'center')
        self.reflesh()

    def ta_r(self):
        iniup('text_align', 'right')
        self.reflesh()

    def select_wallpaper(self):
        title = "배경사진을 골라주세요"
        filter = "사진 파일(*.png)"
        wp_link = QFileDialog.getOpenFileName(self, title, None, filter)
        if wp_link[0] != "":
            wp_link = wp_link[0]
            iniup('wallpaper_source', wp_link)
            self.wallpaper_url.setText(wp_link)

    def select_font(self):
        title = "폰트파일을 골라주세요"
        filter = "폰트파일(*.ttf *.otf)"
        ff_link = QFileDialog.getOpenFileName(self, title, None, filter)
        print(ff_link)
        if ff_link[0] != "":
            ff_link = ff_link[0]
            sp = ff_link.rfind("/")
            ffile = ff_link[sp + 1:]
            ffolder = ff_link[:sp]
            iniup('fontfile', ffile)
            iniup('fontfile', ffolder)
            self.font_url.setText(ff_link)
            self.reflesh()

    def other_groupbox(self):
        groupbox = QGroupBox("그 외의 것들")

        # 테스트 전용 구문

        self.test_button = QPushButton("라이브 테스트")
        self.test_button.clicked.connect(self.test)

        test_box = QHBoxLayout()
        test_box.addWidget(self.test_button)

        self.notice_label = QLabel("시계위치와 폰트크기, 시간데 보정과 화면크기는\n새로고침을 눌러주세요!")

        notice_box = QHBoxLayout()
        notice_box.addWidget(self.notice_label)

        # 테스트 전용 구문 끝

        self.reflesh_button = QPushButton("적용하고 새로고침")
        self.reflesh_button.clicked.connect(self.reflesh)

        reflesh_box = QHBoxLayout()
        reflesh_box.addWidget(self.reflesh_button)

        self.kill_button = QPushButton("지금몇시계 내쫒기")
        self.kill_button.clicked.connect(self.kill)

        kill_box = QHBoxLayout()
        kill_box.addWidget(self.kill_button)

        custom_box = QVBoxLayout()

        # 테스트 전용 구문
        custom_box.addLayout(test_box)
        # 테스트 전용 구문 끝

        # custom_box.addLayout(discord_box)
        custom_box.addLayout(notice_box)
        custom_box.addLayout(reflesh_box)
        custom_box.addLayout(kill_box)
        groupbox.setLayout(custom_box)
        return groupbox

    def kill(self):

        reply = QMessageBox.question(self, '지금몇시계를 내쫒으실 건가요...?', "시계를 단순히 끄고 싶다면 종료하지말고 비활성화를 해주세요.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
                iniup("clock_on", "kill")
                self.clock_off_rb.setChecked(True)
                QMessageBox.information(self, "지금몇시계를 종료했습니다", "시계를 켜실려면 다시 코어를 실행해주세요!")
        else:
            QMessageBox.information(self, "시계가 이미 꺼져있어요..", "시계가 이미 꺼져있어요..")

    def test(self):
        if check_live() == "live":
            print("코어가 살아있음")
        else:
            print("코어가 죽었거나 응답하지 않음")

    def screen_W_set(self):
        val = self.screensize_W.value()
        iniup('screen_W', str(val))

    def screen_H_set(self):
        val = self.screensize_H.value()
        iniup('screen_H', str(val))

    def reflesh(self):  # 시계 새로고침
        if check_live() != "live":
            QMessageBox.information(self, "코어가 꺼져있어요", "지금몇시계 코어를 실행해주세요!")
        else:
            iniup("reflesh", "yes")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = wcii_clock()
    sys.exit(app.exec_())
