import argparse

import logging

from flexstack.metrics.metrics_exposer import MetricsExposer

from flexstack.facilities.vru_awareness_service.vru_awareness_service import VRUAwarenessService
from flexstack.facilities.vru_awareness_service.vam_transmission_management import DeviceDataProvider
from flexstack.utils.static_location_service import ThreadStaticLocationService as LocationService

from flexstack.facilities.local_dynamic_map.factory import ldm_factory
from flexstack.facilities.local_dynamic_map.ldm_classes import Location

from flexstack.btp.router import Router as BTPRouter

from flexstack.geonet.router import Router
from flexstack.geonet.mib import MIB
from flexstack.geonet.gn_address import GNAddress, M, ST, MID

from flexstack.linklayer.raw_link_layer import RawLinkLayer


def parse_mac_address_to_int(mac_address: str):
    mac_address = mac_address.split(":")
    mac_address = [int(x, 16) for x in mac_address]
    return bytes(mac_address)


def main(args: argparse.Namespace) -> None:
    logging.basicConfig(level=logging.INFO)

    # Geonet
    mac_address = parse_mac_address_to_int(args.mac_address)
    mib = MIB()
    gn_addr = GNAddress()
    gn_addr.set_m(M.GN_MULTICAST)
    gn_addr.set_st(ST.CYCLIST)
    gn_addr.set_mid(MID(mac_address))
    mib.itsGnLocalGnAddr = gn_addr
    gn_router = Router(mib=mib, sign_service=None)

    # Link-Layer
    ll = RawLinkLayer(iface=args.interface, mac_address=mac_address, receive_callback=gn_router.gn_data_indicate)
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
    local_dynamic_map = ldm_factory(
        ldm_location, ldm_maintenance_type="Reactive", ldm_service_type="Reactive", ldm_database_type="Dictionary"
    )

    # Facility - Device Data Provider
    device_data_provider = DeviceDataProvider()
    device_data_provider.station_id = args.station_id
    device_data_provider.station_type = 2  # Cyclist

    # Facility - VRU Awareness Service
    vru_awareness_service = VRUAwarenessService(
        btp_router=btp_router, device_data_provider=device_data_provider, ldm=local_dynamic_map
    )

    location_service.add_callback(vru_awareness_service.vam_transmission_management.location_service_callback)

    # Metrics
    metrics_exposer = MetricsExposer("Test-ITS-Station", local_dynamic_map, ldm_location)
    vru_awareness_service.add_metrics_callback(metrics_exposer.facility_level_callback)
    local_dynamic_map.add_metrics_callback(metrics_exposer.ldm_callback)
    gn_router.add_metrics_callback(metrics_exposer.gn_level_callback)

    location_service.location_service_thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a C-ITS station.")
    parser.add_argument(
        "--station-id",
        type=int,
        default="1",
        help="Station ID for C-ITS Station",
    )
    parser.add_argument(
        "--mac-address",
        type=str,
        default="aa:bb:cc:11:22:33",
        help='The MAC address to send CAMs to (e.g. "aa:bb:cc:dd:ee:ff")',
    )
    parser.add_argument(
        "--interface",
        type=str,
        default="lo",
        help='The interface to use for sending CAMs (e.g. "lo")',
    )
    main(parser.parse_args())
