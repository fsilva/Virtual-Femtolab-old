
import pulseBeam
import initialpulse_dialog
import addelement_dialog

import element_propagation
import element_thinlens
import element_chirpedmirror
import element_filter

class Propagator:
    def __init__(self,config):
        self.config = config
        self.initialPulseBeam = pulseBeam.pulseBeam(self.config)
        self.pulseBeam = pulseBeam.pulseBeam(self.config)
        
        self.elements = []

        
    def example_pulseBeam(self):
        self.initialPulseBeam.initialize_pulse(6.6e-15,0,0,0,0,2e-3,1e10,0,1e-3,1000)
        
        self.initialPulseBeam.calculate_autoco()
        self.initialPulseBeam.calculate_FROG()
        
        self.pulseBeam.copy(self.initialPulseBeam)
        
        

    
    def example_elements(self):
        #self.elements.append(element_thinlens.Element_ThinLens(1,800e-9))
        self.elements.append(element_propagation.Element_Propagation(0.025,element_propagation.materials[1],800e-9))
        #self.elements.append(element_propagation.Element_Propagation(0.005,element_propagation.materials[0],800e-9))
        #self.elements.append(element_chirpedmirror.Element_ChirpedMirror(element_chirpedmirror.mirrors[0],10,800e-9))
        #self.elements.append(element_propagation.Element_Propagation(0.005,element_propagation.materials[0],800e-9))
        
        
    def get_max_z(self):
        z0 = 0
        for element in self.elements:
            z0 += element.length
        return z0
        
    def change_z(self,z):
        max_z = self.get_max_z()
        if(z > max_z):
            z = max_z
            return
        
        self.pulseBeam.copy(self.initialPulseBeam)
    
        z0 = 0
        i = 0
        n1 = 0
        n2 = self.elements[0].n
        while(z0 < z and i < len(self.elements)):
            if(z0+self.elements[i].length < z):
               self.elements[i].calc_pulseBeam(self.elements[i].length,self.pulseBeam)
               self.pulseBeam.beam_apply_propagation(self.elements[i].length,self.elements[i].n) #should this move into calc_pulseBeam?
               #refraction at the interface

               n1 = n2
               if(self.elements[i+1].n != 0):
                   n2 = self.elements[i+1].n
                   if(n1 != 0 and n2 != 0):
                       self.pulseBeam.beam_apply_refraction(n1,n2)

               z0 += self.elements[i].length
               i += 1
            else:
               self.elements[i].calc_pulseBeam(z-z0,self.pulseBeam)
               self.pulseBeam.beam_apply_propagation(z-z0,self.elements[i].n)
               z0 = z
    
        self.pulseBeam.calculate_autoco()
        self.pulseBeam.calculate_FROG()   
        
        
    def open_edit_dialog(self,selected,refresh_callback):
        if(selected == 0):
            self.initial_pulse_open_edit_dialog(refresh_callback)
        elif(selected <= len(self.elements)):
            self.elements[selected-1].open_edit_dialog(refresh_callback)
            #-1 because 0 is the initial pulse
            
    def initial_pulse_open_edit_dialog(self,refresh_callback):
        self.initialpulse_dialog = initialpulse_dialog.InitialPulse_Dialog(self.initialPulseBeam,refresh_callback,self.config)
        
    def open_add_dialog(self,selected,refresh_callback):
        self.refresh_callback = refresh_callback
        self.selected = selected
        self.addelement_dialog = addelement_dialog.AddElement_Dialog(self.add_element)
        
    def add_element(self,element_type):
        if(element_type == 'Material Propagation'):
           element = element_propagation.Element_Propagation(0.001,element_propagation.materials[0],800e-9)
        elif(element_type == 'Thin Lens'):
           element = element_thinlens.Element_ThinLens(0.1,800e-9)
        elif(element_type == 'Chirped Mirror'):
           element = element_chirpedmirror.Element_ChirpedMirror(element_chirpedmirror.mirrors[0],22,800e-9)
        elif(element_type == 'Bandstop Spectral Filter'):
           element = element_filter.Element_Filter(780e-9,820e-9)
        else:
            return
            
        self.elements.insert(self.selected,element)
        
        element.open_edit_dialog(self.refresh_callback)
        
        self.refresh_callback() 
        
    def remove_element(self,selected,refresh_callback):
        if(selected == 0):
            print 'Cannot remove initial inpulse'
            return
        if(selected > len(self.elements)):
            print 'remove_element: invalid selected data'
            return 
        
        del self.elements[selected-1] 
            
        refresh_callback() 
