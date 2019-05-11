#!/usr/bin/python3

import argparse
import ipaddress
import logging
import sys
from pyroute2 import IPDB

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)


def add_tunnel(args):
    """
    """
    ipdb = IPDB()
    try:
        ipdb.interfaces[args.physical_interface]
    except KeyError:
        logger.error(f"{args.physical_interface} interface does not exist")
        sys.exit()
    ipdb.interfaces[args.physical_interface].up()
    ipdb.interfaces[args.physical_interface].commit()
    ipdb.create(
        kind="vxlan",
        ifname=f"vxlan{args.vni}",
        vxlan_id=args.vni,
        vxlan_learning=1,
        vxlan_local=args.local_vtep,
        vxlan_group=args.remote_vtep
    )
    ipdb.interfaces[f"vxlan{args.vni}"].commit()
    ipdb.interfaces[f"vxlan{args.vni}"].up()
    ipdb.interfaces[f"vxlan{args.vni}"].commit()
    logger.info(f"vxlan interface vxlan{args.vni} created")
    ipdb.create(kind="bridge", ifname=f"br{args.vni}")
    ipdb.interfaces[f"br{args.vni}"].add_port(ipdb.interfaces[f"vxlan{args.vni}"].index)
    ipdb.interfaces[f"br{args.vni}"].add_port(ipdb.interfaces[args.physical_interface].index)
    ipdb.interfaces[f"br{args.vni}"].up()
    ipdb.interfaces[f"br{args.vni}"].commit()
    logger.info(f"bridge interface br{args.vni} created")
    logger.info(
        f"vxlan{args.vni} and {args.physical_interface} added to br{args.vni}"
    )

def delete_tunnel(args):
    """
    """
    ipdb = IPDB()
    try:
        ipdb.interfaces[args.physical_interface]
    except KeyError:
        logger.error(f"{args.physical_interface} interface does not exist")
        sys.exit()
    try:
        ipdb.interfaces[f"vxlan{args.vni}"]
    except KeyError:
        logger.error(f"vxlan{args.vni} interface does not exist")
        sys.exit()
    try:
        ipdb.interfaces[f"br{args.vni}"]
    except KeyError:
        logger.error(f"br{args.vni} interface does not exist")
        sys.exit()
    ipdb.interfaces[f"vxlan{args.vni}"].remove()
    logger.info(f"vxlan{args.vni} deleted")
    ipdb.interfaces[f"br{args.vni}"].remove()
    logger.info(f"br{args.vni} deleted")
    ipdb.commit()


def main(args):
    """
    """
    try:
        ipaddress.ip_address(args.local_vtep)
        ipaddress.ip_address(args.remote_vtep)
    except ValueError:
        logger.error(f"{args.local_vtep} invalid ip address")
        sys.exit()
    if args.delete:
        delete_tunnel(args)
    else:
        add_tunnel(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example script to build VXLAN tunnel")
    parser.add_argument(
        "--delete", 
        required=False, 
        action="store_true", 
        help="Delete VXLAN tunnel"
    )
    parser.add_argument(
        "--local_vtep", 
        required=True, 
        action="store", 
        help="Local VTEP ip address"
    )
    parser.add_argument(
        "--remote_vtep", 
        required=True, 
        action="store", 
        help="Remote VTEP ip address"
    )
    parser.add_argument(
        "--vni",
        required=True,
        action="store",
        type=int,
        help="VXLAN network identifier",
    )
    parser.add_argument(
        "--physical_interface",
        required=True,
        action="store",
        help="Physical interface to bridge",
    )
    args = parser.parse_args()
    sys.exit(main(args))
