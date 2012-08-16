import cwiid
import time
import pygame
import uinput
from parser import *

import os
import threading
import re
from collections import deque
#from gi.repository import Gtk


#import sys

class Will:
    ZERO_X = 7956
    ZERO_Y = 7996
    _posx = 0
    _posy = 0
    _wm = None
    _original_nunpos = []
    conf = {}
    action = {"mouse":None}
    events = (uinput.ABS_X, uinput.ABS_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT,uinput.KEY_LEFT,uinput.KEY_RIGHT)
    device = uinput.Device(events)
    def __init__(self):

        
#        self._posx = posx = display.Display().screen().root.query_pointer()._data['root_x']
#        self._posy = display.Display().screen().root.query_pointer()._data['root_y']

#        sys.stdout = os.devnull
        print "Put your wiimote in discovery mode by pressing 1+2..."
        self._wm = cwiid.Wiimote()
        print "found"

        self._wm.rpt_mode = cwiid.RPT_ACC  | cwiid.RPT_BTN  | cwiid.RPT_IR 
        time.sleep(1)
        
        parser = Parser("config.yml")
        self.load_conf(parser.get_conf())
        
        
        
    def use_wiimote(self):
        
        
        self._posx = self._width/2
        self._posy = self._height/2
        

        self.device.emit(uinput.ABS_X,self._posx)
        self.device.emit(uinput.ABS_Y,self._posy)

        counter = 0
        old_button = -1
#        d = display.Display()
#        s = d.screen()
        time.sleep(1)
        while 1:
            counter +=1
            time.sleep(0.01)

    #            print self._wm.state['motionplus']['angle_rate'][2]
#            self.load_mouse(s.root,d)
#            print self.action
        #    print self._wm.state
            self.action["mouse"]()
       
        
            if self._wm.state['buttons'] == 8 and old_button != 8:
#                print "button is 8"
                old_button = 8
                self.device.emit(self.conf['a'],1)
                self.device.emit(self.conf['a'],0)

#                os.system(self.conf['a'])
            elif self._wm.state['buttons'] == 4 and old_button != 4:
#                print "button is 4"
                old_button = 4
                self.device.emit(self.conf['b'],1)
                self.device.emit(self.conf['b'],0)

#                os.system(self.conf['b'])
            elif self._wm.state['buttons'] == 512 and old_button != 512:
                self.device.emit(uinput.KEY_RIGHT,1)
                self.device.emit(uinput.KEY_RIGHT,0)

            elif self._wm.state['buttons'] == 256 and old_button != 512:
                self.device.emit(uinput.KEY_LEFT,1)
                self.device.emit(uinput.KEY_LEFT,0)

            elif self._wm.state['buttons'] == 2048 and old_button != 2048:
                os.system("xdotool click 4")
                old_button = 2048
            elif self._wm.state['buttons'] == 1024 and old_button != 1024:
                os.system("xdotool click 5")
                old_button = 1024
            elif self._wm.state['buttons'] == 4096 and old_button != 4096:
                os.system("xdotool key ctrl+plus")
                old_button = 1024

            elif self._wm.state['buttons'] == 16 and old_button != 16:
                os.system("xdotool key ctrl+minus")
                old_button = 1024
            elif self._wm.state['buttons'] == 128 and old_button != 128:
                self._posx = self._width/2
                self._posy = self._height/2
                self.device.emit(uinput.ABS_X,self._posx)
                self.device.emit(uinput.ABS_Y,self._posy)


            if(counter % 70 == 0):
#                print "counter 10"
                counter = 0
                old_button = 0
#                print self._wm.state['buttons']

    def load_conf(self,conf):

        self._wm.led = cwiid.LED1_ON
        
        self.conf.update(mouse=conf['mouse'])
        self.conf.update(a=ConfigDic.get_name(conf['a']))
        self.conf.update(b=ConfigDic.get_name(conf['b']))
        self._offset = conf['offset']

#        print ConfigDic.get_name(self.conf['a'])

        m = re.search('\d+x\d+',commands.getoutput("xrandr | grep '*'"))
        self._width = m.group(0).split("*")[0]
        self._height = m.group(0).split("*")[1]
#
#        window = Gtk.Window()
#        screen = window.get_screen()
#        self._width = screen.get_width()
#        self._height = screen.get_height()

        self.load_mouse()



    def load_mouse(self):
        if(self.conf['mouse'] == "motion"):
            self._wm.enable(cwiid.FLAG_MOTIONPLUS)
            self._wm.rpt_mode = cwiid.RPT_ACC  | cwiid.RPT_BTN  | cwiid.RPT_IR  | cwiid.RPT_MOTIONPLUS 
            time.sleep(1)
            tvalue_x = 0
            tvalue_y = 0

            print "Calibrating motion plus, still for few moment"
            for i in range(10):
                tvalue_x+= self._wm.state['motionplus']['angle_rate'][2]
                tvalue_y+= self._wm.state['motionplus']['angle_rate'][0]
                time.sleep(0.2)
                
            tvalue_x /= 10
            tvalue_y /= 10
            self.ZERO_X = tvalue_x
            self.ZERO_Y = tvalue_y
            self.action["mouse"] = (lambda : self.load_motion())


        elif(self.conf['mouse'] == "nunchuk"):
            self._wm.rpt_mode = cwiid.RPT_ACC  | cwiid.RPT_BTN  | cwiid.RPT_IR  | cwiid.RPT_NUNCHUK | cwiid.RPT_CLASSIC
            time.sleep(2)
