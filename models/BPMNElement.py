from models.XMLSerializable import XMLSerializable

class BPMNElement(XMLSerializable):

    def __init__(self, **args):
        self.id = self.expects(args, 'id')      
        self.name = self.expects(args, 'name')

    def expects(self, args, name, default = None):
        return default if name not in args else args[name]

    def __str__(self):
        return str (self.id);