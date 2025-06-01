from lexica import lexer
from parser import Parser
from semantic import SemanticAnalyzer

with open("codigo_fonte.txt", "r") as f:
    codigo = f.read()

tokens_validos, tokens_invalidos = lexer(codigo)

if tokens_invalidos:
    print("⚠️ Tokens inválidos encontrados:", tokens_invalidos)
else:
    print("✅ Tokens válidos. Iniciando análise sintática...\n")
    parser = Parser(tokens_validos)
    try:
        ast = parser.program()
        print("✅ Árvore sintática abstrata gerada com sucesso.\n")

        print("🔍 Iniciando análise semântica...\n")
        semantic = SemanticAnalyzer()
        semantic.analyze(ast)
        print("✅ Análise semântica concluída. Sem erros encontrados.")

    except SyntaxError as e:
        print("❌ Erro de sintaxe:", e)

    except Exception as e:
        print("❌ Erro semântico:", e)
import json
from lexica import lexer
from parser import Parser
from semantic import SemanticAnalyzer

def main():
    try:
        # Leitura do código-fonte
        with open("codigo_fonte.txt", "r") as f:
            codigo = f.read()

        print("🚀 Iniciando análise léxica...")
        tokens_validos, tokens_invalidos = lexer(codigo)

        if tokens_invalidos:
            print("\n⚠️ Tokens inválidos encontrados:")
            for token in tokens_invalidos:
                print(f"  -> {token}")
            print("\n❌ Corrija os tokens inválidos antes de prosseguir.")
            return

        print("✅ Análise léxica concluída. Nenhum token inválido encontrado.\n")
        print("🧠 Iniciando análise sintática...")

        # Análise sintática
        parser = Parser(tokens_validos)
        ast = parser.program()
        print("✅ Análise sintática concluída com sucesso.\n")

        # Exibir a AST em formato JSON
        print("🌳 Árvore Sintática Abstrata (AST):\n")
        print(json.dumps(ast, indent=2))

        # (Opcional) Salvar a AST em um arquivo JSON
        with open("ast.json", "w") as ast_file:
            json.dump(ast, ast_file, indent=2)
        print("\n💾 AST salva em 'ast.json'\n")

        # Análise semântica
        print("🔍 Iniciando análise semântica...\n")
        semantic = SemanticAnalyzer()
        semantic.analyze(ast)
        print("✅ Análise semântica concluída. Nenhum erro encontrado.\n")

        print("🎉 Todas as análises foram concluídas com sucesso!")

    except SyntaxError as e:
        print(f"\n❌ Erro de sintaxe: {e}")

    except Exception as e:
        print(f"\n❌ Erro semântico ou inesperado: {e}")

if __name__ == "__main__":
    main()
