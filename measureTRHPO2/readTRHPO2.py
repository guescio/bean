#!/usr/bin/env python
#A script to read temperature, relative humidity, barometric pressure, oxygen level and battery level and print, plot or save the data.

#BME280: t, rh, dp, p
#SHT35:  t, rh, dp
#oxygen: o2
#bean:   t, v

#******************************************
__version__ = '0.0'

#******************************************
#import stuff
import serial, time, sys, collections, os, argparse
import matplotlib.pyplot as plt

#******************************************
def readTRHPO2(args):
    
    #plot interactively
    plt.ion()

    #create collections limited in length for plotting
    length = 600
    times = collections.deque(maxlen=length)

    #BME280
    nbme = 4 #measurements by BME280
    tbme  = collections.deque(maxlen=length)
    rhbme = collections.deque(maxlen=length)
    dpbme = collections.deque(maxlen=length)
    pbme  = collections.deque(maxlen=length)

    #SHT35
    nsht = 3 #measurements by SHT35
    tsht  = collections.deque(maxlen=length)
    rhsht = collections.deque(maxlen=length)
    dpsht = collections.deque(maxlen=length)

    #oxygen
    nox2 = 1 #measurements by oxygen sensor
    o2 = collections.deque(maxlen=length)

    #bean
    nbean = 2 #measurements by bean
    tb = collections.deque(maxlen=length)
    vb = collections.deque(maxlen=length)
    
    #create serial object to read from LightBlue Bean
    ser = serial.Serial('/tmp/cu.LightBlue-Bean')#, timeout=10)

    #time
    start = None

    try:

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
            expectedMeasurements=0
            if args.bme: expectedMeasurements+=nbme
            if args.sht: expectedMeasurements+=nsht
            if args.ox2: expectedMeasurements+=nox2
            expectedMeasurements+=nbean

            if len(values.split()) == expectedMeasurements:
            
                #append time to collection for plotting
                if start is None:
                    start = time.time()
                times.append(time.time() - start)
                    
                #parse serial output and append to collections for plotting
                if args.bme:
                    tbme.append(  float( values.split()[0]))
                    rhbme.append( float( values.split()[1]))
                    dpbme.append( float( values.split()[2]))
                    pbme.append(  float( values.split()[3]))
                if args.sht:
                    tsht.append(  float( values.split()[0 + args.bme*nbme]))
                    rhsht.append( float( values.split()[1 + args.bme*nbme]))
                    dpsht.append( float( values.split()[2 + args.bme*nbme]))
                if args.ox2:
                    o2.append( float( values.split()[0 + args.bme*nbme + args.sht*nsht]))
                tb.append( float( values.split()[0 + args.bme*nbme + args.sht*nsht + args.ox2*nox2]))
                vb.append( float( values.split()[1 + args.bme*nbme + args.sht*nsht + args.ox2*nox2]))
            
                #plot
                if args.draw:
                    plt.cla()#clear axes
                    if args.bme:
                        plt.plot(times, tbme,  color='red', label='t$_{BME}$ [C]')
                        plt.plot(times, rhbme, color='cyan', label='RH$_{BME}$ [%]')
                        plt.plot(times, dpbme, color='orange', label='DP$_{BME}$ [C]')
                        if not args.nop:
                            plt.plot(times, pbme, color='lime', label='p$_{BME}$ [hPa]')
                    if args.sht:
                        plt.plot(times, tsht,  color='darkred', label='t$_{SHT}$ [C]')
                        plt.plot(times, rhsht, color='darkcyan', label='RH$_{SHT}$ [%]')
                        plt.plot(times, dpsht, color='darkorange', label='DP$_{SHT}$ [C]')
                    if args.ox2:
                        plt.plot(times, o2,    color='blue', label='O$_{2}$ [%]')
                    plt.plot(times, tb, color='salmon', label='t$_{bean}$ [C]')
                    plt.plot(times, vb, color='green', label='v$_{bean}$ [V]')
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
    parser.add_argument('--bme', dest='bme', action='store_true', default=False, help='BME280')
    parser.add_argument('--sht', dest='sht', action='store_true', default=False, help='SHT35')
    parser.add_argument('--ox2', dest='ox2', action='store_true', default=False, help='oxygen')
    parser.add_argument('-ly', '--logy', dest='logy', action='store_true', default=False, help='logarithmic y axis')
    parser.add_argument('--nop', dest='nop', action='store_true', default=False, help='do not draw pressure')
    args = parser.parse_args()

    readTRHPO2(args)
