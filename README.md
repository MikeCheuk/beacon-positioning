![](image/beacon_positioning.png)
# RSSI-based Positioning System for Autonomous Robots 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/3) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/MikeCheuk/beacon_positioning)
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
The algorithm read packets from all nearby ibeacons using [**beacontools**](https://github.com/citruz/beacontools) by citruz, which can be installed via:

    # install libbluetooth headers and libpcap2
    sudo apt-get install python3-dev libbluetooth-dev libcap2-bin
    # grant the python executable permission to access raw socket data
    sudo setcap 'cap_net_raw,cap_net_admin+eip' "$(readlink -f "$(which python3)")"
    # install beacontools with scanning support
    pip3 install beacontools[scan]

(Opt) The additional path planning algorithm depends on another module [**pathfinding**](https://github.com/brean/python-pathfinding), which can be installed via:

    pip3 install path_finding
    
The installation of this software can be achieved by:

    #install beacon_positioning
    pip3 install threading
    pip3 install beacon_positioning
  
## Usage
The following parameters are free to be modified:

1.RSSI-distance formula **(please do your own logarithmic regression)**

    def rssi_dist(self, rssi):
    self.D = 0.016690589*10**(-self.rssi/47.375)

2.Beacon coordinates conversion hashtable            

    #table1: bt_addr to x-coordinate
    x_coord = {
        '72:64:08:13:03:e2' : 0,   
        '72:64:08:13:03:e8' : 1,   
        '72:64:08:13:03:db' : 0,   
        '72:64:08:13:03:d8' : 1,
        #add new bt_addr : beacon_x here
        }

    #table2: bt_addr to y-coordinate
    y_coord = {
        '72:64:08:13:03:e2' : 0,   
        '72:64:08:13:03:e8' : 0,   
        '72:64:08:13:03:db' : 1,   
        '72:64:08:13:03:d8' : 1,
        #add new bt_addr : beacon_y here
        }
        
3.Repeating intervals for threading (in sec)

    t2 = 2                #for thread2 (create/update object)
    t3 = 6                #for thread3 (positioning)    

4.Kalman filter covariance:

    #initialize kalman variables
    R = 80          #noise covariance
    H = 1           #measurement
    Q = 10          #estimaton covariance
    P = 0           #error covariance (init=0) 
    X_hat = -30     #estimated RSSI
    K = 0           #kalman gain (init=0)
    
For **additional path planning:**

5.Map matrix

    # 0 : obstacle  
    # 1 : free passage
    map_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

6.A* setting

    xk, yk = 0, 0         #robot position 
    xe, ye = 6, 5         #destination position

## License
MIT 
