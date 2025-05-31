from lexica import lexer
from parser import Parser

with open("codigo_fonte.txt", "r") as f:
    codigo = f.read()

tokens_validos, tokens_invalidos = lexer(codigo)

if tokens_invalidos:
    print("⚠️ Tokens inválidos encontrados:", tokens_invalidos)
else:
    print("✅ Tokens válidos. Iniciando análise sintática...\n")
    parser = Parser(tokens_validos)
    try:
        parser.parse()
        print("✅ Análise sintática concluída com sucesso. Código bem estruturado.")
    except SyntaxError as e:
        print("❌ Erro de sintaxe:", e)
