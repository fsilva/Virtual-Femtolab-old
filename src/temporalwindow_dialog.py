
import gtk

class TemporalWindow_Dialog:

    def __init__(self,config):
        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)

        self.window.set_title("Choose Temporal Window")
        
        self.label1 = gtk.Label('Temporal Window (fs)')
        self.label2 = gtk.Label('Number of Points')
        self.temporal_adj = gtk.Adjustment(value=128, lower=0, upper=1e10, step_incr=1)
        self.spin1 = gtk.SpinButton(adjustment=self.temporal_adj,digits=6)
        self.npoints_adj = gtk.Adjustment(value=256, lower=1, upper=1e10, step_incr=1)
        self.spin2 = gtk.SpinButton(adjustment=self.npoints_adj,digits=6)
        
        self.Vbox = gtk.VBox(False, 0)
        self.Hbox1 = gtk.HBox(False, 0)
        self.Hbox1.pack_start(self.label1,False,False)
        self.Hbox1.pack_end(self.spin1,False,False)
        self.Vbox.pack_start(self.Hbox1)
        self.Hbox2 = gtk.HBox(False, 0)
        self.Hbox2.pack_start(self.label2,False,False)
        self.Hbox2.pack_end(self.spin2,False,False)
        self.Vbox.pack_start(self.Hbox2)
        
        #self.button1 = gtk.Button('Calculate Optimal N. Points')
        #self.button1.connect('clicked',self.calc_npoints)
        self.button2 = gtk.Button('Ok')
        self.button2.connect('clicked',self.ok)
        
        self.Hbox3 = gtk.HBox(False, 0)
        self.Hbox3.pack_end(self.button2,False,False)
        #self.Hbox3.pack_end(self.button1,False,False)
        self.Vbox.pack_start(self.Hbox3)

        self.window.add(self.Vbox)
        self.window.show_all()
        
        self.config = config
        
        
    def ok(self,widget):
        self.close_window(widget)
    
    def close_window(self,widget):
        self.config.deltaT = float(self.temporal_adj.value)*1e-15
        self.config.NT = int(self.npoints_adj.value)
        self.window.destroy()
        gtk.main_quit()
        
          
