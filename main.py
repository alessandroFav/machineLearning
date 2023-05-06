import requests

def get_prices():
    crypto_data = requests.get("https://api.telegram.org/bot6242272055:AAHe6DjncVtpP8CuJhTWl9iIccMfoj4QIr0/getUpdates").json()
    return crypto_data

