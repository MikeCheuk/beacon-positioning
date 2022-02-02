import numpy as np
import matplotlib.pyplot as plt  
import random

class Kalman:
    def __init__(self, R, H, Q, P, X_hat, K):
        self.R = R           #noise covariance
        self.H = H           #measurement
        self.Q = Q           #estimaton covariance
        self.P = P           #error covariance (init=0) 
        self.X_hat = X_hat   #estimated RSSI
        self.K = K           #kalman gain (init=0)
    
    def kalman_filter(self,X):
        self.K = self.P*self.H/(self.H*self.P*self.H+self.R)
        self.X_hat = self.X_hat + self.K*(X-self.H*self.X_hat)
        self.P = (1-self.K*self.H)*self.P+self.Q

        return self.X_hat 

#N noise RSSI measurements from one time step:
#(will be refreshed every time step)
samples = np.array([-33, -31, -35, -39, -42, -28, -30, -50, -38, -33, -34, -25])


x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])

#for temporary storage  
temp = []

#for corrected data (culmulative)
rssi = []       

           #R  #H  #Q #P #Xh #K
kf = Kalman(80, 1, 10, 0, 0, 0)

#loop:
print('Number of data:' + str(len(samples)))

for i in range(len(samples)):
    temp.append(kf.kalman_filter(samples[i]))  
    print(temp[i])

plt.plot(x,samples)
plt.plot(x,temp)
plt.title('Kalman Filter')
plt.xlabel('sampled data ')
plt.ylabel('RSSI')
plt.legend(['Raw data','With Kalman Filter'])
plt.show()
rssi.append(temp[-1])
#print(rssi)

#reset the kalman gain & covariance for next iteration
kf = Kalman(80, 1, 10, 0, 0, 0)
