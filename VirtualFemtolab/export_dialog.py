
import gtk

import config


class Export_Dialog:

    def __init__(self,callback):
    
        self.callback = callback
                    
        #create window
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)

        self.window.set_title("Export")
        
        self.Vbox = gtk.VBox(False,0)
        self.Hbox = gtk.HBox(False, 0)
        
        self.radio_1 = gtk.RadioButton(group=None, label='Figure')
        self.radio_2 = gtk.RadioButton(group=self.radio_1, label='Sequence')
        self.label1 = gtk.Label('Number of Frames')
        self.adjustment = gtk.Adjustment(value=64, lower=1, upper=4096, step_incr=0.1)
        self.spin1 = gtk.SpinButton(adjustment=self.adjustment,digits=6)
        
        self.Hbox1 = gtk.HBox(False,0)
        self.Hbox1.pack_start(self.label1)
        self.Hbox1.pack_start(self.spin1)
        
        self.Vbox2 = gtk.VBox(False,0)
        self.Vbox2.pack_start(self.radio_1)
        self.Vbox2.pack_start(self.radio_2)
        self.Vbox2.pack_start(self.Hbox1)
        
        self.Hbox.pack_start(self.Vbox2)
        
        
        self.output_frame = gtk.Frame(label='Output')
        
        self.check1 = gtk.RadioButton(label="Electric Field and Spectrum")
        self.check2 = gtk.RadioButton(group=self.check1,label="Electric Field, Spectrum and Diagnostics")
        self.check3 = gtk.RadioButton(group=self.check1,label="Everything")
        
        self.check3.set_active(True)
        
        self.Vbox1 = gtk.VBox(False,0)
        self.Vbox1.pack_start(self.check1)
        self.Vbox1.pack_start(self.check2)
        self.Vbox1.pack_start(self.check3)

        
        self.output_frame.add(self.Vbox1)
        self.Hbox.pack_start(self.output_frame)
        
        
        self.save_button = gtk.Button('Save')       
        self.save_button.connect('clicked',self.save_callback)
        self.Vbox.pack_end(self.save_button,False,False)
        
        self.Vbox.pack_start(self.Hbox,False,False)
        
        #add everything to window and show
        self.window.add(self.Vbox)
        self.window.show_all()
    
    
    
    def close_window(self,widget):
        self.window.destroy()
        del self
        
    def save_callback(self,widget):
        if(self.radio_1.get_active()): #its a single image
            image = True
        else: 
            image = False
        
        num_frames = self.adjustment.value
        
        elements = ''
        if(self.check1.get_active()):
            elements = 'Electric Field and Spectrum'
        if(self.check2.get_active()):
            elements = 'Electric Field, Spectrum and Diagnostics'
        if(self.check3.get_active()):
            elements = 'Everything'
        
            
        self.callback(image,num_frames,elements)
        self.close_window(widget)
       
          
