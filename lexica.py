import re

# Definição de tokens
RESERVED_WORDS = {"func", "string", "int", "float", "if", "else", "print"}
OPERATORS = {"=", "+", "-", "*", "/", "<", ">", "<=", ">=", "==", "!=", "&&", "||"}
DELIMITERS = {"(", ")", "{", "}", ";", ","}
TOKEN_REGEX = {
    "IDENTIFIER": r"[a-zA-Z_]\w*",
    "NUMBER": r"\d+(\.\d+)?",
    "STRING": r"\".*?\"",
    "OPERATOR": r"(==|!=|<=|>=|&&|\|\||=|\+|\-|\*|/|<|>)",
    "DELIMITER": r"[\(\){};,]",
}

# Função de análise léxica
def lexer(code):
    tokens = []
    invalid_tokens = []
    i = 0
    while i < len(code):
        if code[i].isspace():
            i += 1
            continue

        match = None
        for token_type, regex in TOKEN_REGEX.items():
            pattern = re.compile(regex)
            match = pattern.match(code, i)
            if match:
                lexeme = match.group()
                if token_type == "IDENTIFIER":
                    if lexeme in RESERVED_WORDS:
                        tokens.append(("RESERVED", lexeme))
                    else:
                        tokens.append((token_type, lexeme))
                else:
                    tokens.append((token_type, lexeme))
                i = match.end()
                break

        if not match:
            invalid_tokens.append(code[i])
            i += 1

    return tokens, invalid_tokens

# Exemplo de código de entrada
codigo = '''
func cadastrarCarro() {
    string modelo = "Civic";
    int ano = 2020;
    float preco = 95000.50;

    if (ano >= 2010 && preco < 100000) {
        print("Cadastro válido");
    } else {
        print("Cadastro inválido");
    }
}
'''

# Execução
tokens_validos, tokens_invalidos = lexer(codigo)

# Resultados
print("=== TOKENS VÁLIDOS ===")
for token in tokens_validos:
    print(token)

