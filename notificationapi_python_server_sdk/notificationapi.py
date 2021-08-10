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


def request(method, uri, data):
    api_url = "https://api.notificationapi.com/" + __client_id + "/" + uri
    response = requests.request(
        method,
        api_url,
        auth=requests.auth.HTTPBasicAuth(
            username=__client_id, password=__client_secret
        ),
        json=data,
    )
    if response.status_code == 202:
        logging.warning("NotificationAPI request ignored. params: %s", data)
    if response.status_code == 500:
        logging.error(
            "NotificationAPI request failed. Response: %s. params: %s",
            response.text,
            data,
        )


def send(params):
    request("POST", "sender", params)


def retract(params):
    request("POST", "sender/retract", params)
