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


def request(method, uri, data=None):
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


def create_sub_notification(params):
    request(
        "PUT",
        "notifications/%s/subNotifications/%s"
        % (params["notification_id"], params["sub_notification_id"]),
        {"title": params["title"]},
    )


def delete_sub_notification(params):
    request(
        "DELETE",
        "notifications/%s/subNotifications/%s"
        % (params["notification_id"], params["sub_notification_id"]),
    )


def set_user_preferences(params):
    request(
        "POST",
        "user_preferences/%s" % (params["userId"]),
        params["userPreferences"],
    )
