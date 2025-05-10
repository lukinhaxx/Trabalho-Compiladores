import ply.lex as lex

# Lista de tokens
tokens = (
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'SEMICOLON',
)

# Expressões regulares para cada token
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQUALS     = r'='
t_SEMICOLON  = r';'
t_ignore     = ' \t'  # Ignora espaços e tabs

# Identificadores (nomes de variáveis)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Números inteiros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Contador de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erro
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Criar o analisador léxico
lexer = lex.lex()

# Teste simples
if __name__ == '__main__':
    data = '''
    x = 10 + 20;
    y = x - 5;
    '''
    lexer.input(data)

    print("Tokens encontrados:")
    for token in lexer:
        print(token)
