from Node import *

types = ['int','string']

class Context(object):
    def __init__(self,name=None):
           self.variables = {}
           self.var_count = {}
           self.dec_type = {}
           self.name = name
           
    def has_var(self,name):
           return name in self.variables
    
    def get_var(self,name):
           return self.variables[name]
	
    def set_var(self,name,typ,dec_type):
           #dec_type fdec,vdec,tdec
           self.dec_type[name] = dec_type
           self.variables[name] = typ
           self.var_count[name] = 0

contexts = []
functions = {
       'print':('void',[
                     ("a",'string')
                     ]),
       'printi':('void',[
                     ("a",'int')
                     ]),
       'flush':('void',[
                     ]),
       'getchar':('string',[
                     ]),
       'ord':('int',[
			("a",'string')
                        ]),
       'chr':('string',[
                     ("a",'int')
                     ]),
	'size':('int',[
                     ("a",'string')
                     ]),
       'substring':('string',[
                     ("a",'string'),
                     ("a",'int'),
                     ("a",'int')
                     ]),
       'concat':('string',[
                     ("a",'string'),
                     ("a",'string')
                     ]),
       'not':('int',[
                     ("a",'int')
                     ]),
       'exit':('void',[
                     ("a",'int')
                     ]),
       }

def pop():
	count = contexts[-1].var_count
	for v in count:
		if count[v] == 0:
			print "Warning: variable %s was declared, but not used." % v
	contexts.pop()

def check_if_function(var):
	if var.lower() in functions and not is_function_name(var.lower()):
		raise Exception, "A function called %s already exists" % var
		
def is_function_name(var):
	for i in contexts[::-1]:
		if i.name == var:
			return True
	return False
		
		
def has_var(varn):
	var = varn.lower()
	check_if_function(var)
	for c in contexts[::-1]:
		if c.has_var(var):
			return True
	return False

def get_var(varn):
	var = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(var):
			c.var_count[var] += 1
			return c.get_var(var)
	raise Exception, "Variable %s is referenced before assignment" % var
	
def set_var(varn,typ):
	var = varn.lower()
	check_if_function(var)
	now = contexts[-1]
	if now.has_var(var):
		raise Exception, "Variable %s already defined" % var
	else:
		now.set_var(var,typ.lower())
	
def get_params(node):
	if node.type == "parameter":
		return [check(node.args[0])]
	else:
		l = []
		for i in node.args:
			l.extend(get_params(i))
		return l
		
def flatten(n):
	if not is_node(n): return [n]
	if not n.type.endswith("_list"):
		return [n]
	else:
		l = []
		for i in n.args:
			l.extend(flatten(i))
		return l
		

def is_node(n):
	return hasattr(n,"type")

def pop_error(*args):
    string = ''
    for arg in args:
        string = string+str(arg)
    print "Semantic analysis error: "+string

def check(node):
    if not is_node(node):
        #if is iterable
        if hasattr(node,"__iter__") and type(node) != type(""):
               for n in node:
                      check(n)
        else:
               return node
    else:

           if node.type == 'let':
               contexts.append(Context('let'))
               check(node.args)
               pop()

           elif node.type == 'ID':
               return node.type

           elif node.type in ['decs']:
               check(node.args)

           elif node.type == "assign_type":
               print node.args
               if node.args[1] != node.args[2].type:
                   if type(node) is Node:
                       if type(node.args[0]) is Node:
                           pop_error("assign_type ",node.args[0].type)
                       else:
                           pop_error("assign_type ",node.args[0])
                   else:
                       type
               
               else:
                   contexts[-1].set_var(node.args[0],node.args[1],'var_dec')
                   
           elif node.type == "assign":
               contexts[-1].set_var(node.args[0],node.args[1],'var_dec')
    
           elif node.type in ["func_void"]:
               contexts.append(Context('func_void'))
               name = str(node.args[0])
               contexts[-1].set_var(node.args[0],node,'func_dec')
               check(node.args)
               pop()
               
           else:
               print "No semantic exists for "+node.type
                  
