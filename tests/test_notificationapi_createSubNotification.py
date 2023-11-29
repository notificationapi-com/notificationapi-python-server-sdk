#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
import json
from httpx import Response
from notificationapi_python_server_sdk import notificationapi

client_id = "client_id"
client_secret = "client_secret"
notification_id = "notification_id"
sub_notification_id = "sub_notification_id"
title = "title"
api_paths = {
    "create_sub_notification": f"https://api.notificationapi.com/{client_id}/notifications/{notification_id}/subNotifications/{sub_notification_id}",
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "create_sub_notification",
            {
                "notification_id": notification_id,
                "sub_notification_id": sub_notification_id,
                "title": title,
            },
        ),
    ],
)
async def test_makes_one_put_api_call(respx_mock, func, params):
    route = respx_mock.put(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.called


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "create_sub_notification",
            {
                "notification_id": notification_id,
                "sub_notification_id": sub_notification_id,
                "title": title,
            },
        ),
    ],
)
async def test_uses_basic_authorization(respx_mock, func, params):
    route = respx_mock.put(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.calls.last.request.headers["Authorization"] == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "create_sub_notification",
            {
                "notification_id": notification_id,
                "sub_notification_id": sub_notification_id,
                "title": title,
            },
        ),
    ],
)
async def test_passes_title_as_json_body(respx_mock, func, params):
    route = respx_mock.put(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert json.loads(route.calls.last.request.content) == {"title": params["title"]}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        (
            "create_sub_notification",
            {
                "notification_id": notification_id,
                "sub_notification_id": sub_notification_id,
                "title": title,
            },
        ),
    ],
)
async def test_logs_and_throws_on_500(respx_mock, caplog, func, params):
    respx_mock.put(api_paths[func]).mock(return_value=Response(500, text="big oof 500"))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert "NotificationAPI request failed. Response: big oof 500" in caplog.text
