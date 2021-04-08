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
notification_id = "notification_id"
send_api_path = f"https://api.notificationapi.com/{client_id}/sender"


def test_init_raises_given_empty_client_id():
    with pytest.raises(Exception, match="Bad client_id"):
        notificationapi.init("", "client_secret")


def test_init_raises_given_empty_client_secret():
    with pytest.raises(Exception, match="Bad client_secret"):
        notificationapi.init("client_id", "")


def test_init_passes_given_id_and_secret():
    notificationapi.init(client_id, client_secret)


def test_send_makes_one_post_api_call(requests_mock):
    requests_mock.post(send_api_path)
    notificationapi.init(client_id, client_secret)
    notificationapi.send({"user": user, "notificationId": notification_id})
    assert requests_mock.call_count == 1


def test_send_uses_basic_authorization(requests_mock):
    requests_mock.post(send_api_path)
    notificationapi.init(client_id, client_secret)
    notificationapi.send({"user": user, "notificationId": notification_id})
    assert (
        requests_mock.last_request.headers["Authorization"]
        == "Basic Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
    )


def test_send_includes_notification_id_and_user_in_request_body(
    requests_mock,
):
    requests_mock.post(send_api_path)
    notificationapi.init(client_id, client_secret)
    notificationapi.send({"user": user, "notificationId": notification_id})
    assert requests_mock.last_request.json() == {
        "notificationId": notification_id,
        "user": user,
    }


def test_send_includes_merge_tags_in_request_body(
    requests_mock,
):
    requests_mock.post(send_api_path)
    notificationapi.init(client_id, client_secret)
    notificationapi.send(
        {
            "user": user,
            "notificationId": notification_id,
            "mergeTags": {"x": "y"},
        }
    )
    assert requests_mock.last_request.json() == {
        "notificationId": notification_id,
        "user": user,
        "mergeTags": {"x": "y"},
    }


def test_send_includes_email_options_in_request_body(
    requests_mock,
):
    requests_mock.post(send_api_path)
    notificationapi.init(client_id, client_secret)
    email_options = {
        "email": {
            "bccAddresses": ["test@test.com"],
            "ccAddresses": ["test@test.com"],
            "replyToAddresses": ["test@test.com"],
        }
    }
    notificationapi.send(
        {
            "user": user,
            "notificationId": notification_id,
            "emailOptions": email_options,
        }
    )
    assert requests_mock.last_request.json() == {
        "notificationId": notification_id,
        "user": user,
        "emailOptions": email_options,
    }


def test_send_logs_if_it_gets_202(requests_mock, caplog):
    requests_mock.post(send_api_path, status_code=202)
    notificationapi.init(client_id, client_secret)
    notificationapi.send({"user": user, "notificationId": notification_id})
    assert "NotificationAPI request ignored." in caplog.text


def test_send_logs_on_202(requests_mock, caplog):
    requests_mock.post(send_api_path, status_code=202)
    notificationapi.init(client_id, client_secret)
    notificationapi.send({"user": user, "notificationId": notification_id})
    assert "NotificationAPI request ignored." in caplog.text


def test_send_logs_and_throws_on_500(requests_mock, caplog):
    requests_mock.post(send_api_path, status_code=500, text="big oof 500")
    notificationapi.init(client_id, client_secret)
    notificationapi.send({"user": user, "notificationId": notification_id})
    assert (
        "NotificationAPI request failed. Response: big oof 500" in caplog.text
    )
