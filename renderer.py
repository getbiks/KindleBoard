from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import psutil
import shutil
import os


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
                return float(f.read()) / 1000.0
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


    # Fonts

    clock_font = get_font(56)
    date_font = get_font(20)
    text_font = get_font(18)


    # Outer border

    draw.rectangle(
        (5, 5, WIDTH - 5, HEIGHT - 5),
        outline=0,
        width=2
    )


    # Header

    now = datetime.now()

    draw.text(
        (30, 25),
        now.strftime("%I:%M %p"),
        font=clock_font,
        fill=0
    )

    draw.text(
        (35, 95),
        now.strftime("%A, %d %B %Y"),
        font=date_font,
        fill=0
    )


    # Cards

    card_y = 150

    draw_card(
        draw,
        30,
        card_y,
        350,
        250,
        "BatCave"
    )


    draw_card(
        draw,
        420,
        card_y,
        350,
        250,
        "Weather"
    )


    # BatCave Stats

    cpu = psutil.cpu_percent(interval=1)

    load = os.getloadavg()[0]

    ram = psutil.virtual_memory().percent

    disk = shutil.disk_usage("/")

    disk_percent = (disk.used / disk.total) * 100

    temp = get_cpu_temp()


    uptime = datetime.now() - datetime.fromtimestamp(
        psutil.boot_time()
    )

    days = uptime.days

    hours, remainder = divmod(
        uptime.seconds,
        3600
    )

    minutes = remainder // 60


    stats = [
        f"CPU      {cpu:.1f}%",
        f"Load     {load:.2f}",
        f"RAM      {ram:.1f}%",
        f"Disk     {disk_percent:.1f}%"
    ]


    if temp:
        stats.append(
            f"Temp     {temp:.1f} C"
        )


    stats.append(
        f"Uptime   {days}d {hours}h {minutes}m"
    )


    y = card_y + 50

    for item in stats:

        draw.text(
            (50, y),
            item,
            font=text_font,
            fill=0
        )

        y += 28



    # Weather placeholder

    draw.text(
        (450, 220),
        "Coming soon...",
        font=text_font,
        fill=0
    )


    os.makedirs(
        "output",
        exist_ok=True
    )


    image.save(
        "output/dashboard.png"
    )
