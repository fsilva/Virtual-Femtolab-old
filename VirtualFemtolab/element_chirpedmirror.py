
import gtk
from numpy import *

import element_class
import pulseBeam

# name,GVD,TOD,QOD
mirrors = [ ['DCM1000',-36160e-30*1e-3,-27495e-45*1e-3,0],
            ['DCM1001',-44650e-30*1e-3,-32099e-45*1e-3,0]] #1e-3 to mean 1 mm of glass

class Element_ChirpedMirror(element_class.Element):
    def __init__(self,mirror,num_bounces,lambdaZero):
        self.mirror = mirror
        self.lambdaZero = lambdaZero
        self.name = mirror[0]
        self.n = 0
        self.length = 0
        self.num_bounces = num_bounces
        
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
        
        
        #2) apply propagation
        input_beam.apply_dispersion(self.mirror[1]*self.num_bounces,self.mirror[2]*self.num_bounces,self.mirror[3]*self.num_bounces,0)
                
        #3) recalculate time domain
        input_beam.spectrum_to_field()

        
    def open_edit_dialog(self,refresh_callback):
        self.refresh_callback = refresh_callback
        
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)

        self.window.set_title("Chirped Mirror")

        self.Vbox = gtk.VBox(False,0) 
               
        self.Hbox1 = gtk.HBox(False,0)
        self.label1 = gtk.Label('Name')
        self.edit1 = gtk.Entry(max=10)
        self.edit1.set_text(self.mirror[0])
        self.Hbox1.pack_start(self.label1)
        self.Hbox1.pack_end(self.edit1)
     
        self.Hbox2 = gtk.HBox(False,0)
        self.label2 = gtk.Label('GVD(fs^2)')
        self.adj2 = gtk.Adjustment(value=self.mirror[1]/1e-30, lower=-1e6, upper=1e6, step_incr=0.1)
        self.adj2.connect('value_changed',self.refresh)
        self.spin2 = gtk.SpinButton(adjustment=self.adj2,digits=6)
        self.Hbox2.pack_start(self.label2)
        self.Hbox2.pack_end(self.spin2)
        
        self.Hbox3 = gtk.HBox(False,0)
        self.label3 = gtk.Label('TOD(fs^3)')
        self.adj3 = gtk.Adjustment(value=self.mirror[2]/1e-45, lower=-1e6, upper=1e6, step_incr=0.1)
        self.adj3.connect('value_changed',self.refresh)
        self.spin3 = gtk.SpinButton(adjustment=self.adj3,digits=6)
        self.Hbox3.pack_start(self.label3)
        self.Hbox3.pack_end(self.spin3)
        
        self.Hbox4 = gtk.HBox(False,0)
        self.label4 = gtk.Label('QOD(fs^4)')
        self.adj4 = gtk.Adjustment(value=self.mirror[3]/1e-60, lower=-1e6, upper=1e6, step_incr=0.1)
        self.adj4.connect('value_changed',self.refresh)
        self.spin4 = gtk.SpinButton(adjustment=self.adj4,digits=6)
        self.Hbox4.pack_start(self.label4)
        self.Hbox4.pack_end(self.spin4)
        
        self.Hbox5 = gtk.HBox(False,0)
        self.label5 = gtk.Label('Bounces')
        self.adj5 = gtk.Adjustment(value=self.num_bounces, lower=-1e6, upper=1e6, step_incr=1)
        self.adj5.connect('value_changed',self.refresh)
        self.spin5 = gtk.SpinButton(adjustment=self.adj5,digits=6)
        self.Hbox5.pack_start(self.label5)
        self.Hbox5.pack_end(self.spin5)
               
        self.Vbox.pack_start(self.Hbox1)
        self.Vbox.pack_start(self.Hbox2)
        self.Vbox.pack_start(self.Hbox3)
        self.Vbox.pack_start(self.Hbox4)
        self.Vbox.pack_start(self.Hbox5)
        
        self.button = gtk.Button('Ok')
        self.button.connect('clicked',self.ok)
        
        self.Vbox.pack_start(self.button)
        
        self.window.add(self.Vbox)
        self.window.show_all()
        
    def refresh(self,widget):
        try:
            self.adj2
            self.adj3
            self.adj4
            self.adj5
        except:
            return

        self.name = self.mirror[0] = self.edit1.get_text()
        self.mirror[1] = self.adj2.value*1e-30
        self.mirror[2] = self.adj3.value*1e-45
        self.mirror[3] = self.adj4.value*1e-60
        self.num_bounces = int(self.adj5.value)
        self.refresh_callback()

        
        
    def ok(self,widget):
        self.refresh(widget)
        self.window.destroy()
        
    def close_window(self,widget):
        self.window.destroy()
        
 
