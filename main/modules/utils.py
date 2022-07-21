from math import floor
import os
from main import queue
import cv2, random
from string import ascii_letters, ascii_uppercase, digits
from pyrogram.types import Message, MessageEntity

def get_duration(file):
    data = cv2.VideoCapture(file)

    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    return int(frames / fps)


def get_screenshot(file):
    cap = cv2.VideoCapture(file)
    name = "./" + "".join(random.choices(ascii_uppercase + digits,k = 10)) + ".jpg"

    total_frames = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
    frame_num = random.randint(0,total_frames)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num-1)
    res, frame = cap.read()

    cv2.imwrite(name, frame)
    cap.release()
    #cv2.destroyAllWindows()
    return name

def get_filesize(file):
    x = os.path.getsize(file)
    x = round(x/(1024*1024))
    x = f"{str(round(x/1024,2))} GB" if x > 1024 else f"{str(x)} MB"
    return x

def get_epnum(name):
    x = name.split(" - ")[-1].strip()
    x = x.split(" ")[0]
    x = x.strip()
    return x

def format_time(time):
    min = floor(time/60)
    sec = round(time-(min*60))

    time = f"{str(min)}:{str(sec)}"
    return time

def format_text(text):
    ftext = "".join(
        x if x in ascii_letters or x == " " or x in digits else " "
        for x in text
    )

    while "  " in ftext:
        ftext = ftext.replace("  "," ")
    return ftext

def episode_linker(f,en,text,link):
    ent = en
    off = len(f) + 2
    length = len(text)
    new = MessageEntity(type="text_link",offset=off,length=length,url=link)
    ent.append(new)
    return ent

def tags_generator(title):
    x = "#" + title.replace(" ","_")
    
    while x[-1] == "_":
        x = x[:-1]
    return x

async def status_text(text):
    stat = """
⭐️ **Status :** {}

⏳ **Queue :** 

{}
"""

    queue_text = "".join(
        "📌 "
        + i["title"].replace(".mkv", "").replace(".mp4", "").strip()
        + "\n"
        for i in queue
    )

    if not queue_text:
        queue_text = "❌ Empty"

    return stat.format(
        text,
        queue_text
    )


def get_progress_text(name,status,completed,speed,total,enco=False):
    text = """Name: {}
{}: {}%
⟨⟨{}⟩⟩
{} of {}
Speed: {}
ETA: {}
    """

    text2 = """Name: {}
{}: {}%
⟨⟨{}⟩⟩
Speed: {}
ETA: {}
    """

    if enco == False:
        total = str(total)
        completed = round(completed*100,2)
        size, forma = total.split(' ')
        if forma == "MiB":
            size = int(round(float(size)))
        elif forma == "GiB":
            size = int(round(float(size)*1024,2))

        percent = completed
        speed = round(float(speed)/1024) #kbps

        if speed == 0:
            speed = 0.1

        ETA = round((size - ((percent/100)*size))/(speed/1024))

        if ETA > 60:
            x = floor(ETA/60)
            y = ETA-(x*60)

            if x > 60:
                z = floor(x/60)
                x = x-(z*60)
                ETA = f"{str(z)} Hour {str(x)} Minute"
            else:
                ETA = f"{str(x)} Minute {str(y)} Second"
        else:
            ETA = f"{str(ETA)} Second"  

        if speed > 1024:
            speed = f"{str(round(speed/1024))} MB"
        else:
            speed = f"{str(speed)} KB"

        completed = round((percent/100)*size)

        if completed > 1024:
            completed = str(round(completed/1024,2)) + " GB"
        else:
            completed = str(completed) + " MB"

        size = str(round(size/1024,2)) + " GB" if size > 1024 else str(size) + " MB"
        fill = "▪️"
        blank = "▫️"
        bar = ""

        bar += round(percent/10)*fill
        bar += round(((20 - len(bar))/2))*blank


        speed += "/sec"
        text = text.format(
            name,
            status,
            percent,
            bar,
            completed,
            size,
            speed,
            ETA
        )
        return text

    elif enco == True:
        speed = float(speed)
        if speed == 0:
            speed = 0.01

        remaining = floor(int(total)-completed)
        ETA = floor(remaining / speed)

        if ETA > 60:
            x = floor(ETA/60)
            y = ETA-(x*60)

            if x > 60:
                z = floor(x/60)
                x = x-(z*60)
                ETA = str(z) + " Hour " + str(x) + " Minute"
            else:
                ETA = str(x) + " Minute " + str(y) + " Second"
        else:
            ETA = str(ETA) + " Second"

        percent = round((completed/total)*100,2)

        fill = "▪️"
        blank = "▫️"
        bar = ""

        bar += round(percent/10)*fill
        bar += round(((20 - len(bar))/2))*blank

        speed = str(speed) + "x"

        text2 = text2.format(
            name,
            status,
            percent,
            bar,
            str(speed),
            ETA
        )
        return text2