#            print self._wm.state
            self._original_nunpos = self._wm.state['nunchuk']['stick']
              
            self.action["mouse"] = (lambda: self.load_nunchuk())
#            self.load_nunchuk(root,display)

        
    def load_nunchuk(self):
        print self._wm.state
        nunpos = self._wm.state['nunchuk']['stick']
#        print self._original_nunpos
        if (self._posx-self._offset) <= -1:
            if(nunpos[0] > self._original_nunpos[0]+15):
                self._posx += self._offset
                self._wm.rumble = 1
                time.sleep(0.01)
                self._wm.rumble = 0

        elif (self._posx+self._offset) >= self._width+15:
            if(nunpos[0] < self._original_nunpos[0]-15):
                self._posx -= self._offset
                self._wm.rumble = 1
                time.sleep(0.01)
                self._wm.rumble = 0

        elif (self._posx-self._offset) > -15 and (self._posx+self._offset) < self._width:

            if(nunpos[0] > self._original_nunpos[0]+15):
                self._posx += self._offset
            if(nunpos[0] < self._original_nunpos[0]-15):
                self._posx -= self._offset

        if (self._posy-self._offset) <= -15:
            if(nunpos[1] < self._original_nunpos[1]-15):
                self._posy += self._offset
                self._wm.rumble = 1
                time.sleep(0.01)
                self._wm.rumble = 0

        elif  (self._posy+self._offset) >= self._height:
            if(nunpos[1] > self._original_nunpos[1]+15):
                self._posy -= self._offset
                self._wm.rumble = 1
                time.sleep(0.01)
                self._wm.rumble = 0

        elif(self._posy-self._offset) > -15 and (self._posy+self._offset) < self._height:
            if(nunpos[1] < self._original_nunpos[1]-15):
                self._posy += self._offset
            if(nunpos[1] > self._original_nunpos[1]+15):
                self._posy -= self._offset
        
        self.device.emit(uinput.ABS_X,self._posx)
        self.device.emit(uinput.ABS_Y,self._posy)
    #root.warp_pointer(self._posx,self._posy)
    #        display.sync()


    def load_motion(self):


        flag_x = 0
        flag_y = 0
      

        value_x= self.ZERO_X-self._wm.state['motionplus']['angle_rate'][2]
        value_y = self.ZERO_Y-self._wm.state['motionplus']['angle_rate'][0]
        


        if(value_x > 160):
            flag_x =1
        elif(value_x < -160):
            flag_x = -1
        else:
            flag_x = 0
            
        if(value_y > 160):
            flag_y =1
        elif(value_y < -160):
            flag_y = -1
        else:
            flag_y = 0


        if(self._posx+value_x/75) > -1 and (self._posx+value_x/75) < self._width:
            if (flag_x >0):
                self._posx +=value_x/75
            elif (flag_x <0):
                self._posx +=value_x/75
                
                
        if(self._posy-value_y/75) > -1 and (self._posy-value_y/75) < self._height:
            if (flag_y >0):
                self._posy -=value_y/75
            elif (flag_y <0):
                self._posy -=value_y/75
                
        if(flag_y != 0 or flag_x != 0):
            self.device.emit(uinput.ABS_X,self._posx)
            self.device.emit(uinput.ABS_Y,self._posy)
#            root.warp_pointer(self._posx,self._posy)
#            display.sync()
            
        
            



class WillIcon:
    def __init__(self):
        self.statusicon = Gtk.StatusIcon()
        self.statusicon.set_from_stock(Gtk.STOCK_HOME) 
        self.statusicon.connect("popup-menu", self.right_click_event)
        
    
    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()
 
        about = Gtk.MenuItem()
        about.set_label("About")
        quit = Gtk.MenuItem()
        quit.set_label("Quit")
 
        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", Gtk.main_quit)
 
        self.menu.append(about)
        self.menu.append(quit)
 
        self.menu.show_all()
 
        def pos(menu, icon):
                return (Gtk.StatusIcon.position_menu(menu, icon))
 
        self.menu.popup(None, None, pos, self.statusicon, button, time) 
    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()
 
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Will - wiimote for raspberry pi")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Diego Luca Candido"])
 
        about_dialog.run()
        about_dialog.destroy()

w = Will()
w.use_wiimote()
