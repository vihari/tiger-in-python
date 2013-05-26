#Describes nodes in the AST
#type of node, and 
class Node:
    def __init__(self,type,*args):
         self.type = type
         if args:
              self.args = args
         else:
              self.args = [ ]
