
#loads a file in the format 'wavelength in nm or m (separator) data'
# the separator can be ; , tab space

import csv
from numpy import array,zeros,interp

class Spectrum_loader:

    def __init__(self,filename):
    #test for delimiters
    
    #test ' '
        d = 0
        reader = csv.reader(open(filename), delimiter=' ')
        line = reader.next()
        if(len(line) > 1):
           d = ' '
    #test ';'
        reader = csv.reader(open(filename), delimiter=';')
        line = reader.next()
        if(len(line) > 1):
           d = ';'
    #test ','
        reader = csv.reader(open(filename), delimiter=',')
        line = reader.next()
        if(len(line) > 1):
           d = ','
    #test '\t'
        reader = csv.reader(open(filename), delimiter='\t')
        line = reader.next()
        if(len(line) > 1):
           d = '\t'
           
        if(d == 0):
            print 'could not load ',filename,' - no delimiter found'
            return None
        
        reader = csv.reader(open(filename), delimiter=d)
        dataX = []
        dataY = []
        for line in reader:
            dataX.append(float(line[0]))
            dataY.append(float(line[1]))
        
        self.wavelengths = array(dataX)
        self.delay = array(dataY)
        
        if(self.wavelengths[0] > 1e-3): #oh it is nm, convert to m
            self.wavelengths *= 1e-9
            
           
    def get_data_for_wavelengths(self,wavelengths): #lambdas must be increasing
        return interp(wavelengths,self.wavelengths,self.delay)
          
