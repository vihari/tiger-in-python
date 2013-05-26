import tokens;
import Node;

#PLY doesn't have the flexibility of specifying a specific rule 
#for every matching rule and hence we regroup the matching patterns to 
#facilitate the same and as an offroute from what is present in the 
#tiger-manual

precedence = (
    ('nonassoc','DO','IF','OF'),
    ('nonassoc','ELSE'),
    ('nonassoc','ASSIGN'),
    ('nonassoc','AND','OR'),
    ('nonassoc','EQ','NEQ','LT','LTE','GT','GTE'),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'DIV', 'MOD'),
    ('nonassoc', 'UMINUS')
    )

def p_let(t):
    "let: LET decs IN seq END"
    t[0] = Node('let',t[2],t[4])

def p_decs(t):
    """decs: decs dec
           | dec"""
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = Node('var_dec',t[1],t[2])

def p_dec(t):
    """dec: tdec
          | fdec
          | vdec
          """
    t[0] = t[1]

def p_vdec(t):
    """vdec: VAR ID ASSIGN exp
           | VAR ID COLON ID ASSIGN exp
           """
    if len(t)==5:
        t[0] = Node('assign',t[2],t[4]);
    else:
        t[0] = Node(assign_type,t[2],t[4],t[6])

def p_fdec(t):
    """fdec: FUNCTION ID L_CIR_BRAC tfields R_CIR_BRAC EQ expr
           | FUNCTION ID L_CIR_BRAC tfields R_CIR_BRAC COLON ID EQ exp
    """
    if len(t)==8:
        t[0] = Node('proc',t[2],t[4],t[7])
    else:
        t[0] = Node('func',t[2],t[4],t[7],t[9])

def p_tdec(t):
    "tdec: TYPE ID EQ type"
    t[0] = Node('tdec',t[2],t[4])
    
def p_type(t):
    """type: ID
           | record
           | array_def
    """
    if len(t)==4:
        t[0] = Node('record_def',t[2])
    else:
        t[0] = Node('array_def',t[2])
    

def p_record(t):
    'record: L_FLR_BRAC tfields R_FLR_BRAC'
    t[0] = Node('record',t[2]);

def p_array_def(t):
    'array_def: ARRAY OF ID'
    t[0] = Node('array_def',t[2])

def p_tfields(t):
    '''tfields: type-field
              | tfields COMMA type-field
    '''
    if len(t) == 4:
        t[0] = Node('type-fields',t[1],t[3])
    else:
        t[0] = t[1]

def p_type_field(t):
    'type_field: ID COLON ID'
    t[0] = Node('type-field',t[1],t[3])

def p_expr_seq(t):
    '''
    expr_seq: expr
            | expr_seq SEMI_COLON expr
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = Node('exp_seq',t[1],t[3])

def p_lval(t):
    'lval   : var '
    t[0] = t[1]

def p_var(t):
    '''var    : ID  
              | ID opt_var
              '''
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
    if p[1] == '.' and len(t) == 3:
        t[0] = Node('field',t[2]);
    elif p[1] == '.' and len(t) == 4:
        t[0] = Node('fields',t[2,t[3]])
    elif p[2] == '[' and len(t) == 4:
        t[0] = Node('array_idx',t[2])
    else:
        t[0] = Node('array_idxs',t[2],t[4])

def p_array(t):
    'array  : ID L_SQR_BRAC exp R_SQR_BRAC OF exp'
    t[0] = Node('array_dec',t[3],t[6])

def p_assign(t):
    'assign : var ASSIGN exp'
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
      '''
    if p[1] == '-':
        t[0] = Node('UMINUS',0,t[2])
    else:
        t[0] = Node('bin_op',t[2],t[1],t[3])

def p_flow(t):
    '''
    flow : Break                   
     | WHILE exp DO exp            
     | IF exp THEN exp %prec IF   
     | IF exp THEN exp ELSE exp   
     | FOR ID ASSIGN exp TO exp DO exp
     '''
    if p[1] == 'while':
        t[0] = Node('while',t[2],t[4])
    elif p[1] == 'for':
        t[0] = Node('for',t[2],t[4],t[6],t[8])
    elif p[1] == 'if' and len(t) == 5:
        t[0] = Node('if',t[2],t[4])
    else:
        t[0] = Node('if_else',t[2],t[4],t[6])

def seqexp(t):
    'seqexp: L_CIR_BRAC expr_seq R_CIR_BRAC'
    t[0] = t[2]

def const(t):
    '''
    const: INTEGER
         | STRING
         | NIL
    '''
    t[0] = t[1]

def p_call(t):
    '''
    call: ID L_CIR_BRAC R_CIR_BRAC
        | ID L_CIR_BRAC args R_CIR_BRAC
    '''

def p_args(t):
    '''
    args: args COMMA exp
        | exp
    '''
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
    t[0] = t[1]

def p_error(t):
    print "Syntax error in input, in line %d!" % t.lineno
    sys.exit()
