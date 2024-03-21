# obex-capabilities

obex-capabilities is a simple script to generate OBEX capabilities XML files at 
runtime for Bluetooth OBEX support.

Interacts with oFono or ModemManager to retrieve the current network name,
IMEI, Mobile Country Code (MCC) and mobile Network Code (MNC).
This information is advertised to BlueZ's `obexd`.
If no modem is available, IMEI is replaced by `machine-id` and the network 
information is not advertised to `obexd`.

## OBEX Capability specification

https://www.irda.org/standards/pubs/OBEX13.pdf

## License

[GPL-3.0-or-later](LICENSE)
