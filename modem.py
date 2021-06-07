from abc import ABC, abstractmethod

from dbus import SystemBus, Interface

FREEDESKTOP_INTERFACE_PROPERTIES = 'org.freedesktop.DBus.Properties'
FREEDESKTOP_INTERFACE_OBJECT_MANAGER = 'org.freedesktop.DBus.ObjectManager'
FREEDESKTOP_METHOD_GET_MANAGED_OBJECTS = 'GetManagedObjects'
MM_NAME = 'org.freedesktop.ModemManager1'
MM_OBJECT_PATH = '/org/freedesktop/ModemManager1'
MM_INTERFACE_LOCATION = 'org.freedesktop.ModemManager1.Modem.Location'
MM_METHOD_GET_LOCATION = 'GetLocation'
MM_INTERFACE_MODEM_3GPP = 'org.freedesktop.ModemManager1.Modem.Modem3gpp'
MM_METHOD_GET = 'Get'
MM_LOCATION_3GPP = 1

class Modem(ABC):
    def __repr__(self):
        return f'NETWORK ({self.__class__.__name__})' \
            f'\n  Modem: {self.network}' \
            f'\n  IMEI: {self.imei}' \
            f'\n  MCC: {self.mcc}' \
            f'\n  MNC: {self.mnc}' \

    def __str__(self):
        return self.__repr__()

    @abstractmethod
    def imei(self) -> str:
        """
        Get the IMEI number of the phone.
        """
        raise NotImplementedError("Modem IMEI getter not implemented")

    @abstractmethod
    def network(self) -> str:
        """
        Get the network name on which the phone is registered on.
        """
        raise NotImplementedError("Modem name getter not implemented")

    @abstractmethod
    def mcc(self) -> str:
        """
        Get the country code (MCC) of the network on which the phone is
        registered on.
        """
        raise NotImplementedError("Country code MCC getter not implemented")

    @abstractmethod
    def mnc(self) -> str:
        """
        Get the network ID (MNC) of the network on which the phone is
        registered on.
        """
        raise NotImplementedError("Modem ID MNC getter not implemented")


class Ofono(Modem):
    """
    Ofono backend to retrieve network information.
    """
    def __init__(self):
        super().__init__()

    @property
    def imei(self) -> str:
        return '123456789012345'

    @property
    def network(self) -> str:
        return 'NetworkName'

    @property
    def mcc(self) -> str:
        return '123'

    @property
    def mnc(self) -> str:
        return '42'


class ModemManager(Modem):
    """
    ModemManager backend to retrieve network information.
    """
    def __init__(self):
        super().__init__()
        self._dbus: SystemBus = SystemBus()

        # Get exposed Modem objects
        o = self._dbus.get_object(MM_NAME, MM_OBJECT_PATH)
        self._object_manager_interface: Interface = Interface(o, FREEDESKTOP_INTERFACE_OBJECT_MANAGER)
        modems = self._object_manager_interface.get_dbus_method(FREEDESKTOP_METHOD_GET_MANAGED_OBJECTS)

        if modems:
            # Execute DBus method to get modems and use the first one
            object_path : str = list(modems().keys())[0]
            o = self._dbus.get_object(MM_NAME, object_path)

            # Init DBus MM 3GPP and Location interfaces
            self._location_interface: Interface = Interface(o, MM_INTERFACE_LOCATION)
            self._3gpp_interface: Interface = Interface(o, MM_INTERFACE_MODEM_3GPP)

            # Get IMEI, network and location information
            self._imei: str = self._3gpp_interface.Get(MM_INTERFACE_MODEM_3GPP,
                                                       'Imei',
                                                       dbus_interface=FREEDESKTOP_INTERFACE_PROPERTIES)
            self._network: str = self._3gpp_interface.Get(MM_INTERFACE_MODEM_3GPP,
                                                          'OperatorName',
                                                          dbus_interface=FREEDESKTOP_INTERFACE_PROPERTIES)
            location: dict = self._location_interface.get_dbus_method(MM_METHOD_GET_LOCATION)
            self._mcc, self._mnc, _, _, _ = location()[MM_LOCATION_3GPP].split(',')
        else:
            raise RuntimeError('Unable to find ModemManager modem')

    @property
    def imei(self) -> str:
        return self._imei

    @property
    def network(self) -> str:
        return self._network

    @property
    def mcc(self) -> str:
        return self._mcc

    @property
    def mnc(self) -> str:
        return self._mnc


class MockedModem(Modem):
    """
    Mocked modem backend to retrieve network information for tests.
    """
    def __init__(self):
        super().__init__()

    @property
    def network(self) -> str:
        return 'NetworkName'

    @property
    def mcc(self) -> str:
        return '123'

    @property
    def mnc(self) -> str:
        return '42'
