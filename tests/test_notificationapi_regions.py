#!/usr/bin/env python

"""Tests for region support in `notificationapi_python_server_sdk` package."""

import pytest
import httpx
from notificationapi_python_server_sdk import notificationapi, US_REGION, EU_REGION, CA_REGION

client_id = "client_id"
client_secret = "client_secret"


def test_init_with_default_region():
    notificationapi.init(client_id, client_secret)
    # Access the private variable directly - it's defined at module level
    assert notificationapi.__base_url == US_REGION


def test_init_with_eu_region():
    notificationapi.init(client_id, client_secret, EU_REGION)
    assert notificationapi.__base_url == EU_REGION


def test_init_with_ca_region():
    notificationapi.init(client_id, client_secret, CA_REGION)
    assert notificationapi.__base_url == CA_REGION


@pytest.mark.asyncio
async def test_request_uses_correct_region_url(respx_mock):
    # Test with EU region
    eu_api_url = f"{EU_REGION}/{client_id}/sender"
    route = respx_mock.post(eu_api_url).mock(return_value=httpx.Response(200))

    notificationapi.init(client_id, client_secret, EU_REGION)
    await notificationapi.send({"notificationId": "test", "user": {"id": "user1"}})

    assert route.called
    assert route.calls.last.request.url == eu_api_url
