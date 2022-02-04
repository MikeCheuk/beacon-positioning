import signal
from beacontools.scanner import Monitor, HCIVersion

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    beacon_packets.append([bt_addr , rssi])
    print(beacon_packets)
    beacon.clear()
    print(' ')
    
#scan from all beacons
monitor = Monitor(callback,
                  bt_device_id = 0,
                  device_filter = None,
                  packet_filter = None,
                  scan_parameters= {}
                 )

def main():
    monitor.get_hci_version = lambda: HCIVersion.BT_CORE_SPEC_4_2
    monitor.start()
    signal.pause()


if __name__ == '__main__':
    main()
