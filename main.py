import random
import time

#0. initialization (global variables)

j = 0                  #beacon index (ie:bj)
xk = 0                 #robot position (xk, yk)
yk = 0    
robot_pos = [xk, yk]

class Beacon: 

    def __init__(self, bt_addr, index, x, y, rssi):  
        self.bt_addr = bt_addr
        self.beacon_index = index
        self.x = x
        self.y = y
        self.rssi = rssi
        self.D = 0
        self.sample_array = []
        self.temp = []

    def print_beacon(self):
        print('beacon index :', self.beacon_index )
        print('bt address :', self.bt_addr)
        print('(x,y) :', self.x, self.y)
        print('rssi :', self.rssi)
        print('sample_array :', self.sample_array)
        print(' ')

    def write_sample(self, sample_rssi):
        self.sample_array.append(sample_rssi)

    def rssi_dist(self, rssi):
        self.D = 0.016690589*10**(-self.rssi/47.375)       #from RSSI-distance equation          
        if len(self.sample_array) == 3:                    #limit the number of samples
            self.sample_array.pop(0)    

    #initialize kalman variables
    R = 80          #noise covariance
    H = 1           #measurement
    Q = 10          #estimaton covariance
    P = 0           #error covariance (init=0) 
    X_hat = -30     #estimated RSSI
    K = 0           #kalman gain (init=0)

    def kalman_filter(self,X):
        self.K = self.P*self.H/(self.H*self.P*self.H+self.R)
        self.X_hat = self.X_hat + self.K*(X-self.H*self.X_hat)
        self.P = (1-self.K*self.H)*self.P+self.Q
        return self.X_hat

    def kalman_call(self): #write the corrected RSSI from KF
        for i in range(len(self.sample_array)):
            self.temp.append(self.kalman_filter(self.sample_array[i]))  

        self.rssi = self.temp[-1]
        print('corrected RSSI = ' + str(self.rssi))
        self.temp.clear()

    def reset_kalman(self):
        R = 80           
        H = 1            
        Q = 10           
        P = 0           
        X_hat = -30     
        K = 0          

    def triangulation(x1, y1, x2, y2, x3, y3, D1, D2, D3):
        global xk
        global yk
        
        a = 2*(x2-x1)
        b = 2*(y2-y1)
        c = 2*(x3-x2)
        d = 2*(y3-y2)
        e = D1**2-D2**2-(x1**2-x2**2+y1**2-y2**2)
        f = D2**2-D3**2-(x2**2-x3**2+y2**2-y3**2)

        xk = (e*d-b*f)/(a*d-b*c)
        yk = (a*f-c*e)/(a*d-b*c)


#table1: bt_addr to x-coordinate
x_coord = {
    '72:64:08:13:03:e2' : 0,  #B1
    '72:64:08:13:03:e8' : 10, #B2
    '72:64:08:13:03:db' : 0,  #B3
    '72:64:08:13:03:d8' : 10  
    }

#table2: bt_addr to y-coordinate
y_coord = {
    '72:64:08:13:03:e2' : 0,  #B1
    '72:64:08:13:03:e8' : 0,  #B2
    '72:64:08:13:03:db' : 10, #B3
    '72:64:08:13:03:d8' : 10
    }

#link bt_addr & object index   
existing_beacon = {}

#link rssi & object index
rssi_comp = {}

run = True
while run:

    #incoming packets (with radom rssi):
    beacon_packets = [
        ['72:84:08:13:03:e8', random.randint(-60, -30)],
        ['72:84:08:13:03:e2', random.randint(-60, -30)],
        ['72:84:08:13:03:db', random.randint(-60, -30)],
        ['72:84:08:13:03:d8', random.randint(-60, -30)]
        ]

    #1. Beacon packet extraction
    for i in range(len(beacon_packets)): 
        if beacon_packets[i][0] not in existing_beacon:  #1.1. create beacon object

            for key in x_coord:
                if key is beacon_packets[i][0]:          # !Not Working, WIP
                    x = x_coord.get(key)

            for key in y_coord:
                if key == beacon_packets[i][0]:          # !Not Working, WIP
                    y = y_coord.get(key)

            bj = Beacon(beacon_packets[i][0], j,
                       x_coord.get(key), 
                       y_coord.get(key), 
                       beacon_packets[i][1])

            existing_beacon[str(bj.bt_addr)] = bj        #link existing beacons to object bj
            rssi_comp[ bj.rssi ] = bj                    #link object rssi to object bj
            bj.print_beacon()
            j = j+1                                      #index counter

        else:                                            #1.2. update beacon object 

            for u in existing_beacon:
                if u == beacon_packets[i][0]:
                    existing_beacon.get(u).write_sample(beacon_packets[i][1])


    #2. Kalman filter  

                    existing_beacon.get(u).kalman_call()
                    existing_beacon.get(u).reset_kalman()
                    existing_beacon.get(u).print_beacon()

    #print('existing beacon :', existing_beacon)          #shows the memory locations of existing objects


    #3. Sorting the cloest three beacons

    L = list(rssi_comp.keys())                           #extract rssi keys from dictionary for sorting

    #print('RSSI list :', rssi_comp)

    #temp storing variables
    m = -1000   #the largest
    n = -1000   #the second largest
    t = -1000   #the third largest

    L.sort(reverse = True)
    print("L :", L)

    tri_beacons = []                #store the 3 beacons for triangulation 

    for i in range(len(L)):
        if L[i] >= m:
            m = L[i]     
        elif L[i] >= n:
            n = L[i]
        elif L[i] >= t:
            t = L[i]
        else:
            continue

    for u in rssi_comp:
        if u == m:
            tri_beacons.append(rssi_comp.get(u))

    for u in rssi_comp:
        if u == n:
            tri_beacons.append(rssi_comp.get(u))

    for u in rssi_comp:
        if u == t:
            tri_beacons.append(rssi_comp.get(u))

    print('tri beacons :', tri_beacons)


    #4. RSSI-distance conversion

    tri_beacons[0].rssi_dist(tri_beacons[0].rssi)
    tri_beacons[1].rssi_dist(tri_beacons[1].rssi)
    tri_beacons[2].rssi_dist(tri_beacons[2].rssi)
    
    print('D1 :', tri_beacons[0].D)
    print('D2 :', tri_beacons[1].D)
    print('D3 :', tri_beacons[2].D)


    #5. Triangulation
    #Beacon.triangulation(tri_beacons[0].x, tri_beacons[0].y,
                         #tri_beacons[1].x, tri_beacons[1].y,
                         #tri_beacons[2].x, tri_beacons[2].y,
                         #tri_beacons[0].D,
                         #tri_beacons[1].D,
                         #tri_beacons[2].D)

    print('robot position :')
    print(robot_pos)

    time.sleep(3)


