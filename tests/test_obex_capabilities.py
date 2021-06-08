# SPDX-FileCopyrightText: 2021 Dylan Van Assche <me@dylanvanassche.be>
# SPDX-License-Identifier: GPL-3.0-or-later
import subprocess

from obex_capabilities.device import Device
from obex_capabilities.modem import MockedModem

def test_device():
    d = Device('Manufacturer', 'Phone', 'my-awesome-codename',
               '123456789012345', '1.0.0', '2.0.0')
    assert d.manufacturer == 'Manufacturer'
    assert d.model == 'Phone'
    assert d.codename == 'my-awesome-codename'
    assert d.unique_id == '123456789012345'
    assert d.software_version == '1.0.0'
    assert d.os_version == '2.0.0'

def test_modem():
    m = MockedModem()
    assert m.network == 'NetworkName'
    assert m.mcc == '123'
    assert m.mnc == '42'
    assert m.imei == '123456789012345'

def test_obex_capabilities():
    expected_xml = ''
    with open('./tests/data/mocked.xml') as f:
        expected_xml = f.read()

    env = { 'DEVICEINFO_PATH': './tests/data/deviceinfo',
            'OS_RELEASE_PATH': './tests/data/os-release',
            'MACHINE_ID_PATH': './tests/data/machine-id',
            'MOCK_MODEM': '1' }
    xml = subprocess.check_output('./obex_capabilities/__init__.py',
                                  env=env).decode()
    print(xml)
    print('-'*50)
    print(expected_xml)
    assert xml == expected_xml

def test_obex_capabilities_no_modem():
    expected_xml = ''
    with open('./tests/data/mocked-no-modem.xml') as f:
        expected_xml = f.read()

    env = { 'DEVICEINFO_PATH': './tests/data/deviceinfo',
            'OS_RELEASE_PATH': './tests/data/os-release',
            'MACHINE_ID_PATH': './tests/data/machine-id' }
    xml = subprocess.check_output('./obex_capabilities/__init__.py',
                                  env=env).decode()
    assert xml == expected_xml
