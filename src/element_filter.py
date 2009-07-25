
import gtk
from numpy import *

import element_class
import pulseBeam


class Element_Filter(element_class.Element):
    def __init__(self,wavelength1,wavelength2):
        self.length = 0
        self.wavelength1 = wavelength1
        self.wavelength2 = wavelength2
        self.name = 'Spectral Filter' 
        self.n = 0

    def is_discrete(self):
        #discrete elements can only return calculations after the whole length
        return True
        
    def calc_pulseBeam(self,z,input_beam):
        #calculate pulseBeam after propagation through z 
        if(z < 0 or z > self.length):
            print 'Error with z - outside of length - z=',z
            raise Exception, 'Error with z - outside of length - z=%e'%z
        if(self.is_discrete() and z < self.length):
            return input_beam
        
        #1) material propagation is in the spectral domain
        input_beam.field_to_spectrum()
        
        #2) apply filter
        input_beam.apply_spectral_filter(self.wavelength1,self.wavelength2,0)
                
        #3) recalculate time domain
        input_beam.spectrum_to_field()

        
    def open_edit_dialog(self,refresh_callback):
        self.refresh_callback = refresh_callback
        
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)

        self.window.set_title("Bandstop Spectral Filter")

        self.Vbox = gtk.VBox(False,0) 
               
        self.Hbox2 = gtk.HBox(False,0)
        self.label2 = gtk.Label('Low Cutoff(nm)')
        self.adj2 = gtk.Adjustment(value=self.wavelength1/1e-9, lower=0.001, upper=100000, step_incr=0.1)
        self.adj2.connect('value_changed',self.refresh)
        self.spin2 = gtk.SpinButton(adjustment=self.adj2,digits=6)
        self.Hbox2.pack_start(self.label2)
        self.Hbox2.pack_end(self.spin2)
        
        self.Hbox3 = gtk.HBox(False,0)
        self.label3 = gtk.Label('High Cutoff(nm)')
        self.adj3 = gtk.Adjustment(value=self.wavelength2/1e-9, lower=0.001, upper=100000, step_incr=0.1)
        self.adj3.connect('value_changed',self.refresh)
        self.spin3 = gtk.SpinButton(adjustment=self.adj3,digits=6)
        self.Hbox3.pack_start(self.label3)
        self.Hbox3.pack_end(self.spin3)
               
        self.Vbox.pack_start(self.Hbox2)
        self.Vbox.pack_start(self.Hbox3)
        
        self.button = gtk.Button('Ok')
        self.button.connect('clicked',self.ok)
        
        self.Vbox.pack_start(self.button)
        
        self.window.add(self.Vbox)
        self.window.show_all()
        
    def refresh(self,widget):
        try:
            self.adj2
            self.adj3
        except:
            return

        self.wavelength1 = self.adj2.value*1e-9
        self.wavelength2 = self.adj3.value*1e-9
        self.refresh_callback()

        
    def ok(self,widget):
        self.refresh(widget)
        self.window.destroy()
        
    def close_window(self,widget):
        self.window.destroy()
 
