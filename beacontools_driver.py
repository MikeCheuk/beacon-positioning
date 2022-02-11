import signal
from beacontools.scanner import Monitor, HCIVersion

packet_size = 15

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    beacon_packets.append([bt_addr , rssi])
    print(beacon_packets)
    print(' ')    
    if len(beacon_packets) == packet_size:
        beacon_packets.pop(0)
        

#scan from all beacons
monitor = Monitor(callback,
                  bt_device_id = 0,
                  device_filter = None,
                  packet_filter = None,
                  scan_parameters= {}
                 )


monitor.get_hci_version = lambda: HCIVersion.BT_CORE_SPEC_4_2
monitor.start()
signal.pause()

