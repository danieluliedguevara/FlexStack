# Local Dynamic Map

The Local Dynamic Map (LDM) is in charge of locally storing, managing, and sharing the messages received in a structured manner.

__Required__ component is:
- [__Location Service__](location_service.md)

!!! Important
    [__Logging__](logging.md) is always an optional component. However, it is highly recommended.

A quickstart is available [here](#quickstart), but keep reading if more detailed information about the component is needed.

---

## Local Dynamic Map Overview

The Local Dynamic Map follows the [ETSI EN 302 895 V1.1.1 (2014-09)](https://www.etsi.org/deliver/etsi_en/302800_302899/302895/01.01.01_60/en_302895v010101p.pdf) standard. Newer standards have been published, but no significant relevant changes have been introduced.

The Local Dynamic Map is composed of two subcomponents:
- [LDM Service](#ldm-service)
- [LDM Maintenance](#ldm-maintenance)

---

### Local Dynamic Map Service

The LDM is connected to authorized [__LDM Data Providers__](#ldm-data-providers) and [__LDM Data Consumers__](#ldm-data-consumers). [__LDM Data Providers__](#ldm-data-providers) supply information to the LDM, which then makes this data available to [__LDM Data Consumers__](#ldm-data-consumers). The LDM offers three different types of interfaces:
- A [__publish interface__](#ldm-publish-interface) for [__LDM Data Providers__](#ldm-data-providers). The providers publish information through [__LDM Data Objects__](#local-dynamic-map-ldm-data-object).
- A [__query interface__](#ldm-query-interface) for [__LDM Data Consumers__](#ldm-data-consumers). This query returns a list of [__LDM Data Objects__](#local-dynamic-map-ldm-data-object).
- A [__publish/subscribe interface__](#ldm-publish/subscribe-interface) for [__LDM Data Consumers__](#ldm-data-consumers). It also returns a list of [__LDM Data Objects__](#local-dynamic-map-ldm-data-object).

The LDM provides:
- Mechanisms for facilities to register and deregister as [__LDM Data Providers__](#ldm-data-providers).
- Mechanisms for applications to register and deregister as [__LDM Data Providers__](#ldm-data-providers) or [__LDM Data Consumers__](#ldm-data-consumers).
- Verification of the authorization of [__LDM Data Providers__](#ldm-data-providers) and [__LDM Data Consumers__](#ldm-data-consumers) before granting data access.

### Local Dynamic Map Maintenance

The LDM is responsible for maintaining all [__LDM Data Objects__](#local-dynamic-map-ldm-data-object) received from [__LDM Data Providers__](#ldm-data-providers) throughout their validity period and within the [__LDM Area of Maintenance__](#ldm-area-of-maintenance).

An [__LDM Data Object__](#local-dynamic-map-ldm-data-object) is considered valid for the duration of its specified time validity, starting from its assigned timestamp. Each LDM Data Provider defines the timestamp and time validity for the [__LDM Data Object__](#local-dynamic-map-ldm-data-object) it submits:

- The timestamp is set when adding or updating an [__LDM Data Object__](#local-dynamic-map-ldm-data-object).
- The default time validity for all [__LDM Data Objects__](#local-dynamic-map-ldm-data-object) is established during registration. This default validity is overridden by a specific time validity assigned when an [__LDM Data Object__](#local-dynamic-map-ldm-data-object) is added or updated.

Additionally, an [__LDM Data Object__](#local-dynamic-map-ldm-data-object) is considered valid if its location intersects with the [__LDM Area of Maintenance__](#ldm-area-of-maintenance). The [__LDM Data Provider__](#ldm-data-providers) specifies this location when adding or updating an [__LDM Data Object__](#local-dynamic-map-ldm-data-object). The [__LDM Area of Maintenance__](#ldm-area-of-maintenance) is a defined geographical region that may be dynamically adjusted based on the real-time location of the host ITS-S.

---

## LDM Declaration

### LDM Data Providers
LDM Data Providers are facilities or applications authorized to supply data to the LDM. They register with the LDM and submit [__LDM Data Objects__](#ldm-data-object) that contain timestamped and location-referenced information.

```py
ldm.ldm_if_ldm_3.register_data_provider(
    RegisterDataProviderReq(
        application_id=CAM,
        access_permissions=access_permissions,
        time_validity=TimeValidity(time_validity),
    )
)
```

Where;
```py
access_permission = [CAM]
time_validity = 5
```
Access permissions provide the LDM Data Provider access to provide specific type of data objects, in this case CAMs. The time validity provides the LDM the time for which the message must be stored. In this case 5 seconds.

### LDM Data Consumers
LDM Data Consumers are facilities or applications authorized to request and retrieve data from the LDM. Consumers interact with the LDM through query and publish/subscribe interfaces.

To register a data consumer the following lines of code must be used (example for application requiring VAM and CAM messages);

```py
register_data_consumer_reponse: RegisterDataConsumerResp = ldm.register_data_consumer(
            RegisterDataConsumerReq(
                application_id=MAPEM, # TODO: Allow application to sign up!!
                access_permisions=[VAM, CAM],
                area_of_interest=location,
            )
        )
if register_data_consumer_reponse.result == 2:
    raise Exception(f"Failed to register data consumer: {str(register_data_consumer_reponse)}")
```

Each LDM Data Consumer must also share the area of interest;

```py
reference_position = ReferencePosition(
    latitude=0,
    longitude=0,
    position_confidence_ellipse=PositionConfidenceEllipse(
        semi_major_confidence=0,
        semi_major_orientation=0,
        semi_minor_confidence=0,
    ),
    altitude=Altitude(altitude_value=0, altitude_confidence=0),
)
reference_area = ReferenceArea(
    geometric_area=GeometricArea(circle=Circle(radius=0), rectangle=None, ellipse=None),
    relevance_area=RelevanceArea(
        relevance_distance=RelevanceDistance(relevance_distance=1),
        relevance_traffic_direction=RelevanceTrafficDirection(relevance_traffic_direction=0),
    ),
)
location = Location(reference_position, reference_area)
```



### LDM Data Object
An LDM Data Object is an entity stored in the LDM, Data objects may originate from [__Cooperative Awareness Messages__](cooperative-awareness-messages.md) (CAMs), [__Decentralized Environmental Notification Messages__](decentralized-environmental-notification-messages.md) (DENMs), or other sources.

An example of a data object (i.e., actual CAM message in Dictionary format) from a CAM message is;
```py
data_object = {
                "header": {
                        "protocolVersion": 2, 
                        "messageId": 2, 
                        "stationId": 0
                        },
                "cam": {
                    "generationDeltaTime": 0,
                    "camParameters": {
                        "basicContainer": {
                            "stationType": 0,
                            "referencePosition": {
                                "latitude": 900000001,
                                "longitude": 1800000001,
                                "positionConfidenceEllipse": {
                                    "semiMajorAxisLength": 4095,
                                    "semiMinorAxisLength": 4095,
                                    "semiMajorAxisOrientation": 3601,
                                },
                                "altitude": {
                                    "altitudeValue": 800001,
                                    "altitudeConfidence": "unavailable",
                                },
                            },
                        },
                        "highFrequencyContainer": (
                            "basicVehicleContainerHighFrequency",
                            {
                                "heading": {"headingValue": 3601, "headingConfidence": 127},
                                "speed": {"speedValue": 16383, "speedConfidence": 127},
                                "driveDirection": "unavailable",
                                "vehicleLength": {
                                    "vehicleLengthValue": 1023,
                                    "vehicleLengthConfidenceIndication": "unavailable",
                                },
                                "vehicleWidth": 62,
                                "longitudinalAcceleration": {
                                    "value": 161,
                                    "confidence": 102,
                                },
                                "curvature": {
                                    "curvatureValue": 1023,
                                    "curvatureConfidence": "unavailable",
                                },
                                "curvatureCalculationMode": "unavailable",
                                "yawRate": {
                                    "yawRateValue": 32767,
                                    "yawRateConfidence": "unavailable",
                                },
                            },
                        ),
                    },
                },
            }
```

### LDM Area of Maintenance
The LDM Area of Maintenance defines the geographical region within which the LDM maintains data. This area is dynamically updated based on the host ITS-S location and is used to determine the validity of data objects.

The LDM must be declared with the LDM Area of Maintenance, this can be done easily with the following code;

Using the same [__Location Service__](location-service.md) that is used for the other layers of the V2X stack;
```py
location_service = LocationService()
```

We can create an LDM Location with the following line;
```py
ldm_location = Location.initializer()
```

The add a location callback to have the LDM Area of Maintenance be updated every time a new location (usually form a GPS service) recieves a new position;
```py
location_service.add_callback(ldm_location.location_service_callback)
```

So, bundling everything together the LDM Area of Maitenance can be declared with the following three lines of code;

```py

ldm_location = Location.initializer()
location_service.add_callback(ldm_location.location_service_callback)
```

```py
reference_position = ReferencePosition(
    latitude=0,
    longitude=0,
    position_confidence_ellipse=PositionConfidenceEllipse(
        semi_major_confidence=0,
        semi_major_orientation=0,
        semi_minor_confidence=0,
    ),
    altitude=Altitude(altitude_value=0, altitude_confidence=0),
)
reference_area = ReferenceArea(
    geometric_area=GeometricArea(circle=Circle(radius=0), rectangle=None, ellipse=None),
    relevance_area=RelevanceArea(
        relevance_distance=RelevanceDistance(relevance_distance=1),
        relevance_traffic_direction=RelevanceTrafficDirection(relevance_traffic_direction=0),
    ),
)
location = Location(reference_position, reference_area)
```

---

## Local Dynamic Map Interfacing Options

### LDM Publish Interface

To publish data to the LDM as an LDM Data Provider the following must be done;
```py
data = AddDataProviderReq(
    application_id=CAM,
    time_stamp=TimestampIts().insert_unix_timestamp(time.time()),
    location=Location.location_builder_circle(
        latitude=cam["cam"]["camParameters"]["basicContainer"][
            "referencePosition"
        ]["latitude"],
        longitude=cam["cam"]["camParameters"]["basicContainer"][
            "referencePosition"
        ]["longitude"],
        altitude=cam["cam"]["camParameters"]["basicContainer"][
            "referencePosition"
        ]["altitude"]["altitudeValue"],
        radius=0,
    ),
    data_object=cam,
    time_validity=TimeValidity(time_validity),
)

response = ldm.ldm_if_ldm_3.add_provider_data(data)
```

### LDM Query Interface
A data consumer requests specific data objects from the LDM using queries. The LDM returns matching objects that meet the requested criteria.

To query the LDM, a Request Data Object Request must be created;

```py
request_data_object = RequestDataObjectsReq(
    application_id=MAPEM,
    data_object_type=[CAM, VAM],
    priority=None,
    order=order,
    filter=filter,
)
```

Where the filter and order are;

```py
filter = Filter(
    FilterStatement(
        "header.stationId",
        ComparisonOperators(0),
        station_id,
    )
)

order = [OrderTuple("timeStamp", OrderingDirection(1))]
```

The filter is for the condition of "header.stationId == 0", and the order is a list of Orders, where each header from the [LDM Data Object](#ldm-data-object) can be used. Once the Request Data Objects Request has been declared the request for data object can be done;

```py
ldm_packets: RequestDataObjectsResp = self.ldm.request_data_objects(request_data_object)
```

### LDM Publish/Subscribe Interface
A data consumer subscribes to specific types of LDM Data Objects, receiving updates whenever relevant data changes or new data becomes available.

To subscribe to the LDM, a Subscribe Data Object Request must be used. Here the typical LDM parameters must be used, as well as an LDM Subscription Callback. 

```py
subscribe_data_consumer_response: SubscribeDataObjectsResp = ldm.if_ldm_4.subscribe_data_consumer(
    SubscribeDataobjectsReq(
        application_id=SPATEM,
        data_object_type=[CAM, VAM, DENM],
        priority=None,
        filter=None,
        notify_time=0.5,
        multiplicity=None,
        order=None,
    ),
    ldm_subscription_callback,
)
if subscribe_data_consumer_response.result.result != 0:
    raise Exception(f"Failed to subscribe to data objects: {str(subscribe_data_consumer_response.result)}")
```

This will call the ldm_subscrition_callback every 0.5 seconds (notifiy_time) with the Request Data Objects Response class.
---

## Quickstart

The Local Dynamic Map can be used in conjunction with the [__VRU Awareness Message__](vru-basic-service.md) in its simplest form as follows:

```py
import logging
import logging.config

from flexstack.facilities.vru_awareness_service.vru_awareness_service import VRUAwarenessService
from flexstack.facilities.vru_awareness_service.vam_transmission_management import DeviceDataProvider
from flexstack.utils.static_location_service import ThreadStaticLocationService as LocationService

from flexstack.facilities.local_dynamic_map.factory import LDMFactory
from flexstack.facilities.local_dynamic_map.ldm_classes import Location

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

# Facility - Local Dynamic Maps
ldm_location = Location.initializer()
location_service.add_callback(ldm_location.location_service_callback)
local_dynamic_map = LDMFactory(
    ldm_location, ldm_maintenance_type="Reactive", ldm_service_type="Reactive", ldm_database_type="Dictionary"
)

# Facility - Device Data Provider
device_data_provider = DeviceDataProvider()
device_data_provider.station_id = 1
device_data_provider.station_type = 2  # Cyclist

# Facility - VRU Awareness Service
vru_awareness_service = VRUAwarenessService(btp_router=btp_router,
                                            device_data_provider=device_data_provider, 
                                            ldm=local_dynamic_map)

location_service.add_callback(vru_awareness_service.vam_transmission_management.location_service_callback)

# Applications would be declared here
```

The only issue that may be encountered here is [__Networking Interface__](issues-networking-interface.md).

Logging is included to provide a way to visualize sent messages. View [Logging](logging.md) for detailed usage instructions.

---

## Interfacing with the VRU Basic Service

Interaction between the application layer and lower facility layers is done through the [__Local Dynamic Map__](local-dynamic-map.md).

---

Explore the example scripts available, expand upon them, or use them as a baseline to create your own implementations. If you have any questions, feel free to post in the [forum](forum-url).