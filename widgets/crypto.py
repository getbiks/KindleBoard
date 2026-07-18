import requests
import time


cache = {
    "time": 0,
    "data": None
}


def get_crypto():

    # Cache for 10 minutes
    if cache["data"] and time.time() - cache["time"] < 600:
        return cache["data"]


    try:

        url = (
            "https://api.coingecko.com/api/v3/simple/price?"
            "ids=bitcoin,ethereum,ripple"
            "&vs_currencies=usd,inr"
        )


        response = requests.get(
            url,
            timeout=10
        )


        data = response.json()


        crypto = {
            "BTC": {
                "usd": data["bitcoin"]["usd"],
                "inr": data["bitcoin"]["inr"]
            },

            "ETH": {
                "usd": data["ethereum"]["usd"],
                "inr": data["ethereum"]["inr"]
            },

            "XRP": {
                "usd": data["ripple"]["usd"],
                "inr": data["ripple"]["inr"]
            }
        }


        cache["data"] = crypto
        cache["time"] = time.time()


        return crypto


    except Exception as e:

        return {
            "error": str(e)
        }



def crypto_text():

    data = get_crypto()


    if "error" in data:
        return "Crypto unavailable"


    lines = []


    for coin in ["BTC", "ETH", "XRP"]:

        value = data[coin]

        lines.append(
            coin
        )

        lines.append(
            f"${value['usd']:,.2f} / ₹{value['inr']:,.0f}"
        )


    return "\n".join(lines)
