import requests
import logging

__client_id = ""
__client_secret = ""


def init(client_id, client_secret):
    if not client_id:
        raise Exception("Bad client_id")

    if not client_secret:
        raise Exception("Bad client_secret")

    global __client_id
    __client_id = client_id
    global __client_secret
    __client_secret = client_secret


def send(params):
    api_url = "https://api.notificationapi.com/" + __client_id + "/sender"
    response = requests.post(
        api_url,
        auth=requests.auth.HTTPBasicAuth(
            username=__client_id, password=__client_secret
        ),
        json=params,
    )
    if response.status_code == 202:
        logging.warning("NotificationAPI request ignored. params: %s", params)
    if response.status_code == 500:
        logging.error(
            "NotificationAPI request failed. Response: %s. params: %s",
            response.text,
            params,
        )
