# SPDX-FileCopyrightText: 2021 Dylan Van Assche <me@dylanvanassche.be>
# Copyright (C) 2024 Bardia Moshiri <fakeshell@bardia.tech>
# SPDX-License-Identifier: GPL-3.0-or-later

from os.path import exists
from os import environ, path
from abc import ABC, abstractmethod
from logging import debug, critical
from typing import cast
from .modem import Modem

OS_RELEASE_PATH = '/etc/os-release'
MACHINE_ID_PATH = '/etc/machine-id'
DEVICE_TREE_COMPATIBLE = '/proc/device-tree/compatible'
DEVICE_TREE_MODEL = '/proc/device-tree/model'

class Device(ABC):
    """
    Represent the information about a device.
    """

    def __init__(self, modem=None):
        self._os_release: str = None
        self._unique_id: str = None
        self._modem: Modem = modem
        self._os_release_path = environ.get('OS_RELEASE_PATH', OS_RELEASE_PATH)
        self._machine_id_path = environ.get('MACHINE_ID_PATH', MACHINE_ID_PATH)

    def __repr__(self):
        return 'DEVICE' \
            f'\n  Manufacturer: {self.manufacturer}' \
            f'\n  Model: {self.model}' \
            f'\n  Codename: {self.codename}' \
            f'\n  Unique ID: {self.unique_id}' \
            f'\n  Software version: {self.software_version}' \
            f'\n  OS version: {self.os_version}'

    def __str__(self):
        return self.__repr__()

    def _read_os_release(self) -> str:
        """
        Read /etc/os-release to determine OS version
        """
        # Determine OS release only once
        if self._os_release is not None:
            return self._os_release

        with open(self._os_release_path) as f:
            for line in filter(lambda line: '=' in line, f.readlines()):
                key, value = line.split('=')
                if key.lower() == 'version_id':
                    self._os_release = value.strip().replace('"', '')
                    break

        return self._os_release

    @property
    @abstractmethod
    def manufacturer(self) -> str:
        """
        Pretty name of the manufacturer.
        """

    @property
    @abstractmethod
    def model(self) -> str:
        """
        Pretty name of the device model.
        """

    @property
    @abstractmethod
    def codename(self) -> str:
        """
        Code name of the device.
        """

    @property
    def unique_id(self) -> str:
        """
        Unique identifier such as IMEI or MAC address.
        """
        # Determine unique ID only once
        if self._unique_id is not None:
            return self._unique_id

        if self._modem is not None:
            debug('Found modem, using IMEI')
            self._unique_id = cast(str, self._modem.imei)
        else:
            debug('No modem available, using machine-id')
            with open(self._machine_id_path) as f:
                self._unique_id = f.read().strip()

        return self._unique_id

    @property
    def software_version(self) -> str:
        """
        Software version release number.
        """
        return self._read_os_release()

    @property
    def os_version(self) -> str:
        """
        OS version release number.
        """
        return self._read_os_release()

class ARMDevice(Device):
    def __init__(self, modem=None):
        super().__init__(modem)

    @property
    def manufacturer(self) -> str:
        if path.exists("/usr/lib/droidian/device/obex-manufacturer"):
            with open("/usr/lib/droidian/device/obex-manufacturer", "r") as manufacturer_file:
                return manufacturer_file.read().strip()

        try:
            manufacturer = extract_prop('ro.product.vendor.manufacturer')
            return manufacturer
        except Exception:
            pass

        with open(DEVICE_TREE_COMPATIBLE) as f:
            compatible = f.read().split('\x00')
            manufacturer, _ = compatible[0].split(',')
            return manufacturer

    @property
    def model(self) -> str:
        if path.exists("/usr/lib/droidian/device/obex-model"):
            with open("/usr/lib/droidian/device/obex-model", "r") as model_file:
                return model_file.read().strip()

        try:
            model = extract_prop('ro.product.vendor.model')
            return model
        except Exception:
            pass

        with open(DEVICE_TREE_MODEL) as f:
            model = f.read().split('\x00')[0]
            return model

    @property
    def codename(self) -> str:
        if path.exists("/usr/lib/droidian/device/obex-codename"):
            with open("/usr/lib/droidian/device/obex-codename", "r") as codename_file:
                return codename_file.read().strip()

        try:
            codename = extract_prop('ro.product.board')
            if codename is not None:
                return codename

            codename = extract_prop('ro.product.vendor.device')
            if codename is not None:
                return codename
        except Exception:
            pass

        with open(DEVICE_TREE_COMPATIBLE) as f:
            compatible = f.read().split('\x00')
            _, codename = compatible[0].split(',')
            return codename

def extract_prop(prop):
    prop_files = [
        '/var/lib/lxc/android/rootfs/vendor/build.prop',
        '/android/vendor/build.prop',
        '/vendor/build.prop'
    ]

    prop_file = None
    for file in prop_files:
        if exists(file):
            prop_file = file
            break

    if prop_file is None:
        return None

    with open(prop_file, 'r') as f:
        for line in f:
            if line.startswith(prop):
                return line.split('=')[1].strip()
    return None

def guess_device(modem=None):
    if exists(DEVICE_TREE_COMPATIBLE):
        debug("Device is ARM")
        return ARMDevice(modem)
    else:
        critical("Device not implemented!")
        return
