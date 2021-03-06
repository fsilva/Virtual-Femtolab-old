
import gtk

#import pylab
from matplotlib.figure import Figure
from numpy import *

from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

class Plots:
    def __init__(self):
        pass
        
    def init_plots(self,box):
    # set a 3x2 grid, 1 Vbox, 2 Hboxes
        self.Vbox = gtk.VBox(False, 0)   
        
    #setup Hbox1
        self.Hbox1 = gtk.HBox(False, 0)
    # setup 3 plots and pack them
    
        self.pulse_figure  = Figure(figsize=(5,4), dpi=66,facecolor='w')
        self.pulse_subplot = self.pulse_figure.add_subplot(111)
        canvas = FigureCanvas(self.pulse_figure) 
        self.Hbox1.pack_start(canvas,True,True,0)
        
        self.beam_figure  = Figure(figsize=(5,4), dpi=66,facecolor='w')
        self.beam_subplot = self.beam_figure.add_subplot(111)
        canvas = FigureCanvas(self.beam_figure)  
        self.Hbox1.pack_start(canvas,True,True,0)
        
        self.autoco_figure  = Figure(figsize=(5,4), dpi=66,facecolor='w')
        self.autoco_subplot_1 = self.autoco_figure.add_subplot(211)
        self.autoco_subplot_2 = self.autoco_figure.add_subplot(212)
        canvas = FigureCanvas(self.autoco_figure)  
        self.Hbox1.pack_start(canvas,True,True,0)
    
    # pack Hbox1 in the Vbox
        self.Vbox.pack_start(self.Hbox1,True,True,0)   
    #setup Hbox2
        self.Hbox2 = gtk.HBox(False, 0)   
    # setup 3 plots and pack them
        self.spectrum_figure    = Figure(figsize=(5,4), dpi=66,facecolor='w')
        self.spectrum_subplot_1 = self.spectrum_figure.add_subplot(111)
        self.spectrum_subplot_2 = self.spectrum_subplot_1.twinx()
        canvas = FigureCanvas(self.spectrum_figure)  # a gtk.DrawingArea
        self.Hbox2.pack_start(canvas,True,True,0)
        
        self.statistics_figure  = Figure(figsize=(5,4), dpi=66,facecolor='w')
        self.statistics_subplot = self.statistics_figure.add_subplot(111)
        canvas = FigureCanvas(self.statistics_figure)  # a gtk.DrawingArea
        self.Hbox2.pack_start(canvas,True,True,0)
        
        self.FROG_figure  = Figure(figsize=(5,4), dpi=66,facecolor='w')
        self.FROG_subplot = self.FROG_figure.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)
        self.FROG_subplot.plot(t,s)
        canvas = FigureCanvas(self.FROG_figure)  # a gtk.DrawingArea
        self.Hbox2.pack_start(canvas,True,True,0)
    
    # pack Hbox2 in the Vbox
        self.Vbox.pack_start(self.Hbox2,True,True,0)       
    
    #add the Vbox to the root box
        box.pack_start(self.Vbox,True,True,0)
        
    
        
    def draw_pulse(self,pulsebeam):
        envelope = abs(pulsebeam.ElectricField[:])
        self.pulse_plot1, = self.pulse_subplot.plot(pulsebeam.t,pulsebeam.ElectricField[:].real,'b')
        self.pulse_plot2, = self.pulse_subplot.plot(pulsebeam.t,envelope,'r')
        self.pulse_subplot.set_title('Electric Field')
        
        fwhm1,fwhm2 = pulsebeam.calc_fwhm()
        
        self.pulse_annotation1 = self.pulse_subplot.annotate('FWHM(gaussian fit)= %3.3f fs'%(fwhm1*1e15), xy=(0.65, 0.15),  xycoords='figure fraction', horizontalalignment='center', verticalalignment='center')
        self.pulse_annotation2 = self.pulse_subplot.annotate('               FWHM  = %3.3f fs'%(fwhm2*1e15), xy=(0.65, 0.25),  xycoords='figure fraction', horizontalalignment='center', verticalalignment='center')
        
    def update_pulse(self,pulsebeam):
        envelope = abs(pulsebeam.ElectricField[:])
        self.pulse_subplot.set_ylim((-1.1*pulsebeam.amplitudeE,1.1*pulsebeam.amplitudeE)) 
        self.pulse_plot1.set_ydata(pulsebeam.ElectricField[:].real)
        self.pulse_plot2.set_ydata(envelope)

        fwhm1,fwhm2 = pulsebeam.calc_fwhm()
        
        self.pulse_annotation1.set_text('FWHM(gaussian fit)= %3.3f fs'%(fwhm1*1e15))
        self.pulse_annotation2.set_text('               FWHM  = %3.3f fs'%(fwhm2*1e15))
        
        self.pulse_figure.canvas.draw()
        
        
    def adjust_phase(self,phase,absSpectrum):
        max_spectrum = max(absSpectrum)
        mmax = -1e15
        mmin = 1e15
        for k in xrange(len(phase)):
            if(absSpectrum[k] < 0.001*max_spectrum):
                phase[k] = 10000 #these points should disappear. (ugly hack)
            else:
                if(phase[k] > mmax):
                    mmax = phase[k]
                if(phase[k] < mmin):
                    mmin = phase[k]
                    
        phase -= mmin
        delta = (mmax-mmin)*0.5
        
        return  -delta,mmax-mmin+delta
        
    

    def draw_spectrum(self,pulsebeam):
        absSpectrum = abs(pulsebeam.Spectrum[:])
        max_scale = max(absSpectrum)
        absSpectrum /= max_scale #normalize
        phase = unwrap(angle(pulsebeam.Spectrum[:]))
        a,b=self.adjust_phase(phase,absSpectrum)
        self.spectrum_plot1, = self.spectrum_subplot_1.plot(pulsebeam.frequencies,absSpectrum,'g')
        self.spectrum_plot2, = self.spectrum_subplot_2.plot(pulsebeam.frequencies,phase,'.')
        self.spectrum_subplot_2.set_ylim((a,b))  
        self.spectrum_subplot_1.set_title('Spectrum')
        #draw 800 nm, 400 nm, 1200 nm,600nm
        max_scale = max(absSpectrum)
        self.spectrum_800nm = self.spectrum_subplot_1.annotate('800nm', xy=(3e8/800e-9, max_scale),  xycoords='data', \
                xytext=(0.0, -15), textcoords='offset points', \
                arrowprops=dict(facecolor='black', arrowstyle="->"),\
                horizontalalignment='center', verticalalignment='center')
        self.spectrum_400nm = self.spectrum_subplot_1.annotate('400nm', xy=(3e8/400e-9, max_scale),  xycoords='data', \
                xytext=(0.0, -15), textcoords='offset points', \
                arrowprops=dict(facecolor='black', arrowstyle="->"),\
                horizontalalignment='center', verticalalignment='center')
        self.spectrum_1200nm = self.spectrum_subplot_1.annotate('1.2um', xy=(3e8/1200e-9, max_scale),  xycoords='data', \
                xytext=(0.0, -30), textcoords='offset points', \
                arrowprops=dict(facecolor='black', arrowstyle="->"),\
                horizontalalignment='center', verticalalignment='center')
        self.spectrum_600nm = self.spectrum_subplot_1.annotate('600nm', xy=(3e8/600e-9, max_scale),  xycoords='data', \
                xytext=(0.0, -30), textcoords='offset points', \
                arrowprops=dict(facecolor='black', arrowstyle="->"),\
                horizontalalignment='center', verticalalignment='center')

    def update_spectrum(self,pulsebeam):
        absSpectrum = abs(pulsebeam.Spectrum[:])
        max_scale = max(absSpectrum)
        absSpectrum /= max_scale #normalize
        phase = unwrap(angle(pulsebeam.Spectrum[:]))
        
        a,b = self.adjust_phase(phase,absSpectrum)
        
        self.spectrum_plot1.set_ydata(absSpectrum)
        self.spectrum_plot2.set_ydata(phase)
        self.spectrum_subplot_1.set_ylim((min(absSpectrum),max(absSpectrum))) 
        
        self.spectrum_subplot_2.set_ylim((a,b))          
        
        self.spectrum_figure.canvas.draw()
        

        
    def draw_autoco(self,pulsebeam):
        self.autoco_plot1, = self.autoco_subplot_1.plot(pulsebeam.t,pulsebeam.AutoCo,'b')
        self.autoco_plot2, = self.autoco_subplot_1.plot(pulsebeam.t,pulsebeam.IntensiometricAutoCo,'r')
        self.autoco_plot3, = self.autoco_subplot_2.plot(pulsebeam.t[:len(pulsebeam.t)/2],log(abs(pulsebeam.AutoCoFFT)),'b')
        self.autoco_subplot_1.set_title('Interferometric Autocorrelation')
        self.autoco_subplot_2.set_ylim(-10,0)
        
    def update_autoco(self,pulsebeam):
        self.autoco_plot1.set_ydata(pulsebeam.AutoCo)
        self.autoco_plot2.set_ydata(pulsebeam.IntensiometricAutoCo)
        self.autoco_plot3.set_ydata(log(abs(pulsebeam.AutoCoFFT[:len(pulsebeam.t)/1])))
        self.autoco_figure.canvas.draw()
        
    def calc_FROG(self,pulsebeam):
        return 0,shape(pulsebeam.FROG)[0],0,shape(pulsebeam.FROG)[1]
    # calculate the interesting part of the FROG (different from zero)
        max_frog = pulsebeam.FROG.max()
        len_x = pulsebeam.FROG.shape[0]
        len_y = pulsebeam.FROG.shape[1]
        i = 0
        while(sum(pulsebeam.FROG[i,:]) < 1e-3*max_frog and i < len_x):
            i+=1
        j = len_x-1
        while(sum(pulsebeam.FROG[j,:]) < 1e-3*max_frog and j > 0):
            j-=1
        k = 0
        while(sum(pulsebeam.FROG[:,k]) < 1e-3*max_frog and k < len_y):
            k+=1
        l = len_y-1
        while(sum(pulsebeam.FROG[:,l]) < 1e-3*max_frog and l > 0):
            l-=1
        return i,j,k,l
       

    def draw_FROG(self,pulsebeam):
        i,j,k,l = self.calc_FROG(pulsebeam)
        extent = pulsebeam.FROGxmin+k*pulsebeam.FROGdeltax, pulsebeam.FROGxmin+l*pulsebeam.FROGdeltax, \
                     pulsebeam.FROGymin+i*pulsebeam.FROGdeltay, pulsebeam.FROGymin+j*pulsebeam.FROGdeltay
        self.FROG_plot = self.FROG_subplot.imshow(pulsebeam.FROG[i:j,k:l], interpolation='bicubic',extent=extent,aspect="auto")
        self.FROG_annotation = self.FROG_subplot.annotate('400nm', xy=(pulsebeam.FROGxmin,3e8/400e-9),  xycoords='data', \
                xytext=(-20, -15), textcoords='offset points', \
                arrowprops=dict(facecolor='black', arrowstyle="->"),\
                horizontalalignment='center', verticalalignment='center')
        self.FROG_subplot.set_title('SHG FROG')
        
    def update_FROG(self,pulsebeam):
        i,j,k,l = self.calc_FROG(pulsebeam)
        extent = pulsebeam.FROGxmin+k*pulsebeam.FROGdeltax, pulsebeam.FROGxmin+l*pulsebeam.FROGdeltax, \
                     pulsebeam.FROGymin+i*pulsebeam.FROGdeltay, pulsebeam.FROGymin+j*pulsebeam.FROGdeltay
        self.FROG_plot.set_data(pulsebeam.FROG[i:j,k:l])
        self.FROG_figure.canvas.draw()
        
    def calc_pulseSpot(self,pulsebeam):
        if(pulsebeam.BeamProfile_spot >= 1e-3):
            text1 = 'spot = %3.3f mm'%(pulsebeam.BeamProfile_spot*1e3)
        else:
            text1 = 'spot = %3.3f um'%(pulsebeam.BeamProfile_spot*1e6)
        text2 = 'curvature = %1.2e m'%(pulsebeam.BeamProfile_curvature)
        
        x = arange(-0.015,0.015,0.000005)
        return x, exp(-x**2/pulsebeam.BeamProfile_spot**2),text1,text2
        
      
    def draw_pulseSpot(self,pulsebeam):
        x,y,text1,text2 = self.calc_pulseSpot(pulsebeam)
        self.beam_subplot.set_title('Gaussian Beam')
        self.beam_plot, = self.beam_subplot.plot(y,x)
        self.beam_subplot.set_xlim((-0.25,4))
        self.beam_subplot.set_ylim((x[0]*1.5,x[-1]*1.5))
        
        self.beam_annotation_1 = self.beam_subplot.annotate(text1, xy=(0.4, 0.60),  xycoords='figure fraction', \
                              horizontalalignment='left', verticalalignment='center',size=14)
        self.beam_annotation_2 = self.beam_subplot.annotate(text2, xy=(0.4, 0.40),  xycoords='figure fraction', \
                              horizontalalignment='left', verticalalignment='center',size=14)
        
    
    
    def update_pulseSpot(self,pulsebeam):
        x,y,text1,text2 = self.calc_pulseSpot(pulsebeam)
        self.beam_plot.set_data(y,x)
        self.beam_annotation_1.set_text(text1)
        self.beam_annotation_2.set_text(text2)
        self.beam_figure.canvas.draw()
        
    def calc_statistics(self,pulsebeam):
        text1 = 'peak power = %3.3e W'%(pulsebeam.calc_peak_power())
        text2 = 'peak intensity = %3.3e Wm^-2'%(pulsebeam.calc_peak_intensity())
        energy = pulsebeam.calc_energy()
        if(energy > 0.5):
            text3 = 'energy = %3.3f J'%(energy)
        elif(energy > 0.5e-3):
            text3 = 'energy = %3.3f mJ'%(energy*1000)
        elif(energy > 0.5e-6):
            text3 = 'energy = %3.3f uJ'%(energy*1e6)
        else:
            text3 = 'energy = %3.3e J'%(energy)
        if(pulsebeam.rate > 0.9e6):
            text4 = 'rate = %3.1f MHz'%(pulsebeam.rate/1e6)
        elif(pulsebeam.rate > 0.9e3):
            text4 = 'rate = %3.1f kHz'%(pulsebeam.rate/1e3)
        else:
            text4 = 'rate = %3.3f Hz'%(pulsebeam.rate)
        text5 = 'CW power = %3.3f W'%(pulsebeam.calc_CW_power())
    
        return text1,text2,text3,text4,text5
        
    def draw_statistics(self,pulsebeam):
        self.statistics_subplot.set_title('Pulse Statistics')
        text1,text2,text3,text4,text5 = self.calc_statistics(pulsebeam)
        self.statistics_annotation_1 = self.statistics_subplot.annotate(text1, xy=(0.2, 0.80),  xycoords='figure fraction', \
                              horizontalalignment='left', verticalalignment='center',size=14)
        self.statistics_annotation_2 = self.statistics_subplot.annotate(text2, xy=(0.2, 0.65),  xycoords='figure fraction', \
                              horizontalalignment='left', verticalalignment='center',size=14)
        self.statistics_annotation_3 = self.statistics_subplot.annotate(text3, xy=(0.2, 0.50),  xycoords='figure fraction', \
                              horizontalalignment='left', verticalalignment='center',size=14)
        self.statistics_annotation_4 = self.statistics_subplot.annotate(text4, xy=(0.2, 0.35),  xycoords='figure fraction', \
                              horizontalalignment='left', verticalalignment='center',size=14)
        self.statistics_annotation_5 = self.statistics_subplot.annotate(text5, xy=(0.2, 0.20),  xycoords='figure fraction', \
                              horizontalalignment='left', verticalalignment='center',size=14)
       
        
    def update_statistics(self,pulsebeam):
        text1,text2,text3,text4,text5 = self.calc_statistics(pulsebeam)
        self.statistics_annotation_1.set_text(text1)
        self.statistics_annotation_2.set_text(text2)
        self.statistics_annotation_3.set_text(text3)
        self.statistics_annotation_4.set_text(text4)
        self.statistics_annotation_5.set_text(text5)
        
        self.statistics_figure.canvas.draw()
        
        
        
        
        
    def draw_pulseBeam(self,pulsebeam):
        self.draw_pulse(pulsebeam)       
        self.draw_spectrum(pulsebeam)
        self.draw_pulseSpot(pulsebeam)
        self.draw_autoco(pulsebeam)
        self.draw_FROG(pulsebeam)
        self.draw_statistics(pulsebeam)
        
        
        
                
                
    def update_pulseBeam(self,pulsebeam):
        self.update_pulse(pulsebeam)
        self.update_spectrum(pulsebeam)
        self.update_pulseSpot(pulsebeam)  
        self.update_autoco(pulsebeam)
        self.update_FROG(pulsebeam) 
        self.update_statistics(pulsebeam)
        
    def save_electric_field_png(self,filename,dpi):
        self.pulse_figure.savefig(filename,dpi=dpi)
        
    def save_spectrum_png(self,filename,dpi):
        self.spectrum_figure.savefig(filename,dpi=dpi)
        
    def save_autoco_png(self,filename,dpi):
        self.autoco_figure.savefig(filename,dpi=dpi)
        
    def save_FROG_png(self,filename,dpi):
        self.FROG_figure.savefig(filename,dpi=dpi)
        
             

