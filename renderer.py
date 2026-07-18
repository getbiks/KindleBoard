from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import psutil
import shutil
import os

from widgets.weather import weather_text
from widgets.qbittorrent import qbittorrent_text
from widgets.crypto import crypto_text


WIDTH = 800
HEIGHT = 600

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def get_font(size):
    return ImageFont.truetype(FONT_PATH, size)


def get_cpu_temp():

    paths = [
        "/sys/class/thermal/thermal_zone0/temp",
        "/sys/class/hwmon/hwmon0/temp1_input"
    ]

    for path in paths:
        try:
            with open(path) as f:
                return float(f.read()) / 1000
        except:
            pass

    return None



def draw_card(draw, x, y, w, h, title):

    draw.rectangle(
        (x, y, x + w, y + h),
        outline=0,
        width=2
    )

    draw.text(
        (x + 15, y + 10),
        title,
        font=get_font(20),
        fill=0
    )



def render_dashboard():

    image = Image.new(
        "L",
        (WIDTH, HEIGHT),
        255
    )

    draw = ImageDraw.Draw(image)


    clock_font = get_font(56)
    date_font = get_font(20)
    text_font = get_font(18)



    # Outer border

    draw.rectangle(
        (5, 5, WIDTH-5, HEIGHT-5),
        outline=0,
        width=2
    )



    # Header

    now = datetime.now()

    draw.text(
        (30, 20),
        now.strftime("%I:%M %p"),
        font=clock_font,
        fill=0
    )


    draw.text(
        (35, 90),
        now.strftime("%A, %d %B %Y"),
        font=date_font,
        fill=0
    )



    # Cards

    draw_card(
        draw,
        30,
        150,
        350,
        170,
        "BatCave"
    )


    draw_card(
        draw,
        420,
        150,
        350,
        170,
        "Weather"
    )


    draw_card(
        draw,
        30,
        350,
        350,
        200,
        "qBittorrent"
    )


    draw_card(
        draw,
        420,
        350,
        350,
        200,
        "Crypto"
    )



    # ----------------
    # BatCave Stats
    # ----------------

    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory().percent

    disk = shutil.disk_usage("/")

    disk_percent = (
        disk.used / disk.total
    ) * 100


    temp = get_cpu_temp()


    uptime = datetime.now() - datetime.fromtimestamp(
        psutil.boot_time()
    )


    stats = [
        f"CPU    {cpu:.1f}%",
        f"RAM    {ram:.1f}%",
        f"Disk   {disk_percent:.1f}%"
    ]


    if temp:
        stats.append(
            f"Temp   {temp:.1f} C"
        )


    stats.append(
        f"Up     {uptime.days}d"
    )


    y = 200

    for item in stats:

        draw.text(
            (55, y),
            item,
            font=text_font,
            fill=0
        )

        y += 22



    # ----------------
    # Weather
    # ----------------

    weather = weather_text()

    y = 200

    for item in weather.split("\n"):

        draw.text(
            (450, y),
            item,
            font=text_font,
            fill=0
        )

        y += 28



    # ----------------
    # qBittorrent
    # ----------------

    qbit = qbittorrent_text()

    y = 410

    for item in qbit.split("\n"):

        draw.text(
            (55, y),
            item,
            font=text_font,
            fill=0
        )

        y += 24



    # ----------------
    # Crypto
    # ----------------

    crypto = crypto_text()

    y = 405

    for item in crypto.split("\n"):

        draw.text(
            (450, y),
            item,
            font=text_font,
            fill=0
        )

        y += 22



    # Save image

    os.makedirs(
        "output",
        exist_ok=True
    )


    image.save(
        "output/dashboard.png"
    )
