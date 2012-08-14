import yaml

class Parser:
    conf = ""
    def __init__(self, name):
        try:
            self.conf = yaml.load(open(name))
        except yaml.YAMLError, exc:
            print "Error in configuration file:", exc
    def get_conf(self):
        return self.conf

