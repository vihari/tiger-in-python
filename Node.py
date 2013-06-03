#Describes nodes in the AST
#type of node, and 
class Node(object):
    def __init__(self, t, *args):
        self.type = t
        self.args = args
		
    def __str__(self):
        s = "type: " + str(self.type) + "\n"
        s += "".join( ["i: " + str(i) + "\n" for i in self.args])
        return s
    def dump(self):
        print self.type
        for arg in self.args:
            if type(arg) is Node:
                arg.dump()
                
    def nodes(self,node):

        if type(self) is Node:
            node.append(str(self.type))
        else:
            node.append(str(self))

        for arg in self.args:
            if type(arg) is Node:
                node.append(str(self.type))
                arg.nodes(node)
            else:
                node.append(str(arg))

    def edges(self,edge):
        for arg in self.args:
            if type(arg) is Node:
                edge.append( (str(self.type)+'('+str(id(self))+')',str(arg.type)+'('+str(id(arg))+')' ))
                arg.edges(edge)
            else:
                edge.append( (str(self.type)+'('+str(id(self))+')',str(arg)+'('+str(id(arg))+')' ))
        
        
        
        
