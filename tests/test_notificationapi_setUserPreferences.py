#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
from notificationapi_python_server_sdk import (
    notificationapi,
)

client_id = "client_id"
client_secret = "client_secret"
userPreferences = [
    {"notificationId": "notificationId", "channel": "EMAIL", "state": True}
]
userId = "userId"
api_paths = {
    "set_user_preferences": f"https://api.notificationapi.com/{client_id}/user_preferences/{userId}",
}


@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
def test_makes_one_POST_api_call(requests_mock, func, params):
    requests_mock.post(api_paths[func])
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert requests_mock.call_count == 1


@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
def test_uses_basic_authorization(requests_mock, func, params):
    requests_mock.post(api_paths[func])
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert (
        requests_mock.last_request.headers["Authorization"]
        == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
    )


@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
def test_passes_title_as_json_body(requests_mock, func, params):
    requests_mock.post(api_paths[func])
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert requests_mock.last_request.json() == userPreferences


@pytest.mark.parametrize(
    "func,params",
    [
        (
            "set_user_preferences",
            {"userId": userId, "userPreferences": userPreferences},
        ),
    ],
)
def test_logs_and_throws_on_500(requests_mock, caplog, func, params):
    requests_mock.post(api_paths[func], status_code=500, text="big oof 500")
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert (
        "NotificationAPI request failed. Response: big oof 500" in caplog.text
    )
