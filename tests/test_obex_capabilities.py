# SPDX-FileCopyrightText: 2021 Dylan Van Assche <me@dylanvanassche.be>
# SPDX-License-Identifier: GPL-3.0-or-later
import subprocess

from obex_capabilities.device import Device, MockedDevice
from obex_capabilities.modem import Modem, MockedModem


def test_device():
    d: Device = MockedDevice()
    assert d.manufacturer == 'Manufacturer'
    assert d.model == 'Phone'
    assert d.codename == 'my-awesome-codename'
    assert d.unique_id == '123456789012345'
    assert d.software_version == '1.0.0'
    assert d.os_version == '2.0.0'

def test_modem():
    m: Modem = MockedModem()
    assert m.network == 'NetworkName'
    assert m.mcc == '123'
    assert m.mnc == '42'
    assert m.imei == '123456789012345'

def test_obex_capabilities():
    expected_xml = ''
    with open('./tests/data/mocked.xml') as f:
        expected_xml = f.read()

    env = { 'OS_RELEASE_PATH': './tests/data/os-release',
            'MACHINE_ID_PATH': './tests/data/machine-id',
            'MOCK_MODEM': '1',
            'MOCK_DEVICE': '1' }
    xml = subprocess.check_output('./obex_capabilities/__init__.py',
                                  env=env).decode()
    assert xml == expected_xml

def test_obex_capabilities_no_modem():
    expected_xml = ''
    with open('./tests/data/mocked-no-modem.xml') as f:
        expected_xml = f.read()

    env = { 'OS_RELEASE_PATH': './tests/data/os-release',
            'MACHINE_ID_PATH': './tests/data/machine-id',
            'MOCK_DEVICE': '1' }
    xml = subprocess.check_output('./obex_capabilities/__init__.py',
                                  env=env).decode()
    assert xml == expected_xml
