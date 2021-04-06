#!/usr/bin/env python

"""Tests for `notificationapi_python_server_sdk` package."""

import pytest
import notificationapi_python_server_sdk


def test_hello():
    assert notificationapi_python_server_sdk.hello() == "Hello World"
