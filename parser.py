import lexer
import sys
from Node import Node

debug=False
# META
#start = 'exp'

#PLY doesn't have the flexibility of specifying a specific rule 
#for every matching rule and hence we regroup the matching patterns to 
#facilitate the same and as an offroute from what is present in the 
#tiger-manual

precedence = (
    ('nonassoc','DO','IF','OF'),
    ('nonassoc','ELSE'),
    ('nonassoc','ASSIGN'),
    ('nonassoc','AND','OR'),
    ('nonassoc','EQ','NE','LT','LTE','GT','GTE'),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'DIV','MUL'),
    ('nonassoc', 'UMINUS')
    )

def p_let(t):
    '''let : LET decs IN exp_seq END
    '''
    if(debug):
        print str(t.lexer.lineno)+"let";

    t[0] = Node('let',t[2],t[4])

def p_decs(t):
    '''decs : decs dec
            | dec
    '''
    if(debug):
        print str(t.lexer.lineno)+"decs";

    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = Node('decs',t[1],t[2])

def p_dec(t):
    """dec : tdec
           | fdec
           | vdec
          """
    if(debug):
        print str(t.lexer.lineno)+"dec";

    t[0] = t[1]

def p_vdec(t):
    """vdec : VAR ID ASSIGN exp
            | VAR ID COLON ID ASSIGN exp
           """
    if(debug):
        print str(t.lexer.lineno)+"vdec";

    if len(t)==5:
        t[0] = Node('assign',t[2],t[4]);
    else:
        t[0] = Node('assign_type',t[2],t[4],t[6])

def p_fdec(t):
    """fdec : FUNCTION ID L_CIR_BRAC tfields R_CIR_BRAC EQ exp
            | FUNCTION ID L_CIR_BRAC tfields R_CIR_BRAC COLON ID EQ exp
            | FUNCTION ID L_CIR_BRAC R_CIR_BRAC COLON ID EQ exp
            | FUNCTION ID L_CIR_BRAC R_CIR_BRAC EQ exp
    """

    if(debug):
        print str(t.lexer.lineno)+"fdec";

    if len(t)==10:
        t[0] = Node('proc',t[2],t[4],t[7],t[9])
    elif len(t)==9:
        t[0] = Node('proc_void',t[2],t[6],t[8])
    elif len(t)==8:
        t[0] = Node('func',t[2],t[4],t[7])
    else:
        t[0] = Node('func_void',t[2],t[6])

def p_tdec(t):
    "tdec : TYPE ID EQ type"
    if(debug):
        print str(t.lexer.lineno)+"tdec";

    t[0] = Node('tdec',t[2],t[4])
    
def p_type(t):
    """type : ID
            | record
            | array_def
    """
    if(debug):
        print str(t.lexer.lineno)+"type";

    if t[1]=='record':
        t[0] = Node('record_def',t[1])
    elif t[1] == 'array_def':
        t[0] = Node('array_def',t[1])
    else:
        t[0] = Node('ID',t[1])

def p_record(t):
    'record : L_FLR_BRAC tfields R_FLR_BRAC'
    if(debug):
        print str(t.lexer.lineno)+"record";
    
    t[0] = Node('record',t[2]);

def p_array_def(t):
    'array_def : ARRAY OF ID'
    
    if(debug):
        print str(t.lexer.lineno)+"array_def";

    t[0] = Node('array_def',t[2])

def p_tfields(t):
    '''tfields : type_field
               | tfields COMMA type_field
    '''
    if(debug):
        print str(t.lexer.lineno)+"tfields";

    if len(t) == 4:
        t[0] = Node('tfields',t[1],t[3])
    else:
        t[0] = t[1]

def p_type_field(t):
    'type_field : ID COLON ID'
    if(debug):
        print str(t.lexer.lineno)+"type_field";
    t[0] = Node('type_field',t[1],t[3])

def p_exp_seq(t):
    '''
    exp_seq : exp
             | exp_seq SEMI_COLON exp
    '''
    if(debug):
        print str(t.lexer.lineno)+"exp_seq";

    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = Node('exp_seq',t[1],t[3])

def p_lval(t):
    'lval : var '

    if(debug):
        print str(t.lexer.lineno)+"lval";

    t[0] = t[1]

def p_var(t):
    '''var    : ID  
              | ID opt_var
              '''
    if(debug):
        print str(t.lexer.lineno)+"var";

    if len(t) == 2:
        t[0] = Node('var',t[1])
    else:
        t[0] = Node('field_or_array_idx',t[1],t[2])

