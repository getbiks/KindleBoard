import time
from renderer import render_dashboard


INTERVAL = 300   # 5 minutes


print("KindleBoard auto refresh started")


while True:

    try:
        render_dashboard()
        print("Dashboard updated")

    except Exception as e:
        print("Error:", e)


    time.sleep(INTERVAL)
