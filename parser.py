import yaml
import uinput
class Parser:
    conf = ""
    def __init__(self, name):
        try:
            self.conf = yaml.load(open(name))
        except yaml.YAMLError, exc:
            print "Error in configuration file:", exc
    def get_conf(self):
        return self.conf

class ConfigDic:
    _keys = {'a': uinput.KEY_A,'b':uinput.KEY_B,'c':uinput.KEY_C,'d':uinput.KEY_D,'e':uinput.KEY_E,'f':uinput.KEY_F,'g':uinput.KEY_G,'h':uinput.KEY_H,'i':uinput.KEY_I,'l':uinput.KEY_L,'m':uinput.KEY_M,'n':uinput.KEY_N,'o':uinput.KEY_O,'p':uinput.KEY_P,'q':uinput.KEY_Q,'r':uinput.KEY_R,'s':uinput.KEY_S,'t':uinput.KEY_T,'u':uinput.KEY_U,'v':uinput.KEY_V,'z':uinput.KEY_Z,'up':uinput.KEY_UP,'down':uinput.KEY_DOWN,'left':uinput.KEY_LEFT,'right':uinput.KEY_RIGHT,'rclick': uinput.BTN_RIGHT, 'lclick': uinput.BTN_LEFT}
    @classmethod
    def get_name(self,name):
        print self._keys[name]
        return self._keys[name]
