#!/usr/bin/python3

import requests

"""
requires pytest python package to be installed
run "python3 -m pytest ./test_payloads.py" in cli while server is running
"""

URL = "http://localhost:8080/radios/{}"
URL_LOC = "http://localhost:8080/radios/{}/location"


def test_scenario_1_1():
    resp = requests.post(URL.format(100), json={"alias": "Radio100",
                                                "allowed_locations": ["CPH-1", "CPH-2"]})
    assert resp.status_code == 201 or resp.status_code == 200


def test_scenario_1_2():
    resp = requests.post(URL.format(101), json={"alias": "Radio101",
                                                "allowed_locations": ["CPH-1", "CPH-2", "CPH-3"]})
    assert resp.status_code == 201 or resp.status_code == 200


def test_scenario_1_3():
    resp = requests.post(URL_LOC.format(100), json={"location": "CPH-1"})
    assert resp.status_code == 200


def test_scenario_1_4():
    resp = requests.post(URL_LOC.format(101), json={"location": "CPH-3"})
    assert resp.status_code == 200


def test_scenario_1_5():
    resp = requests.post(URL_LOC.format(100), json={"location": "CPH-3"})
    assert resp.status_code == 403


def test_scenario_1_6():
    resp = requests.get(URL_LOC.format(101))
    assert resp.status_code == 200 and resp.json() == {"location": "CPH-3"}


def test_scenario_1_7():
    resp = requests.get(URL_LOC.format(100))
    print(resp.json())
    assert resp.status_code == 200 and resp.json() == {"location": "CPH-1"}


def test_scenario_2_1():
    resp = requests.post(URL.format(102), json={"alias": "Radio102",
                                                "allowed_locations": ["CPH-1", "CPH-3"]})
    assert resp.status_code == 201 or resp.status_code == 200


def test_scenario_2_2():
    resp = requests.get(URL_LOC.format(102))
    assert resp.status_code == 404
