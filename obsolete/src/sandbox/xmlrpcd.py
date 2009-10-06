from SimpleXMLRPCServer import SimpleXMLRPCServer
from lino.sprl import go

class MyFuncs:
    def div(self, x, y) : return div(x,y)


server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(pow)
server.register_function(lambda x,y: x+y, 'add')
server.register_introspection_functions()
server.register_instance(MyFuncs())
server.serve_forever()
