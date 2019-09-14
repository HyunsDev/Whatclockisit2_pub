# -*- coding:utf-8 -*-
from ctypes import windll #바탕화면 등록 모듈
from datetime import datetime
from os import path, getenv #파일 위치
from time import sleep #sleep
import datetime #현재 시간 모듈
from configparser import ConfigParser #ini 파일 모듈
from PIL import Image, ImageDraw, ImageFont #이미지 제작 모듈
from whatclockisit2_time import wciitime, wciitext #문구 모듈

#appdata 불러오기
appdatafolder = getenv('localappdata') + "/whatclockisit/"
appdatafolder = appdatafolder.replace("\\","/").replace("\\","/").replace("\\","/").replace("\\","/")
appdata = appdatafolder + "data/data.ini"
appfont = appdatafolder + "font/"
appimage = appdatafolder + "image/"
applog = appdatafolder + "log/"
apptemp = appdatafolder + "temp/"

dimage = appimage + "whatclockisit2_wallpaper_source.png"
dffile = "NotoSansCJKkr-Black.otf"
dffolder = appfont

config = ConfigParser()
config.read(appdata)
data = config['main']

#ini 변경 함수
def iniup(ini_key, ini_value):
    data[ini_key] = ini_value
    with open(appdata, 'w') as main:
        config.write(main)



#에러 설정
class wallpaper_error(Exception):
    def __str__(self):
        return "배경화면 불러오기 오류"

class font_error(Exception):
    def __str__(self):
        return "폰트 불러오기 오류"

# 배경화면 생성 및 등록 함수 (메인 함수)
def wcii_wallpaper(wciitext):
    nowtime = wciitime()
    nowtext = wciitext
    ws = data['wallpaper_source']
    ffolder = data['fontfolder']
    ffile = data['fontfile']
    fsize = int(data['fontsize'])
    sW = int(data['screen_W'])
    sH = int(data['screen_H'])
    cpX = int(data['clock_position_X'])
    cpY = int(data['clock_position_Y'])
    tf = data['text_fill']
    ta = data['text_align']
    wt = apptemp + "temp.png"
    to = data['text_on']

    if to == "off": #문구 표시 해제
        msg = str(nowtime)
    else:
        msg = str(nowtext) + "\n" + str(nowtime)

    try:
        imagepath = Image.open(ws)
    except:
        imagepath = Image.open(dimage)
        print("이미지 불러오기 오류 발생")
        iniup('wallpaper_source', dimage)

    font = ImageFont.truetype(path.join(ffolder, ffile), fsize)
    draw = ImageDraw.Draw(imagepath)
    w, h = draw.textsize(msg, font=font)

    draw.text(((sW - w) / 2 + int(cpX), (sH - h ) / 2 - 50 + int(cpY)), msg, fill=tf, font=font, align=ta)
    imagepath.save(wt)
    imagepath = path.normpath(wt)
    windll.user32.SystemParametersInfoW(20, 0, imagepath, 0)

    print("<바탕화면 새로고침>")

def stop_wallpaper():
    ws = data['wallpaper_source']
    ffolder = data['fontfolder']
    ffile = data['fontfile']
    fsize = int(data['fontsize'])
    sW = int(data['screen_W'])
    sH = int(data['screen_H'])
    cpX = int(data['clock_position_X'])
    cpY = int(data['clock_position_Y'])
    tf = data['text_fill']
    ta = data['text_align']
    wt = apptemp + "close.png"
    to = data['text_on']
    msg = "지금몇시계 영업 종료"
    imagepath = Image.open(ws)
    font = ImageFont.truetype(path.join(ffolder, ffile), fsize)
    draw = ImageDraw.Draw(imagepath)
    w, h = draw.textsize(msg, font=font)

    draw.text(((sW - w) / 2 + int(cpX), (sH - h) / 2 - 50 + int(cpY)), msg, fill=tf, font=font,
              align=ta)
    savedimage = wt
    imagepath.save(savedimage)
    imagepath = path.normpath(savedimage)
    windll.user32.SystemParametersInfoW(20, 0, imagepath, 0)



wciitextnow = wciitext()

lognow = datetime.datetime.now()
with open(applog + "wakeup.log", "a") as f:
    f.write("%s년 %s월 %s일 %s시 %s분 %s초에 지금몇시계 일어났어요!\n" % (lognow.year,lognow.month,lognow.day,lognow.hour,lognow.minute,lognow.second))
print("wcii 코어 일어났어요!")

#메인 코드
iniup("clock_on", "oning")
#try: #시계가 종료될 정도의 심한 오류
if True:
    while True: #반복
        #try: #시계가 종료되지 않을 정도인 실행 에러
        if True:
        #메인 코드 시작
            now = datetime.datetime.now()

            if data["clock_on"] == "oning":
                wcii_wallpaper(wciitext())
                iniup("clock_on", "on")
                print("지금몇시계 영업시작")
                sleep(0.1)

            elif data["clock_on"] == "offing":  # 종료ing
                stop_wallpaper()
                iniup("clock_on", "off")
                print("지금몇시계 영업종료")

            elif data["clock_on"] == "kill":
                stop_wallpaper()
                iniup("clock_on", "die")
                print("지금몇시계 폐업")
                sleep(0.1)
                break

            elif data["clock_on"] == "off":
                sleep(0.9)

            else:
                nowmin = now.strftime('%M') #30분마다 문구 불러오기
                if nowmin == '59':
                    korean_nowtext = wciitext()
                elif nowmin == '29':
                    korean_nowtext = wciitext()

                if data["reflesh"] == "yes": #새로고침
                    sleep(0.5)
                    wciitextnow = wciitext()
                    wcii_wallpaper(wciitextnow)
                    iniup('reflesh', "no")

                if now.strftime('%S') == "00": #실행
                    wcii_wallpaper(wciitextnow)
                    print("바탕화면 변경 완료 (%s)" % (wciitime()))

            iniup('live_check', 'live')
            sleep(0.9)

'''
        #메인 코드 끝
        except Exception as e:
            lognow = datetime.datetime.now()
            with open(applog + "error.log", "a") as f:
                f.write(f"{lognow.year}년 {lognow.month}월 {lognow.day}일 {lognow.hour}시 {lognow.minute}분 {lognow.second}초 오류 내용 : {e}\n")
            print("실행 에러 : " + str(e))
            pass

except Exception as e:
    lognow: datetime = datetime.datetime.now()
    with open(applog + "error.log", "a") as f:
        f.write(f"{lognow.year}년 {lognow.month}월 {lognow.day}일 {lognow.hour}시 {lognow.minute}분 {lognow.second}초 심각한 오류 내용 : {e}\n")
    print("심각한 에러 : " + str(e))
'''
