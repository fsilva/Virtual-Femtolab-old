
from math import ceil

import gtk
import propagator

class Schematic:

    def __init__(self,propagator,refresh_callback):
        self.propagator = propagator
        self.selected = 0
        self.refresh_callback = refresh_callback
        pass
        
    def init_schematic(self,box):
        self.area = gtk.DrawingArea()
        self.area.set_size_request(1024,100) #fix this - resize width on window resize
        box.pack_start(self.area,False,False,0)    
        self.drawable = None
        self.area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.area.connect("button-press-event", self.clicked, None)
        
    def clicked(self,widget,event,arg1):
        if(event.x < 45):
            self.selected = 0
        else:
            event.x -= 45
            self.selected = int(ceil(event.x/150))
        self.refresh_callback()

        
    def draw_schematic(self,z):
        #print 'draw schematic z=',z
        if(self.drawable is None):
            self.drawable = self.area.window
            if(self.drawable is None):
                #print 'draw schematic drawable error'
                return
            self.context = self.drawable.cairo_create()
            if(self.context is None):
                print 'draw schematic context error'
                return
#clean background                
        self.context.rectangle(0,0,1440,100)
        self.context.set_source_rgb(1, 1, 1)
        self.context.fill()
        
        total_len = 0   
        z0 = 0     
        current_x = 0
        line_drawn = False
#draw elements
        self.context.set_source_rgb(0, 0, 0)
        self.context.select_font_face("Sans")#, CAIRO_FONT_SLANT_NORMAL,CAIRO_FONT_WEIGHT_BOLD)
        self.context.set_font_size(14.0)
        
#draw 'initial pulse'
        if(self.selected == 0):
            self.context.rectangle(5,5,45,90)
            self.context.set_source_rgb(0.7, 0.7, 0.7)
            self.context.fill()
        self.context.set_source_rgb(0, 0, 0)
        self.context.move_to(10,33)
        self.context.show_text('Initial')
        self.context.move_to(10,66)
        self.context.show_text('Pulse')
        self.context.rectangle(5,5,45,90)
        if(self.selected == 0):
            self.context.set_line_width(2.0)
        else:
            self.context.set_line_width(1.0)
        self.context.stroke()
        
        element_width = 150 #change above
        current_x = 55
        i = 0
        
        for element in self.propagator.elements:
            i += 1
            
            #if(z < z0+element.length and line_drawn == False):
            #    self.context.set_source_rgba(0, 0, 0,1)
            #else:
            #    self.context.set_source_rgba(0, 0, 0,0.5)
            
            
            #draw rect
            if(self.selected == i):
                self.context.rectangle(current_x,5,element_width-5,90)
                self.context.set_source_rgb(0.7, 0.7, 0.7)
                self.context.fill()
            
            self.context.set_source_rgba(0, 0, 0,1)
            self.context.rectangle(current_x,5,element_width-5,90)
            if(self.selected == i):
                self.context.set_line_width(2.0)
            else:
                self.context.set_line_width(1.0)
            self.context.stroke()
            
                            

            
            #draw text
            self.context.move_to(current_x+5,33)
            self.context.show_text(element.name)
            self.context.move_to(current_x+5,66)
            if(element.length > 0):
                self.context.show_text(str(element.length)+' m')
            elif(element.name == 'Thin Lens'):
                self.context.show_text('f = '+str(element.f)+' m')
            
            #should we draw the position line over this element?
            if(z <= z0+element.length and line_drawn == False):
                line_drawn = True
                deltaz = z-z0
                if(element.length > 0):
                    posline_x = current_x+element_width*deltaz/element.length
                else:
                    posline_x = current_x
                self.context.set_line_width(2.0)
                self.context.move_to(posline_x, 10)
                self.context.line_to(posline_x, 90)
                self.context.set_source_rgba(1, 0, 0,1)
                self.context.stroke()
                
                
            z0 += element.length
            current_x += element_width

        

#draw position line       
        self.context.set_source_rgb(1, 1, 1)


        
        
