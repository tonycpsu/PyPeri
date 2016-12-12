#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyperi
----------------------------------

Tests for `pyperi` module.
"""

import httpretty
import pytest  # noqa

from pyperi.pyperi import PyPeri
from pprint import pprint


@httpretty.activate
def test_request_api():
    mock_url = (
        'https://api.periscope.tv/api/v2/testEndpoint?'
        'test_param=something&test_param2=else'
    )
    mock_body = '{"test":"ok"}'
    httpretty.register_uri(httpretty.GET, mock_url, mock_body)
    pp = PyPeri()
    result = pp.request_api(
        'testEndpoint', test_param='something', test_param2='else'
    )
    assert result == {'test': 'ok'}


def test_create_api_request_url():
    pp = PyPeri()
    url = pp.create_api_request_url(
        'testEndpoint', test_param='something', test_param2='else'
    )
    assert url == (
        'https://api.periscope.tv/api/v2/testEndpoint?'
        'test_param=something&test_param2=else'
    )

    url_no_params = pp.create_api_request_url('testEndpoint')
    assert url_no_params == 'https://api.periscope.tv/api/v2/testEndpoint?'


@httpretty.activate
def test_get_broadcast_info():
    broadcast_id = '1zqKVWybqeDGB'
    mock_url = (
        'https://api.periscope.tv/api/v2/accessVideoPublic?'
        'broadcast_id={broadcast_id}'
    ).format(broadcast_id=broadcast_id)
    mock_body_file = open('tests/responses/accessVideoPublic.txt', 'r')
    mock_body = mock_body_file.read()
    httpretty.register_uri(httpretty.GET, mock_url, mock_body)

    pp = PyPeri()
    result = pp.get_broadcast_info('1zqKVWybqeDGB')
    assert result['id'] == broadcast_id
    assert result['user_id'] == '376827'
    assert result['username'] == 'george_clinton'
