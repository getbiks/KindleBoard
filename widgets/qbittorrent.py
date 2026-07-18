import qbittorrentapi
import time


QBIT_HOST = "192.168.1.2"
QBIT_PORT = 8181

# Change these if your qBittorrent login is different
USERNAME = "admin"
PASSWORD = ""


cache = {
    "time": 0,
    "data": None
}


def format_speed(speed):

    if speed >= 1024 * 1024:
        return f"{speed / 1024 / 1024:.1f} MB/s"

    if speed >= 1024:
        return f"{speed / 1024:.1f} KB/s"

    return f"{speed} B/s"



def get_qbittorrent():

    if cache["data"] and time.time() - cache["time"] < 15:
        return cache["data"]


    try:

        client = qbittorrentapi.Client(
            host=QBIT_HOST,
            port=QBIT_PORT,
            username=USERNAME,
            password=PASSWORD
        )


        client.auth_log_in()


        torrents = client.torrents_info(
            status_filter="downloading"
        )


        transfer = client.transfer_info()


        data = {
            "count": len(torrents),
            "download": transfer.dl_info_speed,
            "upload": transfer.up_info_speed,
            "torrent": None
        }


        if torrents:

            torrent = torrents[0]

            data["torrent"] = {
                "name": torrent.name,
                "progress": torrent.progress * 100,
                "eta": torrent.eta
            }


        cache["data"] = data
        cache["time"] = time.time()


        return data


    except Exception as e:

        return {
            "error": str(e)
        }



def qbittorrent_text():

    data = get_qbittorrent()


    if "error" in data:

        return "qBittorrent\nOffline"


    lines = [
        f"Active: {data['count']}",
        f"↓ {format_speed(data['download'])}",
        f"↑ {format_speed(data['upload'])}"
    ]


    if data["torrent"]:

        torrent = data["torrent"]

        lines.append("")
        lines.append(
            torrent["name"][:28]
        )

        lines.append(
            f"{torrent['progress']:.0f}%"
        )


    return "\n".join(lines)
