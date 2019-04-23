import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading



class CubeAudio(object):
    def __init__(self, chunksize=2**10, rate=16000, trim=20):

        self.RATE = rate
        self.CHUNK = chunksize
        self.TRIM = trim

        self.p = pyaudio.PyAudio()  # start pyaudio
        self.stream = self.p.open(format=pyaudio.paInt32, channels=1, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)  # Startup a stream of pyaudio that reads 32 bit ints

        self.maxf = self.RATE / 2  # maximum frequency calculated by the fourier transform
        self.fstep = self.maxf / self.CHUNK  # step in the x axis
        # lowest frequency that will be shown on the plot
        self.minf = self.fstep * self.TRIM

        # calculate a hanning function for smoothing
        self.window = np.hanning(self.CHUNK)

    ##################################
    # SETTERS
    def setrate(self, rate):
        self.RATE = rate
        self.stream = self.p.open(format=pyaudio.paInt32, channels=1, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)  # Startup a stream of pyaudio that reads 32 bit ints
        self.maxf = self.RATE / 2  # maximum frequency calculated by the fourier transform
        self.fstep = self.maxf / self.CHUNK  # step in the x axis
        # lowest frequency that will be shown on the plot
        self.minf = self.fstep * self.TRIM

    def setchunksize(self, chunksize):
        self.CHUNK = chunksize
        self.stream = self.p.open(format=pyaudio.paInt32, channels=1, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)  # Startup a stream of pyaudio that reads 32 bit ints
        self.maxf = self.RATE / 2  # maximum frequency calculated by the fourier transform
        self.fstep = self.maxf / self.CHUNK  # step in the x axis
        # lowest frequency that will be shown on the plot
        self.minf = self.fstep * self.TRIM
        # calculate a hanning function for smoothing
        self.window = np.hanning(self.CHUNK)

    def settrim(self, trim):
        self.TRIM = trim
        self.stream = self.p.open(format=pyaudio.paInt32, channels=1, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)  # Startup a stream of pyaudio that reads 32 bit ints
        self.maxf = self.RATE / 2  # maximum frequency calculated by the fourier transform
        self.fstep = self.maxf / self.CHUNK  # step in the x axis
        # lowest frequency that will be shown on the plot
        self.minf = self.fstep * self.TRIM

    def setstream(self, newstream):
        self.stream = newstream

    ###################################
    # GETTERS
    def getrate(self):
        return self.RATE

    def getchunksize(self):
        return self.CHUNK

    def gettrim(self):
        return self.TRIM

    def getstream(self):
        return self.stream

    ###################################
    # Other Functions

    def readfourier(self):
        '''Reads a CHUNK of data from the pyaudio stream then performs a fourier transform and returns that array trimmed at low frequency by TRIM points'''

        # Read one CHUNK from the stream
        ydata = np.fromstring(self.stream.read(self.CHUNK), dtype=np.int32)
        # Detrend data, this was suggested on the internet. Moves the wave so it is centered at 0
        data = ydata - np.mean(ydata)
        # Apply a window Function, apparently this makes your data better
        data = data * self.window

        # do a real fourier transform on the data
        ytransform = np.abs(np.fft.rfft(data))

        return ytransform[self.TRIM:]

    def readrawdata(self):
        data = np.fromstring(self.stream.read(self.CHUNK), dtype=np.int32)
        return data

    def xvalues(self):
        '''gives an array of x values (frequency values) that match readfourier for plotting purposes'''
        x = np.linspace(self.minf, self.maxf, (self.CHUNK / 2) - self.TRIM +
                        1)  # x axis based on sampling rate, chunk size, and TRIM

        return x

    def shutdown(self):
        # Closes out pyaudio

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

def fouriergraph():
    fig,(ax1,ax2) = plt.subplots(2,1)  # Create a matplotlib figure
    # add a subplot that we can animate (Constantly Update)

    f = CubeAudio()  # start a cubeaudio instance

    x = f.xvalues()  # get the x axis for the plot


    def animate(i):
        y = f.readfourier()  # pull some y values
        r = np.array(f.readrawdata())
        rawx = range(len(r))
        # reset the plot then plot again
        ax1.clear()
        ax2.clear()
        ax1.set_ylim([0, 10**10.5])
        ax2.set_ylim(-5*10**8,5*10**8)
        ax1.plot(x, y)
        ax2.plot(rawx,r)

    # run our animation with pauses of length interval
    ani = animation.FuncAnimation(fig, animate, interval=1000 / 60)
    plt.show()

def audioimage():
    fig,(ax1,ax2) = plt.subplots(2,1)  # Create a matplotlib figure
    # add a subplot that we can animate (Constantly Update)

    f = CubeAudio()  # start a cubeaudio instance

    x = f.xvalues()  # get the x axis for the plot
    size = len(f.readrawdata())
    image = np.zeros((size,size))
    def animate(i):
        for i in range(len(image)-1):
            image[-1-i] = image[-2-i]
        image[0] = np.array(np.log(np.abs(f.readrawdata())))

        r = np.array(f.readrawdata())
        rawx = range(len(r))
        # reset the plot then plot again
        ax1.clear()
        ax2.clear()
        ax1.imshow(image,vmin=0,vmax=20)
        ax2.imshow(np.array(np.fft.fft2(image),dtype=np.float32))

    # run our animation with pauses of length interval
    ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()

fouriergraph()
