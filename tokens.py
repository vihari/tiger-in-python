#AUTHOR :Vihari Piratla
#Date/Revision:22/5/13
#SP_BLOCK reg expression is not working modify it.
tokens = (
    #symbol
    'ID',
    'INTEGER',
    'STRING',
    
    #esc-seq's
    'NEW_LINE',
    'TAB',
    'SPACE',

    #This is the block enclosed in /.../ and \s,\t,\r,\f and \n 
    # are all ignored
    'SP_BLOCK'

    'COMMENT',
    
    #keywords
    'ARRAY',
    'BREAK',
    'DO',
    'ELSE',
    'END',
    'FOR',
    'FUNCTION',
    'IF',
    'IN',
    'LET',
    'NIL',
    'OF',
    'THEN',
    'TO',
    'TYPE',
    'VAR',
    'WHILE',

    #punctuation symbols
    'COMMA',
    'COLON',
    'SEMI_COLON',
    'L_CIR_BRAC',
    'R_CIR_BRAC',
    'L_SQR_BRAC',
    'R_SQR_BRAC',
    'L_FLR_BRAC',
    'R_FLR_BRAC',
    'DOT',
    'PLUS',
    'MINUS',
    'MUL', #*
    'DIV', #\
    'LT',
    'GT',
    'LTE',
    'GTE',
    'ANG_BRAC',
    'AND',
    'OR',
    'ASSIGN',
    'EQ',
    'NE'
    );

reservedKeywords = (
    'array',
    'break',
    'do',
    'else',
    'end',
    'for',
    'function',
    'if',
    'in',
    'let',
    'nil',
    'of',
    'then',
    'to',
    'type',
    'var',
    'while'
);

def t_ID(t):
    r"[a-zA-Z][a-zA-Z0-9]*";
    if t.value in reservedKeywords:
        t.type = t.value.upper();
    return t;
t_INTEGER =               r"0|[1-9][0-9]*";
def t_STRING(t):
    r'\"([^\\\"]|(\\.))*\"';     #not to match any quotes in the middle.
                                 #tiger does n't allow single quotes
                                 #\. incudes even \s and \S
    new_str = "  ";              #only \n and \t have to be retained
    str = t.value;
    escaped = 0;
    for i in range(0, len(str)): 
        c = str[i] 
        if escaped: 
            if c == "n": 
                c = "\n" 
            elif c == "t": 
                c = "\t" 
            new_str += c 
            escaped = 0 
        else: 
            if c == "\\": 
                escaped = 1 
            else: 
                new_str += c 
    t.value = new_str 
    return t

#usage of ignore keyword provides better lexing performance rather than passing
def t_ignore_NEWLINE(t):
    r"\n+";
    t.lexer.lineno += len(t.value);

t_TAB =                   r"[ \\t]+";

#Though nested comments are allowed, the regexp will match the largest matching string.
t_ignore_COMMENT =        r"///*.*/*//";

#There should be a space after /../
def t_SP_BLOCK(t):
    r'\\(\\.)*\\';
    #rip off all the \s stuff.
    str = t.value;
    new_str = "";
    
    escaped = 0;
    for i in range(1,len(str)):
        c = str[i]
        ig_chars=('n','t','f','r');
        if escaped: 
            if c in ig_chars:
                continue;
            new_str += c 
            escaped = 0 
        else: 
            if c == "\\": 
                escaped = 1 
            elif c!=' ': 
                new_str += c 
    t.value = new_str 
    return t    
    
t_COMMA =               r",";
t_COLON =               r":";
t_SEMI_COLON =          r";";
t_L_CIR_BRAC =          r"\(";
t_R_CIR_BRAC =          r"\)";
t_L_SQR_BRAC =          r"\[";
t_R_SQR_BRAC =          r"\]";
t_L_FLR_BRAC =          r"\{";
t_R_FLR_BRAC =          r"\}";
t_DOT =                 r"\.";
t_PLUS =                r"\+";
t_MINUS =               r"-";
t_MUL =                 r"\*";
t_DIV =                 r"/";
t_LT =                  r"\<";
t_GT =                  r"\>";
t_LTE =                 r"\<\=";
t_GTE =                 r"\>\=";
t_ANG_BRAC =            r"\<\>";
t_AND =                 r"\&";
t_OR =                  r"\|";
t_ASSIGN =              r"\:\=";
t_EQ =                  r"=";
t_NE =                  r"\!=";

def t_error(t):
    print "Illegal character " + str(t.value[0]) + ' at line # '+str(t.lexer.lineno);

if __name__ == '__main__':
	# Build the lexer
	from ply import lex
	import sys 
	
	lex.lex()
	
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
	
	lex.input(data)
	
	# Tokenize
	while 1:
	    tok = lex.token()
	    if not tok: break      # No more input
	    print tok
	

