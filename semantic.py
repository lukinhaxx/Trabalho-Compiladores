class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.current_function = None

    def analyze(self, node):
        node_type = node["type"]

        if node_type == "Program":
            self.current_function = node["name"]
            self.visit_program(node)
        else:
            raise SemanticError(f"Nó desconhecido no nível superior: {node_type}")

        print("\n📜 Tabela de Símbolos Final:")
        for name, info in self.symbol_table.items():
            print(f"  -> {name}: {info}")

    def visit_program(self, node):
        for stmt in node["body"]:
            self.visit(stmt)

    def visit(self, node):
        node_type = node["type"]

        if node_type == "VarDecl":
            self.visit_var_decl(node)
        elif node_type == "Assignment":
            self.visit_assignment(node)
        elif node_type == "If":
            self.visit_if(node)
        elif node_type == "While":
            self.visit_while(node)
        elif node_type == "For":
            self.visit_for(node)
        elif node_type == "Print":
            self.visit_print(node)
        elif node_type == "Return":
            self.visit_return(node)
        elif node_type in {"Literal", "BinaryOp", "Identifier"}:
            return self.eval_expr(node)
        else:
            raise SemanticError(f"Nó desconhecido: {node_type}")

    def visit_var_decl(self, node):
        var_name = node["var_name"]
        var_type = node["var_type"]

        if var_name in self.symbol_table:
            raise SemanticError(f"Variável '{var_name}' já foi declarada.")

        expr_type = self.eval_expr(node["value"])

        if not self.is_compatible(var_type, expr_type):
            raise SemanticError(f"Tipo incompatível na declaração de '{var_name}'. Esperado {var_type}, obtido {expr_type}.")

        self.symbol_table[var_name] = {"type": var_type, "value": None}

    def visit_assignment(self, node):
        var_name = node["var_name"]

        if var_name not in self.symbol_table:
            raise SemanticError(f"Variável '{var_name}' não foi declarada.")

        var_type = self.symbol_table[var_name]["type"]
        expr_type = self.eval_expr(node["value"])

        if not self.is_compatible(var_type, expr_type):
            raise SemanticError(f"Tipo incompatível na atribuição para '{var_name}'. Esperado {var_type}, obtido {expr_type}.")

    def visit_if(self, node):
        cond_type = self.eval_expr(node["condition"])
        if cond_type != "int":
            raise SemanticError("A condição do 'if' deve ser do tipo int (0 ou 1).")

        for stmt in node["then"]:
            self.visit(stmt)

        if node.get("else"):
            for stmt in node["else"]:
                self.visit(stmt)

    def visit_while(self, node):
        cond_type = self.eval_expr(node["condition"])
        if cond_type != "int":
            raise SemanticError("A condição do 'while' deve ser do tipo int (0 ou 1).")

        for stmt in node["body"]:
            self.visit(stmt)

    def visit_for(self, node):
        self.visit(node["init"])  # Pode ser VarDecl ou Assignment

        cond_type = self.eval_expr(node["condition"])
        if cond_type != "int":
            raise SemanticError("A condição do 'for' deve ser do tipo int (0 ou 1).")

        self.visit(node["update"])

        for stmt in node["body"]:
            self.visit(stmt)

    def visit_print(self, node):
        # Verifica se a expressão a ser impressa é válida
        self.eval_expr({"type": "Literal", "value": node["value"]})

    def visit_return(self, node):
        return_type = self.eval_expr(node["value"])
        # Poderia verificar se o tipo de retorno combina com o tipo da função

    def eval_expr(self, node):
        if node["type"] == "Literal":
            value = node["value"]
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                return "string"
            try:
                if "." in value:
                    float(value)
                    return "float"
                else:
                    int(value)
                    return "int"
            except ValueError:
                return "unknown"

        elif node["type"] == "BinaryOp":
            left_type = self.eval_expr(node["left"])
            right_type = self.eval_expr(node["right"])
            op = node["operator"]

            if left_type != right_type:
                raise SemanticError(f"Operação inválida entre tipos diferentes: {left_type} {op} {right_type}.")

            if op in {"+", "-", "*", "/"}:
                if left_type in ["int", "float"]:
                    return left_type
                raise SemanticError(f"Operador '{op}' não suportado para tipo {left_type}.")
            elif op in {"<", ">", "<=", ">=", "==", "!="}:
                return "int"  # Resultado de comparação é booleano (tratado como int)
            else:
                raise SemanticError(f"Operador desconhecido: {op}")

        elif node["type"] == "Identifier":
            var_name = node["name"]  # Corrigido para usar "name" em vez de "value"
            if var_name not in self.symbol_table:
                raise SemanticError(f"Uso de variável não declarada: {var_name}")
            return self.symbol_table[var_name]["type"]

        raise SemanticError(f"Expressão inválida: {node}")

    def is_compatible(self, declared_type, expr_type):
        if declared_type == expr_type:
            return True
        if declared_type == "float" and expr_type == "int":
            return True  # Permite int em float
        return False