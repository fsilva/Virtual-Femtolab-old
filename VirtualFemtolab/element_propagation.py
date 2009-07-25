
import gtk
from numpy import *

import element_class
import pulseBeam


# name, GVD,TOD,QOD
materials = [ ['Glass - Fused Silica',1.45332,36160e-30,27495e-45,0],
              ['Glass - BK7',1.51078,44650e-30,32099e-45,0],
              ['Air - 1 bar',1.0,20.4e-30,10.896e-45,0],
              ['Vacuum',1.0,0,0,0]]

class Element_Propagation(element_class.Element):
    def __init__(self,length,material,lambdaZero):
        self.length = length
        self.material = material[:]
        self.lambdaZero = lambdaZero
        self.name = material[0]
        self.n = material[1]
        
    def is_discrete(self):
        #discrete elements can only return calculations after the whole length
        return False 
        
    def calc_pulseBeam(self,z,input_beam):
        #calculate pulseBeam after propagation through z 
        if(z < 0 or (abs(z-self.length) > 1e-10 and z > self.length)): #i.e. z > self.length
            print 'Error with z - outside of length - z=',z
            raise Exception, 'Error with z - outside of length - z=%e'%z
        if(self.is_discrete() and z < self.length):
            return input_beam
        
        #1) material propagation is in the spectral domain
        input_beam.field_to_spectrum()
        
       
        #2) apply propagation
        input_beam.apply_dispersion(z*self.material[2],z*self.material[3],z*self.material[4],0)
                
        #3) recalculate time domain
        input_beam.spectrum_to_field()

        
    def open_edit_dialog(self,refresh_callback):
        self.refresh_callback = refresh_callback
        
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)

        self.window.set_title("Material Propagation")

        self.Vbox = gtk.VBox(False,0)

        self.Hbox0 = gtk.HBox(False,0)
        self.type_label = gtk.Label('Material')
        self.type_combo = gtk.combo_box_new_text()
        for mat in materials:
            self.type_combo.append_text(mat[0])
        self.type_combo.connect('changed',self.changed)
        self.Hbox0.pack_start(self.type_label)
        self.Hbox0.pack_end(self.type_combo)
        self.Vbox.pack_start(self.Hbox0)
               
        self.Hbox1 = gtk.HBox(False,0)
        self.label1 = gtk.Label('Name')
        self.edit1 = gtk.Entry(max=20)
        self.edit1.set_text(self.name)
        self.Hbox1.pack_start(self.label1)
        self.Hbox1.pack_end(self.edit1)
        
        self.Hbox2_1 = gtk.HBox(False,0)
        self.label2_1 = gtk.Label('n')
        self.adj2_1 = gtk.Adjustment(value=self.material[1], lower=0, upper=1e6, step_incr=0.1)
        self.adj2_1.connect('value_changed',self.refresh)
        self.spin2_1 = gtk.SpinButton(adjustment=self.adj2_1,digits=6)
        self.Hbox2_1.pack_start(self.label2_1)
        self.Hbox2_1.pack_end(self.spin2_1)
     
        self.Hbox2 = gtk.HBox(False,0)
        self.label2 = gtk.Label('GVD(fs^2)')
        self.adj2 = gtk.Adjustment(value=self.material[2]/1e-30, lower=-1e6, upper=1e6, step_incr=0.1)
        self.adj2.connect('value_changed',self.refresh)
        self.spin2 = gtk.SpinButton(adjustment=self.adj2,digits=6)
        self.Hbox2.pack_start(self.label2)
        self.Hbox2.pack_end(self.spin2)
        
        self.Hbox3 = gtk.HBox(False,0)
        self.label3 = gtk.Label('TOD(fs^3)')
        self.adj3 = gtk.Adjustment(value=self.material[3]/1e-45, lower=-1e6, upper=1e6, step_incr=0.1)
        self.adj3.connect('value_changed',self.refresh)
        self.spin3 = gtk.SpinButton(adjustment=self.adj3,digits=6)
        self.Hbox3.pack_start(self.label3)
        self.Hbox3.pack_end(self.spin3)
        
        self.Hbox4 = gtk.HBox(False,0)
        self.label4 = gtk.Label('QOD(fs^4)')
        self.adj4 = gtk.Adjustment(value=self.material[4]/1e-60, lower=-1e6, upper=1e6, step_incr=0.1)
        self.adj4.connect('value_changed',self.refresh)
        self.spin4 = gtk.SpinButton(adjustment=self.adj4,digits=6)
        self.Hbox4.pack_start(self.label4)
        self.Hbox4.pack_end(self.spin4)
        
        self.Hbox5 = gtk.HBox(False,0)
        self.label5 = gtk.Label('Length(m)')
        self.adj5 = gtk.Adjustment(value=self.length, lower=-1e6, upper=1e6, step_incr=1)
        self.adj5.connect('value_changed',self.refresh)
        self.spin5 = gtk.SpinButton(adjustment=self.adj5,digits=6)
        self.Hbox5.pack_start(self.label5)
        self.Hbox5.pack_end(self.spin5)
               
        self.Vbox.pack_start(self.Hbox1)
        self.Vbox.pack_start(self.Hbox2_1)
        self.Vbox.pack_start(self.Hbox2)
        self.Vbox.pack_start(self.Hbox3)
        self.Vbox.pack_start(self.Hbox4)
        self.Vbox.pack_start(self.Hbox5)
        
        self.button = gtk.Button('Ok')
        self.button.connect('clicked',self.ok)
        
        self.Vbox.pack_start(self.button)
        
        self.window.add(self.Vbox)
        self.window.show_all()

    def changed(self,widget):
        n = self.type_combo.get_active()
        self.name = materials[n][0]
        self.edit1.set_text(self.name)
        self.material[0] = materials[n][0]
        self.adj2_1.set_value(materials[n][1])
        self.material[1] = materials[n][1]
        self.adj2.set_value(materials[n][2]/1e-30)
        self.material[2] = materials[n][2]
        self.adj3.set_value(materials[n][3]/1e-45)
        self.material[3] = materials[n][3]
        self.adj4.set_value(materials[n][4]/1e-60)        
        self.material[4] = materials[n][4]

        
    def refresh(self,widget):
        try:
            self.adj2
            self.adj3
            self.adj4
            self.adj5
        except:
            return

        self.name = self.material[0] = self.edit1.get_text()
        self.material[1] = self.adj2_1.value
        self.material[2] = self.adj2.value*1e-30
        self.material[3] = self.adj3.value*1e-45
        self.material[4] = self.adj4.value*1e-60
        self.length = self.adj5.value
        self.refresh_callback()

        
    def ok(self,widget):
        self.refresh(widget)
        self.window.destroy()
        
    def close_window(self,widget):
        self.window.destroy()
 
