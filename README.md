# Linux VXLAN Tunnel Example Python Script

This script is for creating a point to point unicast VXLAN tunnel between two linux hosts.  This script is to be ran on each of the hosts.

## Prerequisites

>= python3.6
pipenv

## Installing

```
git clone https://github.com/briantsaunders/linux-vxlan-tunnel-example-script.git
cd linux-vxlan-tunnel-example-script
pipenv install
```

## Operation

### Args

| Option String | Required | Type    | Default | Example  | Description    |
|---------------|----------|---------|---------|----------|----------------|
| local_vtep    | True     | string  | none    | 10.0.0.1 | Local VXLAN tunnel endpoint  |
| remote_vtep   | True     | string  | none    | 10.0.0.2 | Remove VXLAN tunnel endpoint |
| vni           | True     | integer | none    | 100      | VXLAN network identifier     |
| physical_interface | True | string | none    | ens192   | Local interface to bridge to VXLAN Tunnel |
| delete | False | boolean | False | none | Deletes VXLAN tunnel |

### Run

#### Create

```
sudo python3 vxlan_tunnel_example.py --local_vtep 192.168.0.2 --remote_vtep 192.168.0.1 --vni 100 --physical_interface enp0s9
```

#### Delete

```
sudo python3 vxlan_tunnel_example.py --local_vtep 192.168.0.2 --remote_vtep 192.168.0.1 --vni 100 --physical_interface enp0s9 --delete
```