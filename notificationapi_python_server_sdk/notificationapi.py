import httpx
import logging
import hashlib
import base64
import urllib.parse
from . import US_REGION

__client_id = ""
__client_secret = ""
__base_url = US_REGION


def init(client_id, client_secret, base_url=None):
    if not client_id:
        raise Exception("Bad client_id")

    if not client_secret:
        raise Exception("Bad client_secret")

    global __client_id
    __client_id = client_id
    global __client_secret
    __client_secret = client_secret
    global __base_url
    if base_url:
        __base_url = base_url
    else:
        __base_url = US_REGION


async def request(method, uri, data=None, custom_auth=None, queryStrings=None):
    api_url = f"{__base_url}/{__client_id}/{uri}"

    headers = {}
    if custom_auth:
        headers['Authorization'] = custom_auth
    else:
        headers['Authorization'] = 'Basic ' + base64.b64encode(f'{__client_id}:{__client_secret}'.encode()).decode()

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            api_url,
            params=queryStrings,
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
    return response


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


async def update_schedule(params):
    await request(
        "PATCH",
        "schedule/%s"
        % (params["tracking_id"]),
        params["send_request"],
    )


async def delete_schedule(params):
    await request(
        "DELETE",
        "schedule/%s"
        % (params["tracking_id"]),
    )


async def set_user_preferences(params):
    await request(
        "POST",
        "user_preferences/%s" % (params["userId"]),
        params["userPreferences"],
    )


async def delete_user_preferences(params):
    user_id = params.pop('id')

    hashed_user_id = hashlib.sha256((__client_secret + user_id).encode()).digest()
    hashed_user_id_base64 = base64.b64encode(hashed_user_id).decode()

    custom_auth = 'Basic ' + base64.b64encode(f'{__client_id}:{user_id}:{hashed_user_id_base64}'.encode()).decode()

    await request('DELETE', f'users/{user_id}/preferences', None, custom_auth, params)


async def identify_user(params):
    user_id = params.pop('id')

    hashed_user_id = hashlib.sha256((__client_secret + user_id).encode()).digest()
    hashed_user_id_base64 = base64.b64encode(hashed_user_id).decode()

    custom_auth = 'Basic ' + base64.b64encode(f'{__client_id}:{user_id}:{hashed_user_id_base64}'.encode()).decode()

    await request('POST', f'users/{urllib.parse.quote(user_id)}', params, custom_auth)


async def query_logs(params):
    response = await request("POST", "logs/query", params)
    return response


async def update_in_app_notification(user_id, params):
    hashed_user_id = hashlib.sha256((__client_secret + user_id).encode()).digest()
    hashed_user_id_base64 = base64.b64encode(hashed_user_id).decode()
    custom_auth = 'Basic ' + base64.b64encode(f'{__client_id}:{user_id}:{hashed_user_id_base64}'.encode()).decode()

    return await request('PATCH', f'users/{user_id}/notifications/INAPP_WEB', params, custom_auth)
