#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
import json
from httpx import Response
from notificationapi_python_server_sdk import notificationapi

client_id = "client_id"
client_secret = "client_secret"
userPreferences = [
    {"notificationId": "notificationId", "channel": "EMAIL", "state": True}
]
userId = "userId"
api_paths = {
    "set_user_preferences": f"https://api.notificationapi.com/{client_id}/user_preferences/{userId}",
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
async def test_makes_one_POST_api_call(respx_mock, func, params):
    route = respx_mock.post(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.called


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
async def test_uses_basic_authorization(respx_mock, func, params):
    route = respx_mock.post(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.calls.last.request.headers["Authorization"] == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
async def test_passes_user_preferences_as_json_body(respx_mock, func, params):
    route = respx_mock.post(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert json.loads(route.calls.last.request.content) == params["userPreferences"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
async def test_logs_and_throws_on_500(respx_mock, caplog, func, params):
    respx_mock.post(api_paths[func]).mock(return_value=Response(500, text="big oof 500"))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert "NotificationAPI request failed. Response: big oof 500" in caplog.text
