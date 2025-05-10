from ply import lex

# 1. Definindo os tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'ID'
)

# 2. Regras para cada token (usando regex)
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'  # Ex: x, soma, var1

# 3. Regra para números (com ação adicional)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Converte para inteiro
    return t

# 4. Ignorar espaços e tabs
t_ignore = ' \t'

# 5. Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()

# --- Testes ---
if __name__ == "__main__":
    data = "x = 42 + (30 * y)"
    lexer.input(data)

    print("Tokens encontrados:")
    for token in lexer:
        print(f"Tipo: {token.type}, Valor: {token.value}")