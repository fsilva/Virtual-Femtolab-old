
import gtk
from matplotlib.figure import Figure
from numpy import *
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

import config
import pulseBeam
import spectrum_loader


class InitialPulse_Dialog:

    def __init__(self,initialPulseBeam,refresh_callback,config):
        self.pulseBeam = initialPulseBeam
        self.refresh_callback = refresh_callback
        self.NT = config.NT
        self.lambdaZero = config.lambdaZero
        
        #create window
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)
        #self.window.set_default_size(600,400)
        self.window.set_default_size(600,100)
        self.window.set_title("Initial Pulse Parameters")
        
        self.Vbox = gtk.VBox(False, 0)
        
        #add 2 plots, E and spectra
        #self.figure  = Figure(figsize=(8,6), dpi=66,facecolor='w')
        #self.E_subplot       = self.figure.add_subplot(121)
        #self.spectrum_subplot_1 = self.figure.add_subplot(122)
        #self.canvas = FigureCanvas(self.figure) 
        
        #draw E
        envelope = abs(initialPulseBeam.ElectricField)
        #self.E_plot1 = self.E_subplot.plot(initialPulseBeam.t,initialPulseBeam.ElectricField.real,'b')
        #self.E_plot2 = self.E_subplot.plot(initialPulseBeam.t,envelope,'r')
        #self.E_subplot.set_title('Electric Field')

        #draw Spectrum
        #absSpectrum = abs(initialPulseBeam.Spectrum)
        #self.spectrum_plot1 = self.spectrum_subplot_1.plot(initialPulseBeam.frequencies,absSpectrum,'g')
        #self.spectrum_subplot_2 = self.spectrum_subplot_1.twinx()
        #self.spectrum_plot2 = self.spectrum_subplot_2.plot(initialPulseBeam.frequencies,unwrap(angle(initialPulseBeam.Spectrum)),'k')
        #self.spectrum_subplot_1.set_title('Spectrum')
        
        #self.Vbox.pack_start(self.canvas,True,True)
        
        
        
        #add 2 frames side by side
        self.Hbox = gtk.HBox(False, 0)
        
        #add pulse shape frame with controls
        self.shape_frame = gtk.Frame(label='Pulse Shape')
        self.shape_radio_1 = gtk.RadioButton(group=None              , label='Temporal FWHM(fs)')
        self.shape_radio_1.connect('toggled',self.value_changed)
        self.shape_radio_2 = gtk.RadioButton(group=self.shape_radio_1, label='Spectral FWHM(nm)')
        self.shape_radio_2.connect('toggled',self.value_changed)
        self.shape_radio_3 = gtk.RadioButton(group=self.shape_radio_1, label='Load Spectrum')
        #self.shape_radio_3.connect('toggled',self.load_spectrum)
        self.shape_radio_3.connect('clicked',self.load_spectrum)
        self.shape_t_adj = gtk.Adjustment(value=6.6, lower=1, upper=100, step_incr=0.1)
        self.shape_t_adj.connect('value_changed',self.value_changed)
        self.shape_spin_1 = gtk.SpinButton(adjustment=self.shape_t_adj,digits=6)
        self.shape_lambda_adj = gtk.Adjustment(value=400, lower=1, upper=2000, step_incr=0.1)
        self.shape_lambda_adj.connect('value_changed',self.value_changed)
        self.shape_spin_2 = gtk.SpinButton(adjustment=self.shape_lambda_adj,digits=6)
        
        self.shapeVbox  = gtk.VBox(False, 0)
        self.shapeHbox1 = gtk.HBox(False, 0)
        self.shapeHbox1.pack_start(self.shape_radio_1,False,False)
        self.shapeHbox1.pack_end(self.shape_spin_1,False,False)
        self.shapeHbox2 = gtk.HBox(False, 0)
        self.shapeHbox2.pack_start(self.shape_radio_2,False,False)
        self.shapeHbox2.pack_end(self.shape_spin_2,False,False)
        self.shapeVbox.pack_start(self.shapeHbox1,True,False)
        self.shapeVbox.pack_start(self.shapeHbox2,True,False)
        self.shapeVbox.pack_start(self.shape_radio_3,True,False)
        self.shape_frame.add(self.shapeVbox)
        
        self.Hbox.pack_start(self.shape_frame)
        
        #add frame with GVD, TOD, QOD, FOD
        self.phase_frame = gtk.Frame(label='Spectral Phase')
        self.phaseVbox  = gtk.VBox(False, 0)
        
        self.phase_label_GVD = gtk.Label('GVD(fs^2)')
        self.phase_GVD_adj = gtk.Adjustment(value=0, lower=-1e15, upper=1e15, step_incr=0.1)
        self.phase_GVD_adj.connect('value_changed',self.value_changed)
        self.phase_spin_GVD = gtk.SpinButton(adjustment=self.phase_GVD_adj,digits=6)
        self.phaseHbox1 = gtk.HBox(False, 0)
        self.phaseHbox1.pack_start(self.phase_label_GVD,False,False)
        self.phaseHbox1.pack_end(self.phase_spin_GVD,False,False)
        self.phaseVbox.pack_start(self.phaseHbox1,True,False)
        
        self.phase_label_TOD = gtk.Label('TOD(fs^3)')
        self.phase_TOD_adj = gtk.Adjustment(value=0, lower=-1e15, upper=1e15, step_incr=0.1)
        self.phase_TOD_adj.connect('value_changed',self.value_changed)
        self.phase_spin_TOD = gtk.SpinButton(adjustment=self.phase_TOD_adj,digits=6)
        self.phaseHbox2 = gtk.HBox(False, 0)
        self.phaseHbox2.pack_start(self.phase_label_TOD,False,False)
        self.phaseHbox2.pack_end(self.phase_spin_TOD,False,False)
        self.phaseVbox.pack_start(self.phaseHbox2,True,False)
        
        self.phase_label_QOD = gtk.Label('QOD(fs^4)')
        self.phase_QOD_adj = gtk.Adjustment(value=0, lower=-1e15, upper=1e15, step_incr=0.1)
        self.phase_QOD_adj.connect('value_changed',self.value_changed)
        self.phase_spin_QOD = gtk.SpinButton(adjustment=self.phase_QOD_adj,digits=6)
        self.phaseHbox3 = gtk.HBox(False, 0)
        self.phaseHbox3.pack_start(self.phase_label_QOD,False,False)
        self.phaseHbox3.pack_end(self.phase_spin_QOD,False,False)
        self.phaseVbox.pack_start(self.phaseHbox3,True,False)
        
        self.phase_label_FOD = gtk.Label('FOD(fs^5)')
        self.phase_FOD_adj = gtk.Adjustment(value=0, lower=-1e15, upper=1e15, step_incr=0.1)
        self.phase_FOD_adj.connect('value_changed',self.value_changed)
        self.phase_spin_FOD = gtk.SpinButton(adjustment=self.phase_FOD_adj,digits=6)
        self.phaseHbox4 = gtk.HBox(False, 0)
        self.phaseHbox4.pack_start(self.phase_label_FOD,False,False)
        self.phaseHbox4.pack_end(self.phase_spin_FOD,False,False)
        self.phaseVbox.pack_start(self.phaseHbox4,True,False)
        
        self.phase_frame.add(self.phaseVbox)
        
        
        self.Hbox.pack_start(self.phase_frame,False,False)
        
        
        
        #add beam frame with controls
        
        self.beam_frame = gtk.Frame(label='Beam Shape')
        self.beam_label_1 = gtk.Label('Spot(mm)')
        self.beam_label_2 = gtk.Label('Curvature(m)')
        self.beam_spot_adj = gtk.Adjustment(value=self.pulseBeam.BeamProfile_spot, lower=1e-6, upper=100, step_incr=0.1)
        self.beam_spot_adj.connect('value_changed',self.value_changed)
        self.beam_spin_1 = gtk.SpinButton(adjustment=self.beam_spot_adj,digits=6)
        self.beam_curvature_adj = gtk.Adjustment(value=self.pulseBeam.BeamProfile_curvature, lower=-1e8, upper=1e8, step_incr=0.1)
        self.beam_curvature_adj.connect('value_changed',self.value_changed)
        self.beam_spin_2 = gtk.SpinButton(adjustment=self.beam_curvature_adj,digits=6)
        
        self.beamVbox  = gtk.VBox(False, 0)
        self.beamHbox1 = gtk.HBox(False, 0)
        self.beamHbox1.pack_start(self.beam_label_1,False,False)
        self.beamHbox1.pack_end(self.beam_spin_1,False,False)
        self.beamHbox2 = gtk.HBox(False, 0)
        self.beamHbox2.pack_start(self.beam_label_2,False,False)
        self.beamHbox2.pack_end(self.beam_spin_2,False,False)
        self.beamVbox.pack_start(self.beamHbox1,True,False)
        self.beamVbox.pack_start(self.beamHbox2,True,False)
        self.beam_frame.add(self.beamVbox)

        self.Hbox.pack_start(self.beam_frame)
        
        
        #add energy/power frame with controls
        
        self.amp_frame = gtk.Frame(label='Amplitude')
        self.amp_radio_1 = gtk.RadioButton(group=None              , label='Energy (mJ)')
        self.amp_radio_1.connect('toggled',self.value_changed)
        self.amp_label   = gtk.Label('Rate (KHz)')
        self.amp_radio_2 = gtk.RadioButton(group=self.amp_radio_1, label='Peak Power (MW)')
        self.amp_radio_2.connect('toggled',self.value_changed)
        self.amp_energy_adj = gtk.Adjustment(value=self.pulseBeam.energy, lower=1e-15, upper=100, step_incr=0.1)
        self.amp_energy_adj.connect('value_changed',self.value_changed)
        self.amp_spin_1     = gtk.SpinButton(adjustment=self.amp_energy_adj,digits=6)
        self.amp_rate_adj   = gtk.Adjustment(value=self.pulseBeam.rate, lower=0, upper=1e15, step_incr=1)
        self.amp_rate_adj.connect('value_changed',self.value_changed)
        self.amp_spin_2     = gtk.SpinButton(adjustment=self.amp_rate_adj,digits=6)
        self.amp_power_adj  = gtk.Adjustment(value=self.pulseBeam.peak_power, lower=1e-15, upper=1e8, step_incr=0.1)
        self.amp_power_adj.connect('value_changed',self.value_changed)
        self.amp_spin_3     = gtk.SpinButton(adjustment=self.amp_power_adj,digits=6)
        
        self.ampVbox  = gtk.VBox(False, 0)
        self.ampHbox1 = gtk.HBox(False, 0)
        self.ampHbox1.pack_start(self.amp_radio_1,True,False)
        self.ampHbox1.pack_end(self.amp_spin_1,True,False)
        self.ampHbox2 = gtk.HBox(False, 0)
        self.ampHbox2.pack_start(self.amp_label,True,False)
        self.ampHbox2.pack_end(self.amp_spin_2,True,False)
        self.ampHbox3 = gtk.HBox(False, 0)
        self.ampHbox3.pack_start(self.amp_radio_2,True,False)
        self.ampHbox3.pack_end(self.amp_spin_3,True,False)
        self.ampVbox.pack_start(self.ampHbox1,True,False)
        self.ampVbox.pack_start(self.ampHbox2,True,False)
        self.ampVbox.pack_start(self.ampHbox3,True,False)
        self.amp_frame.add(self.ampVbox)
        
        self.Hbox.pack_end(self.amp_frame,False,False)
        
        
        #add everything to window and show
        self.window.add(self.Hbox)
        self.window.show_all()
        
    def refresh(self):
        try: #test if these variables exist. TODO:fix the problem?
            self.beam_curvature_adj.value 
            self.beam_spot_adj.value 
            self.amp_radio_1
            self.amp_rate_adj.value
        except:
            return
            
        if(self.shape_radio_3.get_active() == 1): #load spectra selected
            self.change_loaded_spectrum()
            return    
            
            
        if(self.amp_radio_1.get_active() == 0): #peak power is selected
            power  = self.amp_power_adj.value*1e6
            energy = 0
        else:                                   #energy is selected
            energy = self.amp_energy_adj.value*1e-3
            power = 0
            
        
        if(self.shape_radio_1.get_active() == 1): #temporal selected
            self.pulseBeam.initialize_pulse(self.shape_t_adj.value*1e-15,  \
                                            self.phase_GVD_adj.value*1e-30,\
                                            self.phase_TOD_adj.value*1e-45,\
                                            self.phase_QOD_adj.value*1e-60,\
                                            self.phase_FOD_adj.value*1e-75,\
                                            self.beam_spot_adj.value*0.001,\
                                            self.beam_curvature_adj.value, \
                                            power,energy,self.amp_rate_adj.value*1e3)
        if(self.shape_radio_2.get_active() == 1): #spectrum selected
            deltaOmega = 3e8/self.lambdaZero**2*self.shape_lambda_adj.value*1e-9/2
            self.pulseBeam.initialize_spectrum(deltaOmega,   \
                                               self.phase_GVD_adj.value*1e-30,\
                                               self.phase_TOD_adj.value*1e-45,\
                                               self.phase_QOD_adj.value*1e-60,\
                                               self.phase_FOD_adj.value*1e-75,\
                                               self.beam_spot_adj.value*0.001,\
                                               self.beam_curvature_adj.value, \
                                               power,energy,self.amp_rate_adj.value*1e3)
                                               
        self.refresh_callback()  
                                               
    def load_spectrum(self,widget):
        try: #test if these variables exist. TODO:fix the problem?
            self.beam_curvature_adj.value is None
            self.beam_spot_adj.value is None
            self.amp_rate_adj
        except:
            return
            
        #test if it was selected or deselected
        if(widget.get_active() == 0):
            return
        
        #open dialog box to get spectrum filename 
        
        filesel = gtk.FileChooserDialog(title='Select csv file to load as spectrum',action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        filesel.set_filename( 'data/RainbowSpectrum.csv')
        response = filesel.run()
        
        if response == gtk.RESPONSE_OK:
            filename = filesel.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected, not loading spectrum'
            filesel.destroy()
            return
        filesel.destroy()

        self.loader = spectrum_loader.Spectrum_loader(filename)

       #open dialog box to get phase filename 
        
        filesel = gtk.FileChooserDialog(title='Select csv file to load as spectral phase, in radians. Cancel for flat phase.',action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                   buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        response = filesel.run()
        
        if response == gtk.RESPONSE_OK:
            phasefilename = filesel.get_filename()
            self.phaseloader = spectrum_loader.Spectrum_loader(phasefilename)
        elif response == gtk.RESPONSE_CANCEL:
            self.phaseloader = None
        filesel.destroy()
            
        
        if(self.amp_radio_1.get_active() == 0): #peak power is selected
            power  = self.amp_power_adj.value*1e6
            energy = 0
        else:                                   #energy is selected
            energy = self.amp_energy_adj.value*1e-3
            power = 0

        self.pulseBeam.initialize_spectrum_loaded(self.loader,self.phaseloader,\
                                               self.phase_GVD_adj.value*1e-30,\
                                               self.phase_TOD_adj.value*1e-45,\
                                               self.phase_QOD_adj.value*1e-60,\
                                               self.phase_FOD_adj.value*1e-75,\
                                               self.beam_spot_adj.value*0.001, \
                                               self.beam_curvature_adj.value,power,energy,self.amp_rate_adj.value*1e3)
        

        self.refresh_callback()
        
    def change_loaded_spectrum(self):
        try: 
            self.loader
        except:
            return
        
        if(self.amp_radio_1.get_active() == 0): #peak power is selected
            power  = self.amp_power_adj.value*1e6
            energy = 0
        else:                                   #energy is selected
            energy = self.amp_energy_adj.value*1e-3
            power = 0
            
        self.pulseBeam.initialize_spectrum_loaded(self.loader,self.phaseloader,\
                                               self.phase_GVD_adj.value*1e-30,\
                                               self.phase_TOD_adj.value*1e-45,\
                                               self.phase_QOD_adj.value*1e-60,\
                                               self.phase_FOD_adj.value*1e-75,\
                                               self.beam_spot_adj.value*0.001, \
                                                self.beam_curvature_adj.value,power,energy,self.amp_rate_adj.value*1e3)
        self.refresh_callback()

        
    def value_changed(self,widget):
        self.refresh()
    
    def close_window(self,widget):
        del self
        #print 'erro isto nao esta bem feito, podem haver varias janelas abertas'
        
       
          
