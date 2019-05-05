# Linux VXLAN Tunnel Example Python Script

This script is an example for how to create a point to point unicast VXLAN tunnel between two linux hosts via python.  Included is a vagrant file that will spin up a vagrant environment for testing the script functionality.

## Script Prerequisites

```
>= python3.6
pip3
bridge-utils
```

## Vagrant Environment

![environment](https://github.com/briantsaunders/linux-vxlan-tunnel-example-script/blob/master/docs/environment.PNG?raw=true)

Vagrant and virtualbox should be installed prior to bringing up the vagrant environment.

The vagrant environment is simulating two sites connected by an isp.  The routers (circles in the  diagram) are Ubuntu 18.04 with [FRRouting](https://frrouting.org/) installed.  The servers (squares in the diagram) are vanilla Ubuntu 18.04.

Following the below instructions the script will form a VXLAN tunnel overlay between the two site routers allowing the two servers to talk to each other as if they were directly connected.  Without the tunnel they are unable to communicate with each other.

### Vagrant Up

```
git clone https://github.com/briantsaunders/linux-vxlan-tunnel-example-script.git
cd linux-vxlan-tunnel-example-script
vagrant up
```

Ansible is used to provision the vagrant boxes.  It will configure FRRouting on the routers, install pip3 on the site routers, and will pip3 install the requirements.txt on the site routers.  Check out the playbook pb.conf.all.yml for more details.

### Testing in Vagrant

Once the vagrant environment is up issue the following commands to configure the VXLAN tunnel and validate.

Configure sie1router:
```
vagrant ssh site1router
cd /vagrant
sudo python3 linux_vxlan_tunnel_example.py --local_vtep 192.168.0.2 --remote_vtep 192.168.0.5 --vni 100 --physical_interface enp0s9
```

Configure site2router:
```
vagrant ssh site2router
cd /vagrant
sudo python3 linux_vxlan_tunnel_example.py --local_vtep 192.168.0.5 --remote_vtep 192.168.0.2 --vni 100 --physical_interface enp0s9
```

Validate site1server and ping site2server:
```
vagrant ssh site1server
ping 172.16.0.11
```

## Script Operation

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
sudo python3 run python vxlan_tunnel_example.py --local_vtep 192.168.0.2 --remote_vtep 192.168.0.1 --vni 100 --physical_interface enp0s9
```

#### Delete

```
sudo python3 run python vxlan_tunnel_example.py --local_vtep 192.168.0.2 --remote_vtep 192.168.0.1 --vni 100 --physical_interface enp0s9 --delete
```
