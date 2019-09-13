import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
from os import getenv
from configparser import ConfigParser #ini 파일 모듈

appdatafolder = getenv('localappdata') + "/whatclockisit/"
appdata = appdatafolder + "data/data.ini"

config = ConfigParser()
config.read(appdata)
data = config['main']

def wciitime():
    now = datetime.datetime.now()
    nowtime = now.strftime('%H%M')
    nowtime = str(nowtime)
    if nowtime == '0000':
        showtime = "지금은 자정이야"
        return showtime
    elif nowtime == '1200':
        showtime = "지금은 정오야"
        return showtime
    else:
        hour = int(nowtime[0:2])
        if hour == 00:
            hour = 24
        minu = int(nowtime[2:4])
        time_map_hour = {0: "", 1: "한", 2: "두", 3: "세", 4: "네", 5: "다섯", 6: "여섯", 7: "일곱", 8: "여덟", 9: "아홉"}
        time_map_minu = {0: "", 1: "일", 2: "이", 3: "삼", 4: "사", 5: "오", 6: "육", 7: "칠", 8: "팔", 9: "구"}

        # 시간
        if hour >= 21: showhour = "밤 "
        elif hour >= 17: showhour = "저녁 "
        elif hour >= 15: showhour = "오후 "
        elif hour >= 11: showhour = "점심 "
        elif hour >= 7: showhour = "아침 "
        elif hour >= 5: showhour = "이른 아침 "
        elif hour >= 3: showhour = "새벽 "
        elif hour >= 1: showhour = "늦은 밤 "
        elif hour >= 0: showhour = "밤 "

        if hour > 12: hour = hour - 12

        if hour >= 10:
            hour = hour - 10
            showhour = showhour + "열" + time_map_hour[hour] + " 시 "
        else:
            showhour = showhour + time_map_hour[hour] + " 시 "

        # 분 구문
        showminu = ""
        if minu >= 10:
            if minu > 20:
                minu_ten = int(str(minu)[0])
                showminu = time_map_minu[minu_ten] + "십"
            else:
                showminu = "십"
            minu_one = int(str(minu)[1])
            showminu = showminu + time_map_minu[minu_one] + " 분"
        elif minu > 0:
            minu_one = int(str(minu)[0])
            showminu = showminu + time_map_minu[minu_one] + " 분"
        else:
            showminu = showminu + "정각"

        # 최종 출력 구문
        showtime = showhour + showminu + "이야."
        return showtime

class no_online(Exception):
    pass

def wciitext():
    now = datetime.datetime.now()
    nowdate = now.strftime('%H')
    time_now = int(nowdate) // 2 + 1
    time_now = time_now
    data['online'] = "connect"
    with open(appdata, 'w') as main:
        config.write(main)
    try:
        if data['online'] == "offline":
            raise no_online()
        else:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            url = urlopen(f'http://hyuns.space/api/hanguel/{time_now}/index.php', timeout=3)
            #url = urlopen(f'http://localhost:8080/api/{time_now}/index.php', timeout=3)
            soup = BeautifulSoup(url, "lxml")
            soup = str(soup.body)
            soup = soup.replace("<body>", "")
            soup = soup.replace("</body>", "")
            soup = soup.strip()
            showtext = soup
            return showtext

    except Exception as e:
        print(f"서버연결 오류발생 : {e}")
        data['online'] = "offline"
        with open(appdata, 'w') as main:
            config.write(main)

        if time_now == 1:
            showtext = "좋은 꿈 꿔"
        elif time_now == 2:
            showtext = "아직 안 자고 뭐해?"
        elif time_now == 3:
            showtext = "오늘도 좋은 아침"
        elif time_now == 4:
            showtext = "잠은 잘 잤니?"
        elif time_now == 5:
            showtext = "아침은 먹었니?"
        elif time_now == 6:
            showtext = "지금 뭐해?"
        elif time_now == 7:
            showtext = "뭐하고 있어?"
        elif time_now == 8:
            showtext = "기재기 한 번 어때?"
        elif time_now == 9:
            showtext = "힘들지 않아?"
        elif time_now == 10:
            showtext = "오늘 저녁 맛있었어?"
        elif time_now == 11:
            showtext = "지금 뭐해?"
        elif time_now == 12:
            showtext = "굿나잇!"

    return showtext

if __name__ == "__main__":
    print(wciitext())
    print(wciitime())
