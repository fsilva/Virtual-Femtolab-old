import gtk


class Toolbar:
    def __init__(self):
        pass
        
    def init_toolbar(self,box,callback):
    # set a Hbox
        self.Hbox = gtk.HBox(False, 0)   
        
    #create buttons
        self.add_new = gtk.Button(label='Add New Element')#, stock=gtk.STOCK_ADD)
        self.add_new.connect("clicked", callback, 'add','add')
        self.Hbox.pack_start(self.add_new)
        
        self.edit = gtk.Button(label='Edit Element')#, stock=gtk.STOCK_PROPERTIES)
        self.edit.connect("clicked", callback,'edit','edit')
        self.Hbox.pack_start(self.edit)
        
        self.remove = gtk.Button(label='Remove Element')#, stock=gtk.STOCK_REMOVE)
        self.remove.connect("clicked", callback, 'remove','remove')
        self.Hbox.pack_start(self.remove)
        
        #self.load = gtk.Button(label='Load', stock=gtk.STOCK_OPEN)
        #self.Hbox.pack_start(self.load)
        
        #self.save = gtk.Button(label='Save', stock=gtk.STOCK_SAVE)
        #self.Hbox.pack_start(self.save)
        
        self.export = gtk.Button(label='Export')
        self.export.connect("clicked", callback, 'export','export')
        self.Hbox.pack_start(self.export)
    
    #add the Vbox to the root box
        box.pack_start(self.Hbox,False,False,0)
        
    def get_height(self):
        return self.Hbox.size_request()[1]
