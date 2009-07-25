#!/usr/bin/env python

#import libraries
import gtk
import gobject
import os

#import other python scripts
import plots
import schematic
import toolbar

import temporalwindow_dialog
import export_dialog

import propagator
import config

class Application:    
    def init_window(self):

        self.window = gtk.Window()
        self.window.connect("destroy", self.close_window)
        self.window.connect("size_allocate",self.refresh_callback)
        self.window.set_default_size(1024,600)
        self.window.set_title("Virtual FemtoLab")
        
        self.Vbox = gtk.VBox(False, 0)
        
        self.plots = plots.Plots()    
        self.plots.init_plots(self.Vbox)
        
        self.config = config
        self.propagator = propagator.Propagator(self.config)
        
        self.schematic = schematic.Schematic(self.propagator,self.refresh)
        self.schematic.init_schematic(self.Vbox)
        
        self.spin_button = gtk.SpinButton(adjustment=None, climb_rate=0.0, digits=6)
        self.Vbox.pack_start(self.spin_button,False,False,0)
        
        self.scale = gtk.HScrollbar(adjustment=None)
        self.scale.set_update_policy(gtk.UPDATE_DELAYED)

        self.Vbox.pack_start(self.scale,False,False,0)
        
        self.toolbar = toolbar.Toolbar()    
        self.toolbar.init_toolbar(self.Vbox,self.button_callback)
        
        self.window.add(self.Vbox)
        
        #setup the propagator with an example structure
        
        self.propagator.example_pulseBeam()
        self.propagator.example_elements()
        
        #propagator is set, setup the L adjustment
        self.l_adjustment = gtk.Adjustment(value=0, lower=0, upper=self.propagator.get_max_z()-0.0001, step_incr=0.0001)

        self.l_adjustment.connect('value_changed',self.change_z)
        self.scale.set_adjustment(self.l_adjustment)
        self.spin_button.set_adjustment(self.l_adjustment)
                
        self.plots.draw_pulseBeam(self.propagator.pulseBeam)

        self.window.show_all()
        gobject.timeout_add (750, self.refresh_callback2,0)
        
        self.current_z = 0
    
    def change_z(self,adjustment):
        self.current_z = adjustment.value
        self.scale.set_value(adjustment.value)
        self.spin_button.set_value(adjustment.value)
        self.propagator.change_z(adjustment.value)
        self.plots.update_pulseBeam(self.propagator.pulseBeam)
        self.schematic.draw_schematic(adjustment.value)
        self.window.show_all()
        
    def refresh(self):
        self.change_z(self.l_adjustment)
        max_z = self.propagator.get_max_z()
        if(max_z != self.l_adjustment.upper):
            self.l_adjustment.upper = max_z
        
    def refresh_callback(self,widget,arg):
        self.refresh()
        
    def refresh_callback2(self,arg):
        self.refresh()
        
    def button_callback(self,widget,event,name):
        if(name == 'edit'):
            self.propagator.open_edit_dialog(self.schematic.selected,self.refresh)
        if(name == 'add'):
            self.propagator.open_add_dialog(self.schematic.selected,self.refresh)
        if(name == 'remove'):
            if(self.schematic.selected > len(self.propagator.elements)):
                 return
            self.dialog = gtk.MessageDialog(self.window,flags=gtk.DIALOG_MODAL,type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_YES_NO,message_format='Are you shure you want to remove the selected element?') 
            resp = self.dialog.run()
            if resp == gtk.RESPONSE_YES:
                self.propagator.remove_element(self.schematic.selected,self.refresh)
            self.dialog.destroy()
        if(name == 'export'):
            self.exporter_dialog = export_dialog.Export_Dialog(self.export)
            
    def export(self,image,numframes,elements):
         if(image): #its a single frame, ask for a filename and write it
             filesel = gtk.FileChooserDialog(title='Select PNG filename',action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
         
             response = filesel.run()
   
             if response == gtk.RESPONSE_OK:
                 filename = filesel.get_filename()
                 filesel.destroy()
             elif response == gtk.RESPONSE_CANCEL:
                 print 'Closed, no files selected, not saving frame'
                 filesel.destroy()
                 return
                 
             self.export_frame(filename+'.png',elements)
         else: # many frames, ask for a directory name and write 'XXXXXXXX.png' there
               # bonus write a mencoder bash script(to wmv) and a imagemagick bash script (to gif)
             filesel = gtk.FileChooserDialog(title='Select directory name',action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
         
             response = filesel.run()
   
             if response == gtk.RESPONSE_OK:
                 dirname = filesel.get_filename()
                 filesel.destroy()
             elif response == gtk.RESPONSE_CANCEL:
                 print 'Closed, no files selected, not saving frame'
                 filesel.destroy()
                 return

             csv_file = open(dirname+'/propagation.csv','w')
             string = 'z(m);spot(m);curvature(m);peak power(W);peak intensity(Wm^-2);energy(J);\n'
             csv_file.write(string)


             z = 0
             j = 0
             num_elements = 0
             for element in self.propagator.elements:
                 if(not element.is_discrete()):
                     num_elements += 1
             frames_per_element = numframes/num_elements
             for element in self.propagator.elements:
                 if(not element.is_discrete()):
                     for i in xrange(int(frames_per_element)):
                         j += 1
                         z += element.length/frames_per_element
                         self.l_adjustment.value = z
                         self.change_z(self.l_adjustment)
                         filename = dirname + "/%.6d.png"%j
                         self.export_frame(filename,elements)
                         #export data into csv
                         string = '%e;%e;%e;%e;%e;%e;\n'%(z,self.propagator.pulseBeam.BeamProfile_spot,\
                                                     self.propagator.pulseBeam.BeamProfile_curvature,\
                                                     self.propagator.pulseBeam.calc_peak_power(),\
                                                     self.propagator.pulseBeam.calc_peak_intensity(),\
                                                     self.propagator.pulseBeam.calc_energy())
                         csv_file.write(string)

             csv_file.close()
             f=file(dirname+'/make_mpeg2.bat','w')
             f.write('mencoder -ovc lavc -lavcopts vcodec=mpeg2video:vbitrate=1500  -mf type=png:fps=5 -nosound -of mpeg -o output.mpg mf://*.png')
             f.close()
             f=file(dirname+'/make_gif.bat','w')
             f.write('convert *.png  -delay 20 animation.gif')
             f.close()
             f=file(dirname+'/make_README.txt','w')
             f.write('You need imagemagick for make_gif.bat and mencoder for make_mpeg2.bat')
             f.close()
             
         
    def export_frame(self,filename,elements):
        dpi = 100
        if(elements == 'Everything'):
            w,h = self.window.window.get_size()

            h -= self.toolbar.get_height()+self.scale.size_request()[1] #remove scroll bar and buttons        

            pixbuf = gtk.gdk.Pixbuf.get_from_drawable(gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, w, h),self.window.window,gtk.gdk.colormap_get_system(), 0,0, 0, 0, w, h)
            pixbuf.save(filename,'png')
            print 'export frame', filename
        elif(elements == 'Electric Field and Spectrum'):
            self.plots.save_electric_field_png('1.png',dpi)  #hmm Hack. should not create temporary files anywhere
            self.plots.save_spectrum_png('2.png',dpi)        #future: investigate TempFile module
            # join images
            from PIL import Image
            im1 = Image.open('1.png')
            im2 = Image.open('2.png')
            im3 = Image.new('RGB',(im1.size[0]+im2.size[0],max(im1.size[1],im2.size[1])))
            im3.paste(im1,(0,0))
            im3.paste(im2,(im1.size[0],0))
            im3.save(filename)
            del im1
            del im2
            del im3
            os.remove('1.png')
            os.remove('2.png')
        else:
            self.plots.save_electric_field_png('1.png',dpi)  #hmm Hack. should not create temporary files anywhere
            self.plots.save_spectrum_png('2.png',dpi)        #future: investigate TempFile module
            self.plots.save_autoco_png('3.png',dpi) 
            self.plots.save_FROG_png('4.png',dpi) 
            # join images
            from PIL import Image
            im1 = Image.open('1.png')
            im2 = Image.open('2.png')
            im3 = Image.open('3.png')
            im4 = Image.open('4.png')
            im5 = Image.new('RGB',(max(im1.size[0]+im3.size[0],im2.size[0]+im4.size[0]),max(im1.size[1]+im2.size[1],im3.size[1]+im4.size[1])))
            im5.paste(im1,(0,0))
            im5.paste(im2,(0,im1.size[1]))
            im5.paste(im3,(im1.size[0],0))
            im5.paste(im4,(im2.size[0],im1.size[1]))
            im5.save(filename)
            del im1
            del im2
            del im3
            del im4
            del im5
            os.remove('1.png')
            os.remove('2.png')
            os.remove('3.png')
            os.remove('4.png')
            
            
            
    def close_window(self,arg):
        gtk.main_quit()
        
TmpWin = temporalwindow_dialog.TemporalWindow_Dialog(config)
gtk.main() #when the user closes/Oks the window, the execution proceeds

App = Application()
App.init_window()
       
gtk.main()

