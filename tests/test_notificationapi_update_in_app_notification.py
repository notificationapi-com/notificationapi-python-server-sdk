#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
import hashlib
import base64
import urllib.parse
import json
from httpx import Response
from notificationapi_python_server_sdk import notificationapi

client_id = "client_id"
client_secret = "client_secret"
user_id = "userId"

api_paths = {
    "update_in_app_notification": f"https://api.notificationapi.com/{client_id}/users/{urllib.parse.quote(user_id)}/notifications/INAPP_WEB",
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_in_app_notification",
            (
                user_id,
                {
                    "trackingIds": ["sampleTrackingId"],
                    "opened": "1970-01-01T00:00:00.000Z",
                    "clicked": "1970-01-01T00:00:00.000Z",
                    "archived": "1970-01-01T00:00:00.000Z",
                    "actioned1": "1970-01-01T00:00:00.000Z",
                    "actioned2": "1970-01-01T00:00:00.000Z",
                    "reply": {"date": "1970-01-01T00:00:00.000Z", "message": "nice!"}
                }
            ),
        ),
    ],
)
async def test_makes_one_patch_api_call(respx_mock, func, params):
    route = respx_mock.patch(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(*params)
    assert route.called


@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_in_app_notification",
            (
                user_id,
                {
                    "trackingIds": ["sampleTrackingId"],
                    "opened": "1970-01-01T00:00:00.000Z",
                    "clicked": "1970-01-01T00:00:00.000Z",
                    "archived": "1970-01-01T00:00:00.000Z",
                    "actioned1": "1970-01-01T00:00:00.000Z",
                    "actioned2": "1970-01-01T00:00:00.000Z",
                    "reply": {"date": "1970-01-01T00:00:00.000Z", "message": "nice!"}
                }
            ),
        ),
    ],
)
async def test_uses_custom_authorization(respx_mock, func, params):
    route = respx_mock.patch(api_paths[func]).mock(return_value=Response(200))
    hashed_user_id = hashlib.sha256((client_secret + user_id).encode()).digest()
    hashed_user_id_base64 = base64.b64encode(hashed_user_id).decode()

    # Create custom authorization header
    custom_auth = 'Basic ' + base64.b64encode(f'{client_id}:{user_id}:{hashed_user_id_base64}'.encode()).decode()
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(*params)
    assert "Authorization" in route.calls.last.request.headers
    assert route.calls.last.request.headers["Authorization"] == custom_auth


@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_in_app_notification",
            (
                user_id,
                {
                    "trackingIds": ["sampleTrackingId"],
                    "opened": "1970-01-01T00:00:00.000Z",
                    "clicked": "1970-01-01T00:00:00.000Z",
                    "archived": "1970-01-01T00:00:00.000Z",
                    "actioned1": "1970-01-01T00:00:00.000Z",
                    "actioned2": "1970-01-01T00:00:00.000Z",
                    "reply": {"date": "1970-01-01T00:00:00.000Z", "message": "nice!"}
                }
            ),
        ),
    ],
)
async def test_passes_data_as_json_body(respx_mock, func, params):
    route = respx_mock.patch(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(*params)
    sent_data = json.loads(route.calls.last.request.content)
    assert sent_data == {
        "trackingIds": ["sampleTrackingId"],
        "opened": "1970-01-01T00:00:00.000Z",
        "clicked": "1970-01-01T00:00:00.000Z",
        "archived": "1970-01-01T00:00:00.000Z",
        "actioned1": "1970-01-01T00:00:00.000Z",
        "actioned2": "1970-01-01T00:00:00.000Z",
        "reply": {"date": "1970-01-01T00:00:00.000Z", "message": "nice!"}
    }


@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_in_app_notification",
            (
                user_id,
                {
                    "trackingIds": ["sampleTrackingId"],
                    "opened": "1970-01-01T00:00:00.000Z",
                    "clicked": "1970-01-01T00:00:00.000Z",
                    "archived": "1970-01-01T00:00:00.000Z",
                    "actioned1": "1970-01-01T00:00:00.000Z",
                    "actioned2": "1970-01-01T00:00:00.000Z",
                    "reply": {"date": "1970-01-01T00:00:00.000Z", "message": "nice!"}
                }
            ),
        ),
    ],
)
async def test_logs_and_throws_on_500(respx_mock, caplog, func, params):
    respx_mock.patch(api_paths[func]).mock(return_value=Response(500, text="big oof 500"))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(*params)
    assert "NotificationAPI request failed. Response: big oof 500" in caplog.text
