class Device:
    """
    Represent the information about a device.
    """
    def __init__(self, manufacturer: str, model: str, codename: str,
                 unique_id: str, software_version: str, os_version: str):
        self._manufacturer: str = manufacturer
        self._model: str = model
        self._codename: str = codename
        self._unique_id: str = unique_id
        self._software_version: str = software_version
        self._os_version: str = os_version

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

    @property
    def manufacturer(self) -> str:
        """
        Pretty name of the manufacturer.
        """
        return self._manufacturer

    @property
    def model(self) -> str:
        """
        Pretty name of the device model.
        """
        return self._model

    @property
    def codename(self) -> str:
        """
        Code name of the device.
        """
        return self._codename

    @property
    def unique_id(self) -> str:
        """
        Unique identifier such as IMEI or MAC address.
        """
        return self._unique_id

    @property
    def software_version(self) -> str:
        """
        Software version release number.
        """
        return self._software_version

    @property
    def os_version(self) -> str:
        """
        OS version release number.
        """
        return self._os_version

