import httpx
import logging
import hashlib
import base64
import urllib.parse

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


async def request(method, uri, data=None, custom_auth=None):
    api_url = "https://api.notificationapi.com/" + __client_id + "/" + uri

    headers = {}
    if custom_auth:
        headers['Authorization'] = custom_auth
    else:
        headers['Authorization'] = 'Basic ' + base64.b64encode(f'{__client_id}:{__client_secret}'.encode()).decode()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            api_url,
            headers=headers,
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


async def send(params):
    await request("POST", "sender", params)


async def retract(params):
    await request("POST", "sender/retract", params)


async def create_sub_notification(params):
    await request(
        "PUT",
        "notifications/%s/subNotifications/%s"
        % (params["notification_id"], params["sub_notification_id"]),
        {"title": params["title"]},
    )


async def delete_sub_notification(params):
    await request(
        "DELETE",
        "notifications/%s/subNotifications/%s"
        % (params["notification_id"], params["sub_notification_id"]),
    )


async def set_user_preferences(params):
    await request(
        "POST",
        "user_preferences/%s" % (params["userId"]),
        params["userPreferences"],
    )


async def identify_user(params):
    user_id = params.pop('id')

    hashed_user_id = hashlib.sha256((__client_secret + user_id).encode()).digest()
    hashed_user_id_base64 = base64.b64encode(hashed_user_id).decode()

    custom_auth = 'Basic ' + base64.b64encode(f'{__client_id}:{user_id}:{hashed_user_id_base64}'.encode()).decode()

    await request('POST', f'users/{urllib.parse.quote(user_id)}', params, custom_auth)
