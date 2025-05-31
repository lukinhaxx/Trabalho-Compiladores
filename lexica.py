import re

# Definição de tokens
RESERVED_WORDS = {"func", "string", "int", "float", "if", "else", "while", "for", "print", "return"}
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
                if token_type == "IDENTIFIER" and lexeme in RESERVED_WORDS:
                    tokens.append(("RESERVED", lexeme))
                else:
                    tokens.append((token_type, lexeme))
                i = match.end()
                break

        if not match:
            invalid_tokens.append(code[i])
            i += 1

    return tokens, invalid_tokens

# Leitura de arquivo-fonte
with open("codigo_fonte.txt", "r") as f:
    codigo = f.read()

tokens_validos, tokens_invalidos = lexer(codigo)

# Exibição dos tokens
print("=== TOKENS VÁLIDOS ===")
for token in tokens_validos:
    print(token)

print("\n=== TOKENS INVÁLIDOS ===")
for token in tokens_invalidos:
    print(token)
