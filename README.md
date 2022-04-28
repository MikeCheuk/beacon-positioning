![](image/beacon_positioning.png)
# Indoor Positioning System for Autonomous Robots 

###### *An EE final year student project bringing RSSI-based triangulation theory into a software application.* 
###### - The software is a proof of concept rather than a practical application as the accuracy of RSSI-distance conversion requires refinement. 
###### - The main.py is an all-in-one file containing all functionalities, though it may be tuned to your own liking. 
###### - The software **works only on Linux**, as the Windows version is solely for testing purposes.

## Overview

Objective - To develop a wireless positioning & navigation software for autonomous robots
- Implemented a class Beacon & Kalman filter for information received from Bluetooth beacons
- Modelled an RSSI-distance equation by experimental data with logarithmic regression
- Researched and applied RSSI-based triangulation technique for positioning the robot
- Introduced threading for packet receiving, data processing and triangulation  
- Implemented A* path planning, obstacle sensing & motion control algorithms

## Installation
The algorithm read packets from all nearby ibeacons using **beacontools** by citruz, which can be installed via:

    # install libbluetooth headers and libpcap2
    sudo apt-get install python3-dev libbluetooth-dev libcap2-bin
    # grant the python executable permission to access raw socket data
    sudo setcap 'cap_net_raw,cap_net_admin+eip' "$(readlink -f "$(which python3)")"
    # install beacontools with scanning support
    pip3 install beacontools[scan]

The installation of this software can be achieved by:

    #install beacon_positioning
    pip3 install beacon_positioning
  
## Usage


