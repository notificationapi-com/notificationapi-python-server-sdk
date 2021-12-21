#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
from notificationapi_python_server_sdk import (
    notificationapi,
)

client_id = "client_id"
client_secret = "client_secret"


def test_init_raises_given_empty_client_id():
    with pytest.raises(Exception, match="Bad client_id"):
        notificationapi.init("", "client_secret")


def test_init_raises_given_empty_client_secret():
    with pytest.raises(Exception, match="Bad client_secret"):
        notificationapi.init("client_id", "")


def test_init_passes_given_id_and_secret():
    notificationapi.init(client_id, client_secret)
