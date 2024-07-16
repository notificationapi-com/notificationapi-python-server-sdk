#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
import urllib.parse
import hashlib
import base64
from httpx import Response
from notificationapi_python_server_sdk import notificationapi

client_id = "client_id"
client_secret = "client_secret"
user_id = "userId"
notification_id = "notification_id"

api_paths = {
    "delete_user_preferences":
        f"https://api.notificationapi.com/{client_id}/users/{urllib.parse.quote(user_id)}/preferences?notificationId={notification_id}",
}

delete_user_preferences_params = {
    "id": user_id,
    "notificationId": notification_id
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        ("delete_user_preferences", delete_user_preferences_params),
    ],
)
async def test_makes_one_delete_api_call(respx_mock, func, params):
    route = respx_mock.delete(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.called


delete_user_preferences_params = {
    "id": user_id,
    "notificationId": notification_id
}
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        ("delete_user_preferences", delete_user_preferences_params),
    ],
)
async def test_uses_custom_authorization(respx_mock, func, params):
    route = respx_mock.delete(api_paths[func]).mock(return_value=Response(200))
    hashed_user_id = hashlib.sha256((client_secret + user_id).encode()).digest()
    hashed_user_id_base64 = base64.b64encode(hashed_user_id).decode()

    # Create custom authorization header
    custom_auth = 'Basic ' + base64.b64encode(f'{client_id}:{user_id}:{hashed_user_id_base64}'.encode()).decode()
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert "Authorization" in route.calls.last.request.headers
    assert route.calls.last.request.headers["Authorization"] == custom_auth


delete_user_preferences_params = {
    "id": user_id,
    "notificationId": notification_id
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        ("delete_user_preferences", delete_user_preferences_params),
    ],
)
async def test_logs_and_throws_on_500(respx_mock, caplog, func, params):
    respx_mock.delete(api_paths[func]).mock(return_value=Response(500, text="big oof 500"))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert "NotificationAPI request failed. Response: big oof 500" in caplog.text
