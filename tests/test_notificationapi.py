#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
from notificationapi_python_server_sdk import (
    notificationapi,
)

client_id = "client_id"
client_secret = "client_secret"
user = {
    "id": "userId",
    "email": "test+python_server_sdk@notificationapi.com",
}
userId = "userId"
notification_id = "notification_id"
api_paths = {
    "send": f"https://api.notificationapi.com/{client_id}/sender",
    "retract": f"https://api.notificationapi.com/{client_id}/sender/retract",
}

send_api_path = f"https://api.notificationapi.com/{client_id}/sender"


def test_init_raises_given_empty_client_id():
    with pytest.raises(Exception, match="Bad client_id"):
        notificationapi.init("", "client_secret")


def test_init_raises_given_empty_client_secret():
    with pytest.raises(Exception, match="Bad client_secret"):
        notificationapi.init("client_id", "")


def test_init_passes_given_id_and_secret():
    notificationapi.init(client_id, client_secret)


@pytest.mark.parametrize(
    "func,params",
    [
        ("send", {"user": user, "notificationId": notification_id}),
        ("retract", {"userId": userId, "notificationId": notification_id}),
    ],
)
def test_makes_one_post_api_call(requests_mock, func, params):
    requests_mock.post(api_paths[func])
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert requests_mock.call_count == 1


@pytest.mark.parametrize(
    "func,params",
    [
        ("send", {"user": user, "notificationId": notification_id}),
        ("retract", {"userId": userId, "notificationId": notification_id}),
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
        ("send", {"user": user, "notificationId": notification_id}),
        ("retract", {"userId": userId, "notificationId": notification_id}),
    ],
)
def test_passes_params_as_json_body(requests_mock, func, params):
    requests_mock.post(api_paths[func])
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert requests_mock.last_request.json() == params


@pytest.mark.parametrize(
    "func,params",
    [
        ("send", {"user": user, "notificationId": notification_id}),
        ("retract", {"userId": userId, "notificationId": notification_id}),
    ],
)
def test_logs_on_202(requests_mock, caplog, func, params):
    requests_mock.post(api_paths[func], status_code=202)
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert "NotificationAPI request ignored." in caplog.text


@pytest.mark.parametrize(
    "func,params",
    [
        ("send", {"user": user, "notificationId": notification_id}),
        ("retract", {"userId": userId, "notificationId": notification_id}),
    ],
)
def test_logs_and_throws_on_500(requests_mock, caplog, func, params):
    requests_mock.post(api_paths[func], status_code=500, text="big oof 500")
    notificationapi.init(client_id, client_secret)
    getattr(notificationapi, func)(params)
    assert (
        "NotificationAPI request failed. Response: big oof 500" in caplog.text
    )
