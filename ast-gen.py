import pydot
from lexer import *
from parser import *

def grph(edges,filename):
   g=pydot.graph_from_edges(edges) 
   if filename:
       f = filename + ".svg"
   else:
       f = "graph.svg"
   g.write_svg(f, prog='dot') 
        
def ast_gen(ast):
    nodes = []
    edges = []
    ast.nodes(nodes)
    ast.edges(edges)
    #nodes=set(nodes)
    #edges=set(edges)
    #print nodes
    #print edges
    grph(edges,"8q")

def main():
    # Build the lexer
    from ply import lex,yacc
    import sys 
    
    #lex.lex(debug=True)
    yacc.yacc(debug=False)
    
    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
    else:
        data = ""
        while 1:
            try:
                data += raw_input() + "\n"
            except:
                break
            
    ast = yacc.parse(data,lexer = lex.lex(debug=False))	
    ast_gen(ast)
            
	# Tokenize
        
if __name__:
    main()
	

