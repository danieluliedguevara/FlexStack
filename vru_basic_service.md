# VRU Awareness Messages

Vulnerable Road User (VRU) Awareness Messages allow VRUs to share their presence to other road users through VAMs. VAMs have the same instantation format than other facility-layer messages like CAMs, DENMs, etc. 

__Required__ components are;
- [__LinkLayer__](link_layer.md)
- [__GeoNetworking Router__](geonetworking.md)
- [__BTP Router__](btp.md)
- [__Location Service__](location_service.md)
- [__Device Data Provider__](device-data-provider.md)
- [__VRU Awareness Service__](#vru-awareness-service)

__Optional__ (but recomended) components are;
- [__Local Dynamic_Map__](local-dynamic-map.md)

!!! Important
    [__Logging__](logging.md) is always an optional component. But it's highly recomended.

A quickstart is available [here](#quickstart), however keep reading if more detailed information about the component is needed.

---

## VRU Awareness Messages Overview

The VRU Awareness Message comes from the [ETSI TS 103 300-3 V2.1.1 (2020-11)]( https://www.etsi.org/deliver/etsi_ts/103300_103399/10330003/02.01.01_60/ts_10330003v020101p.pdf) standard. 

The VRU Awareness Message is composed of six subcomponents including;
- [VRU Basic Service Management](#vru-basic-service-management)
- [VRU Cluster Management](#vru-cluster-management)
- [VAM Reception Management](#vru-reception-management)
- [VAM Transmission Management](#vam-transmission-management)
- [VAM Encoding & Decoding](#vam-encoding-&-decoding)

---

### VRU Basic Service Management

The __VRU Basic Service Management__ is the main component for VAM messages. This component declares the neded subcomponents (i.e., VAM Coder, VAM Reception Management and VAM Transmission Mangement). 

The basic use is;

```py
from flexstack.facilities.vru_awareness_service.vru_awareness_service import VRUAwarenessService

vru_awareness_service = VRUAwarenessService(btp_router=btp_router,
                                            device_data_provider=device_data_provider)
```
Here the [__BTP Router__](btp-router.md) as well as the [__Device_Data_Provider__](device-data-provider.md) are needed.

### VRU Cluster Management

The __VRU Cluster Management__ is the component in charge of providing the clustering intelligence. VRUs many times are clustered together (e.g., cyclists in a peloton, pedestrians in a busy street) meaning that providing a unique message for all of them can decrease the amount of messages sent whilst still mantaining VRU __awareness__ levels intact.

This component is however __currently not implemented__.

### VAM Reception Management

The __VAM Reception Management__ component is in charge of recieving all the VAM messages from the BTP component. The __VAM Reception Management__ componet doesn't have to be explicitly declared. It's already declared with the code provided in the __VRU Basic Service Management__ [example](#vru-basic-service-management).

### VAM Transmission Management

The __VAM Transmission Management__ component is in charge of transmitting all the VAM messages from the application layer to the BTP component. The declaration of the __VAM Transmission Management__ can be done by adding a single line to the __VRU Basic Service Management__ [example](#vru-basic-service-management);

```py
from flexstack.facilities.vru_awareness_service.vru_awareness_service import VRUAwarenessService

vru_awareness_service = VRUAwarenessService(btp_router=btp_router,
                                            device_data_provider=device_data_provider)

location_service.add_callback(vru_awareness_service.vam_transmission_management.location_service_callback)
```

A [__location service__](location-service.md) will be needed to transmit VAM messages. This location service will call the __VAM Transmission Management__ every time a new location is obtained. The __VAM Transmission Management__ can also trigger the transmission of VAM messages if one of the following occurs;
- The time elapsed since the last time the individual VAM was transmitted exceeds T_GenVamMax.
- The Euclidian absolute distance between the current estimated position of the reference point of the VRU and the estimated position of the reference point lastly included in an individual VAM exceeds a pre-defined threshold minReferencePointPositionChangeThreshold.
- The difference between the current estimated ground speed of the reference point of the VRU and the estimated absolute speed of the reference point of the VRU lastly included in an individual VAM exceeds a pre-defined threshold minGroundSpeedChangeThreshold.
- The difference between the orientation of the vector of the current estimated ground velocity of the reference point of the VRU and the estimated orientation of the vector of the ground velocity of the reference point of the VRU lastly included in an individual VAM exceeds a pre-defined threshold  minGroundVelocityOrientationChangeThreshold.
- ...

Please refer to for [ETSI TS 103 300-3 V2.1.1 (2020-11)]( https://www.etsi.org/deliver/etsi_ts/103300_103399/10330003/02.01.01_60/ts_10330003v020101p.pdf) for more information.

### VAM Encoding & Decoding
__VAM Encoding & Decoding__ uses the [__ASN1Tools Python Library__](https://asn1tools.readthedocs.io/en/latest/). It encodes and decodes based on the [__VAM ASN.1__](https://forge.etsi.org/rep/ITS/asn1/vam-ts103300_3/tree/v2.1.1/).

The coding and decoding is done automatically with the previously shown code.

---

## Quickstart

The VRU Awareness Message can be used in it's most simple flavour as follows;


```py
import logging
import logging.config

from flexstack.facilities.vru_awareness_service.vru_awareness_service import VRUAwarenessService
from flexstack.facilities.vru_awareness_service.vam_transmission_management import DeviceDataProvider
from flexstack.utils.static_location_service import ThreadStaticLocationService as LocationService

from flexstack.btp.router import Router as BTPRouter

from flexstack.geonet.router import Router
from flexstack.geonet.mib import MIB
from flexstack.geonet.gn_address import GNAddress, M, ST, MID

from flexstack.linklayer.raw_link_layer import RawLinkLayer


logging.basicConfig(level=logging.INFO)


# Geonet
mac_address = b"\x00\x00\x00\x00\x00\x00"
mib = MIB()
gn_addr = GNAddress()
gn_addr.set_m(M.GN_MULTICAST)
gn_addr.set_st(ST.CYCLIST)
gn_addr.set_mid(MID(mac_address))
mib.itsGnLocalGnAddr = gn_addr
gn_router = Router(mib=mib, sign_service=None)

# Link-Layer
ll = RawLinkLayer(iface="eth0", mac_address=mac_address, 
                  receive_callback=gn_router.gn_data_indicate)
gn_router.link_layer = ll

# BTP
btp_router = BTPRouter(gn_router)
gn_router.register_indication_callback(btp_router.btp_data_indication)


# Facility - Location Service
location_service = LocationService()

location_service.add_callback(gn_router.refresh_ego_position_vector)

# Facility - Device Data Provider
device_data_provider = DeviceDataProvider()
device_data_provider.station_id = 1
device_data_provider.station_type = 2  # Cyclist

# Facility - VRU Awareness Service
vru_awareness_service = VRUAwarenessService(btp_router=btp_router,
                                            device_data_provider=device_data_provider)

location_service.add_callback(vru_awareness_service.vam_transmission_management.location_service_callback)

# Applications would be declared here


location_service.location_service_thread.join()

```
The only issue that can be encounter here is [__Networking Interface__](issues-networking-interface.md).

Logging has been included to provide a way of visualizing the sent messages. View [Logging] to get more detailed information on how to use it.

---

## Interfacing with the VRU Basic Service

Interaction between the application layer and the facility and below layers is done through the [__Local_Dynamic_Map__](local-dynamic-map.md).

---

You can explore the examples scripts avaialble, expand upon them or use them as a baseline to create your own. If you have any questions about the agents, feel free to post in the [forum](forum-url).





