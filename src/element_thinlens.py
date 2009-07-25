
from numpy import *

import gtk

import pulseBeam

class Element_ThinLens:
    def __init__(self,f,lambdaZero):
        self.f = f
        self.name = 'Thin Lens'
        self.n = 0 #0 means this element calculates the refraction
        self.length = 0
        self.lambdaZero = lambdaZero

        
    def is_discrete(self):
        #discrete elements can only return calculations after the whole length
        return True
        
    def calc_pulseBeam(self,z,input_beam):
        #calculate pulseBeam after propagation through z 
        if(z < 0 or z > self.length):
            print 'Error with z - outside of length'
            raise
        if(self.is_discrete() and z < self.length):
            return input_beam
            
        input_beam.beam_apply_thinlens(self.f)
            
        return input_beam
        
        
    def open_edit_dialog(self,refresh_callback):
        self.refresh_callback = refresh_callback
        
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)

        self.window.set_title("Thin Lens")

        self.Vbox = gtk.VBox(False,0)        
        self.Hbox = gtk.HBox(False,0)
        
        self.label1 = gtk.Label('Focus(m)')
        self.adjustment = gtk.Adjustment(value=self.f, lower=1e-6, upper=1e10, step_incr=0.1)
        self.adjustment.connect('value_changed',self.refresh)
        self.spin1 = gtk.SpinButton(adjustment=self.adjustment,digits=6)
        
        self.Hbox.pack_start(self.label1)
        self.Hbox.pack_end(self.spin1)
        
        self.Vbox.pack_start(self.Hbox)
        
        self.button = gtk.Button('Ok')
        self.button.connect('clicked',self.ok)
        
        self.Vbox.pack_start(self.button)
        
        self.window.add(self.Vbox)
        self.window.show_all()
        
    def refresh(self,widget):
        self.f = self.adjustment.value
        self.refresh_callback()
        
        
    def ok(self,widget):
        self.f = self.adjustment.value
        self.window.destroy()
        
    def close_window(self,widget):
        self.window.destroy()
        