def p_opt_var(t):
    '''opt_var : DOT ID              
    | L_SQR_BRAC exp R_SQR_BRAC        
    | DOT ID opt_var          
    | L_SQR_BRAC exp R_SQR_BRAC opt_var 
    '''

    if(debug):
        print str(t.lexer.lineno)+"opt_var";

    if t[1] == '.' and len(t) == 3:
        t[0] = Node('field',t[2]);
    elif t[1] == '.' and len(t) == 4:
        t[0] = Node('fields',t[2],t[3])
    elif t[1] == '[' and len(t) == 4:
        t[0] = Node('array_idx',t[2])
    else:
        print len(t)
        t[0] = Node('array_idxs',t[2],t[4])

def p_array(t):
    'array  : ID L_SQR_BRAC exp R_SQR_BRAC OF exp'

    if(debug):
        print str(t.lexer.lineno)+"array";

    t[0] = Node('array_dec',t[3],t[6])

def p_assign(t):
    'assign : var ASSIGN exp'

    if(debug):
        print str(t.lexer.lineno)+"assign";

    t[0] = Node('assign',t[1],t[3])

def p_opexp(t):
    '''opexp : MINUS exp %prec UMINUS
      | exp PLUS exp %prec PLUS 
      | exp MINUS exp %prec MINUS 
      | exp MUL exp %prec MUL 
      | exp DIV exp %prec DIV
      | exp EQ exp  %prec EQ  
      | exp NE exp %prec NE 
      | exp LT exp  %prec LT  
      | exp LTE exp  %prec LTE  
      | exp GT exp  %prec GT  
      | exp GTE exp  %prec GTE  
      | exp AND exp %prec AND
      | exp OR exp  %prec OR  
      | exp ANG_BRAC exp %prec EQ
      '''
    #| opexp AND exp %prec AND
    #ANG_BRAC and EQ can be used interchagibly
    
    if(debug):
        print str(t.lexer.lineno)+"opexp";

    if t[1] == '-':
        t[0] = Node('UMINUS',0,t[2])
    else:
        t[0] = Node(t[2],t[1],t[3])
        if debug:
            print t[1],t[2],t[3]

def p_flow(t):
    '''
    flow : BREAK                   
     | WHILE exp DO exp            
     | IF exp THEN exp %prec IF   
     | IF exp THEN exp ELSE exp   
     | FOR ID ASSIGN exp TO exp DO exp
     '''

    if(debug):
        print str(t.lexer.lineno)+"flow";

    if t[1] == 'while':
        t[0] = Node('while',t[2],t[4])
    elif t[1] == 'for':
        t[0] = Node('for',t[2],t[4],t[6],t[8])
    elif t[1] == 'if' and len(t) == 5:
        t[0] = Node('if',t[2],t[4])
    else:
        t[0] = Node('if_else',t[2],t[4],t[6])

def p_seqexp(t):
    'seqexp : L_CIR_BRAC exp_seq R_CIR_BRAC'

    if(debug):
        print str(t.lexer.lineno)+"seqexp";

    t[0] = t[2]

def p_const(t):
    '''
    const : integer
          | string
          | nil
    '''

    if(debug):
        print str(t.lexer.lineno)+"const";

    t[0] = t[1]

def p_integer(t):
    '''
    integer : INTEGER
    '''
    if(debug):
        print str(t.lexer.lineno)+"integer";
    t[0] = Node('int',t[1])

def p_string(t):
    'string : STRING'
    if(debug):
        print str(t.lexer.lineno)+"string";
    t[0] = Node('str',t[1])    

def p_nill(t):
    'nil : NIL'
    if(debug):
        print str(t.lexer.lineno)+"nil";
    t[0] = Node('nil',t[1])    

def p_call(t):
    '''
    call : ID L_CIR_BRAC R_CIR_BRAC
         | ID L_CIR_BRAC args R_CIR_BRAC
    '''

    if(debug):
        print str(t.lexer.lineno)+"call";

    if len(t)==4:
        t[0] = Node('p_call',t[1])
    else:
        t[0] = Node('f_call',t[1],t[3])

def p_args(t):
    '''
    args : args COMMA exp
         | exp
    '''

    if(debug):
        print str(t.lexer.lineno)+"args";

    if len(t) == 2:
        t[0] = t[1]
    else: 
        t[0] = Node('args',t[1],t[3])

def p_exp(t):
    '''
    exp : const 
    | seqexp
    | call   
    | record 
    | opexp  
    | flow   
    | lval   
    | array  
    | assign 
    | let   
    '''

    if(debug):
        print str(t.lexer.lineno)+"exp";
        print t[1]

    t[0] = t[1]

def p_error(t):
    print "Syntax error in input, in line %d!" % t.lineno
    print "Some extra info: ? "
    print t
    sys.exit()
