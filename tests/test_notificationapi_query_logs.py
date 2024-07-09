#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
import json
from httpx import Response
from notificationapi_python_server_sdk import notificationapi

client_id = "client_id"
client_secret = "client_secret"
api_paths = {
    "query_logs": f"https://api.notificationapi.com/{client_id}/logs/query",
}

query_logs_params = {
    "dateRangeFilter": {
        "startTime": 1719600830559,
        "endTime": 1719600840559
    },
    "notificationFilter": ["order_tracking"],
    "channelFilter": ["EMAIL"],
    "userFilter": ["abcd-1234"],
    "statusFilter": ["SUCCESS"],
    "trackingIds": ["172cf2f4-18cd-4f1f-b2ac-e50c7d71891c"],
    "requestFilter": ['request.mergeTags.item="Krabby Patty Burger"'],
    "envIdFilter": ["6ok6imq9unr2budgiebjdaa6oi"]
}

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        ("query_logs", query_logs_params),
    ],
)
async def test_makes_one_post_api_call(respx_mock, func, params):
    route = respx_mock.post(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert route.called

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        ("query_logs", query_logs_params),
    ],
)
async def test_passes_params_as_json_body(respx_mock, func, params):
    route = respx_mock.post(api_paths[func]).mock(return_value=Response(200))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert json.loads(route.calls.last.request.content) == params

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        ("query_logs", query_logs_params),
    ],
)
async def test_logs_on_202(respx_mock, caplog, func, params):
    respx_mock.post(api_paths[func]).mock(return_value=Response(202))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert "NotificationAPI request ignored." in caplog.text

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func,params",
    [
        ("query_logs", query_logs_params),
    ],
)
async def test_logs_and_throws_on_500(respx_mock, caplog, func, params):
    respx_mock.post(api_paths[func]).mock(return_value=Response(500, text="big oof 500"))
    notificationapi.init(client_id, client_secret)
    await getattr(notificationapi, func)(params)
    assert "NotificationAPI request failed. Response: big oof 500" in caplog.text
