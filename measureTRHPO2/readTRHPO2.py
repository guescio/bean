#!/usr/bin/env python
#A script to read temperature, relative humidity, dew point, barometric pressure and battery level and print, plot or save the data.

#SHT35:  t, rh, dp
#BME280: p, (t, rh, dp)
#bean:   v, (t)

#******************************************
__version__ = '0.2'

#******************************************
#import stuff
import serial, time, sys, collections, os, argparse
import matplotlib.pyplot as plt

#******************************************
def readTRHPO2(args):

    #measurements flags
    if args.t or args.rh or args.dp or args.p or args.v:
        args.all = False
    if args.all:
        args.t  = True
        args.rh = True
        args.dp = True
        args.p  = True
        args.v  = True
    if args.nop:
        args.p = False
    
    #plot interactively
    plt.ion()

    #expected number of measurements
    expectedMeasurements=5
    
    #create collections limited in length for plotting
    length = 600
    times = collections.deque(maxlen=length)

    #SHT35
    tsht  = collections.deque(maxlen=length)#temperature
    rhsht = collections.deque(maxlen=length)#relative humidity
    dpsht = collections.deque(maxlen=length)#dew point

    #BME280
    pbme  = collections.deque(maxlen=length)#pressure
    
    #bean
    vb = collections.deque(maxlen=length)#battery voltage
    
    #create serial object to read from LightBlue Bean
    ser = serial.Serial('/tmp/cu.LightBlue-Bean')#, timeout=10)

    #time
    start = None

    try:

        #measuements and units
        if args.verbose:
            print('date           T[C] RH[%] DP[C] P[hPa] V[V]')
        
        #loop
        while True:
        
            #read line from serial output
            values = str(ser.readline().decode('utf-8')).strip()
            
            #print time stamp and serial output
            timestamp = time.strftime('%Y%m%d%H%M%S')
            if args.verbose:
                print(timestamp, values)

            #save data locally
            if args.save:
                
                #check and create data directory
                directory = os.path.dirname(os.path.realpath(__file__))+'/data/'+time.strftime('%Y')+'/'+time.strftime('%m')
                if not os.path.exists(directory):
                    os.makedirs(directory)

                #store data locally
                with open(directory+"/"+time.strftime('%Y%m%d')+".log", "a") as f:
                    f.write(timestamp + " " + values + "\n")
        
            #check if the serial output has the expected number of entries
            if len(values.split()) == expectedMeasurements:
            
                #append time to collection for plotting
                if start is None:
                    start = time.time()
                times.append(time.time() - start)
                    
                #parse serial output and append to collections for plotting
                tsht.append(  float( values.split()[0]))
                rhsht.append( float( values.split()[1]))
                dpsht.append( float( values.split()[2]))
                pbme.append(  float( values.split()[3]))
                vb.append(    float( values.split()[4]))
            
                #plot
                if args.draw:
                    plt.cla()#clear axes
                    if args.t:
                        plt.plot(times, tsht,  color='darkred',    label='t$_{SHT}$ [C]')
                    if args.rh:
                        plt.plot(times, rhsht, color='darkcyan',   label='RH$_{SHT}$ [%]')
                    if args.dp:
                        plt.plot(times, dpsht, color='darkorange', label='DP$_{SHT}$ [C]')
                    if args.p:
                        plt.plot(times, pbme,  color='indigo',       label='p$_{BME}$ [hPa]')
                    if args.v:
                        plt.plot(times, vb,    color='darkgreen',      label='v$_{bean}$ [V]')
                    plt.legend(fontsize='x-small', loc=2)
                    if args.logy:
                        plt.yscale('log')
                    plt.xlabel('time [s]')
                    plt.draw()
                    plt.pause(0.1)

            else:
                print("the number of measurements does not match the expected number from the sensors listed")
                #sys.exit(0)

    except KeyboardInterrupt:
        print
        sys.exit(0)

#******************************************
if __name__ == '__main__':

    #parse input arguments
    parser = argparse.ArgumentParser(description='%prog [options]')
    parser.add_argument('-s', '--save', dest='save', action='store_true', default=False, help='save data')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='verbose mode')
    parser.add_argument('-d', '--draw', dest='draw', action='store_true', default=False, help='draw')
    parser.add_argument('-ly', '--logy', dest='logy', action='store_true', default=False, help='logarithmic y axis')
    parser.add_argument('--nop', dest='nop', action='store_true', default=False, help='do not draw pressure')
    parser.add_argument('--all', dest='all', action='store_true', default=True, help='all measurements')
    parser.add_argument('--t',  dest='t',  action='store_true', default=False, help='temperature')
    parser.add_argument('--rh', dest='rh', action='store_true', default=False, help='relative humidity')
    parser.add_argument('--dp', dest='dp', action='store_true', default=False, help='dew point')
    parser.add_argument('--p',  dest='p',  action='store_true', default=False, help='pressure')
    parser.add_argument('--v',  dest='v',  action='store_true', default=False, help='voltage')
    args = parser.parse_args()

    readTRHPO2(args)
