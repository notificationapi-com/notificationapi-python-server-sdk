#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

from notificationapi_python_server_sdk import notificationapi


def test_init():
    assert notificationapi.init() == "Initialized"
