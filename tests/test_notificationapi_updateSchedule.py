#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
import json
from httpx import Response
from notificationapi_python_server_sdk import notificationapi

client_id = "client_id"
client_secret = "client_secret"
tracking_id = "tracking_id"
send_request={
    'notificationId':'notification_id'
}
api_paths = {
    "update_schedule": f"https://api.notificationapi.com/{client_id}/schedule/{tracking_id}",
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_schedule",
            {
                "tracking_id": tracking_id,
                "send_request": send_request,
            },
        ),
    ],
)
async def test_makes_one_patch_api_call(respx_mock, func, params):
    route = respx_mock.patch(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.called


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_schedule",
            {
                "tracking_id": tracking_id,
                "send_request": send_request,
            },
        ),
    ],
)
async def test_uses_basic_authorization(respx_mock, func, params):
    route = respx_mock.patch(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.calls.last.request.headers["Authorization"] == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_schedule",
            {
                "tracking_id": tracking_id,
                "send_request": send_request,
            },
        ),
    ],
)
async def test_passes_send_request_as_json_body(respx_mock, func, params):
    route = respx_mock.patch(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert json.loads(route.calls.last.request.content) ==  params["send_request"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "update_schedule",
            {
                "tracking_id": tracking_id,
                "send_request": send_request,
            },
        ),
    ],
)
async def test_logs_and_throws_on_500(respx_mock, caplog, func, params):
    respx_mock.patch(api_paths[func]).mock(return_value=Response(500, text="big oof 500"))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert "NotificationAPI request failed. Response: big oof 500" in caplog.text
