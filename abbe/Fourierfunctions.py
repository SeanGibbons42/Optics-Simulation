import numpy as np
import matplotlib.pyplot as plt

def TwoDfft(arr):
    fftdata = np.array(np.fft.fft2(arr),dtype=np.float32)
    fig,(ax1,ax2) = plt.subplots(1,2)

    ax1.imshow(data)
    ax2.imshow(fftdata)

    plt.show()

def oneDfft(arr):
    fftdata = np.abs(np.array(np.fft.fft(arr),dtype=np.float32)[1:])
    fig,(ax1,ax2) = plt.subplots(1,2)

    fftdata = fftdata[:int(len(fftdata)/2)]
    fftdata = np.concatenate((np.flip(fftdata,0),fftdata))

    ax1.plot(data)
    ax2.plot(fftdata)

    plt.show()

#data = [(np.sin(x))*(np.cos(y)) for (x,y) in (range(100),range(100))]
#TwoDfft(data)

#data = [10,10,10,10,10,10,10,10,10,10,0,0,0,0,0,0,0,0,0,0]*10
data = np.array([(np.sin(x/15))+100 for x in range(1000)])
oneDfft(data)
