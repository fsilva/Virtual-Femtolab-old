
import gtk

import config
import pulseBeam
import spectrum_loader


class AddElement_Dialog:

    def __init__(self,add_callback):
    
        self.add_callback = add_callback
                
        #create window
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)
        self.window.set_default_size(300,100)
        self.window.set_title("Add Element")
        
        self.Vbox = gtk.VBox(False, 0)
        
        #add hbox with label and combobox
        self.Hbox = gtk.HBox(False, 0)
        
        self.type_label = gtk.Label('Element Type')
        self.type_combo = gtk.combo_box_new_text()
        self.add_elements_to_combobox()
        self.Hbox.pack_start(self.type_label)
        self.Hbox.pack_end(self.type_combo)
        self.Vbox.pack_start(self.Hbox)
        
        self.extra_label = gtk.Label('The element will be added after the selected one')
        self.Vbox.pack_start(self.extra_label)
        
        self.Hbox2  = gtk.HBox(False, 0)
        self.ok     = gtk.Button('Ok')
        self.ok.connect('clicked',self.button_callback)
        self.cancel = gtk.Button('Cancel')
        self.cancel.connect('clicked',self.button_callback)
        self.Hbox2.pack_start(self.ok)
        self.Hbox2.pack_start(self.cancel)
        self.Vbox.pack_start(self.Hbox2)

        
        #add everything to window and show
        self.window.add(self.Vbox)
        self.window.show_all()
    
    def add_elements_to_combobox(self):
        self.type_combo.append_text('Material Propagation')
        self.type_combo.append_text('Thin Lens') 
        self.type_combo.append_text('Chirped Mirror') 
        self.type_combo.append_text('Bandstop Spectral Filter')         

        self.type_combo.set_active(0)
        
    def button_callback(self,widget):
        self.window.destroy()
        if(widget == self.ok):
            self.add_callback(self.type_combo.get_active_text())
        del self
    
    
    def close_window(self,widget):
        del self 
        #print 'erro isto nao esta bem feito, podem haver varias janelas abertas'
        
       
          
