from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import psutil
import shutil
import os

WIDTH = 800
HEIGHT = 600


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


def render_dashboard():

    image = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)

    title_font = ImageFont.load_default()
    text_font = ImageFont.load_default()

    # Border
    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=0)

    # Title
    draw.text((20, 20), "KindleBoard", fill=0, font=title_font)

    # Date
    now = datetime.now()
    draw.text((20, 45), now.strftime("%A, %d %B %Y"), fill=0, font=text_font)

    # Time
    draw.text((20, 75), now.strftime("%I:%M:%S %p"), fill=0, font=text_font)

    cpu = psutil.cpu_percent(interval=0.1)

    ram = psutil.virtual_memory().percent

    disk = shutil.disk_usage("/")
    disk_percent = (disk.used / disk.total) * 100

    temp = get_cpu_temp()

    y = 130

    draw.text((20, y), f"CPU Usage : {cpu:.1f}%", fill=0, font=text_font)
    y += 25

    draw.text((20, y), f"RAM Usage : {ram:.1f}%", fill=0, font=text_font)
    y += 25

    draw.text((20, y), f"Disk Usage: {disk_percent:.1f}%", fill=0, font=text_font)
    y += 25

    if temp:
        draw.text((20, y), f"CPU Temp : {temp:.1f} C", fill=0, font=text_font)

    os.makedirs("output", exist_ok=True)

    image.save("output/dashboard.png")
