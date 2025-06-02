class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, expected_type=None, expected_value=None):
        if self.pos >= len(self.tokens):
            return False
        token_type, token_value = self.tokens[self.pos]
        if (expected_type and token_type != expected_type) or (expected_value and token_value != expected_value):
            return False
        self.pos += 1
        return token_type, token_value

    def expect(self, expected_type=None, expected_value=None):
        result = self.match(expected_type, expected_value)
        if not result:
            raise SyntaxError(f"Erro de sintaxe na posição {self.pos}: esperado {expected_type} '{expected_value}'.")
        return result

    def parse(self):
        return self.program()

    def program(self):
        self.expect("RESERVED", "func")
        func_name = self.expect("IDENTIFIER")[1]
        self.expect("DELIMITER", "(")
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        body = self.stmt_list()
        self.expect("DELIMITER", "}")

        return {"type": "Program", "name": func_name, "body": body}

    def stmt_list(self):
        stmts = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] != "}":
            stmts.append(self.stmt())
        return stmts

    def stmt(self):
        token = self.tokens[self.pos]
        if token[0] == "RESERVED":
            if token[1] in {"int", "string", "float"}:
                node = self.var_decl()
                self.expect("DELIMITER", ";")
                return node
            elif token[1] == "if":
                return self.if_stmt()
            elif token[1] == "while":
                return self.while_stmt()
            elif token[1] == "for":
                return self.for_stmt()
            elif token[1] == "print":
                node = self.print_stmt()
                self.expect("DELIMITER", ";")
                return node
            elif token[1] == "return":
                node = self.return_stmt()
                self.expect("DELIMITER", ";")
                return node
        elif token[0] == "IDENTIFIER":
            node = self.assignment()
            self.expect("DELIMITER", ";")
            return node
        else:
            raise SyntaxError(f"Comando inesperado: {token}")

    def var_decl(self):
        var_type = self.expect("RESERVED")[1]
        var_name = self.expect("IDENTIFIER")[1]
        self.expect("OPERATOR", "=")
        value = self.expr()
        return {"type": "VarDecl", "var_type": var_type, "var_name": var_name, "value": value}

    def assignment(self):
        var_name = self.expect("IDENTIFIER")[1]
        self.expect("OPERATOR", "=")
        value = self.expr()
        return {"type": "Assignment", "var_name": var_name, "value": value}

    def if_stmt(self):
        self.expect("RESERVED", "if")
        self.expect("DELIMITER", "(")
        condition = self.expr()
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        then_body = self.stmt_list()
        self.expect("DELIMITER", "}")

        else_body = None
        if self.match("RESERVED", "else"):
            self.expect("DELIMITER", "{")
            else_body = self.stmt_list()
            self.expect("DELIMITER", "}")

        return {"type": "If", "condition": condition, "then": then_body, "else": else_body}

    def while_stmt(self):
        self.expect("RESERVED", "while")
        self.expect("DELIMITER", "(")
        condition = self.expr()
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        body = self.stmt_list()
        self.expect("DELIMITER", "}")
        return {"type": "While", "condition": condition, "body": body}

    def for_stmt(self):
        self.expect("RESERVED", "for")
        self.expect("DELIMITER", "(")
        init = self.var_decl()
        self.expect("DELIMITER", ";")
        condition = self.expr()
        self.expect("DELIMITER", ";")
        update = self.assignment()
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        body = self.stmt_list()
        self.expect("DELIMITER", "}")
        return {
            "type": "For",
            "init": init,
            "condition": condition,
            "update": update,
            "body": body
        }

    def print_stmt(self):
        self.expect("RESERVED", "print")
        self.expect("DELIMITER", "(")
        value = self.expect("STRING")[1]
        self.expect("DELIMITER", ")")
        return {"type": "Print", "value": value}

    def return_stmt(self):
        self.expect("RESERVED", "return")
        value = self.expr()
        return {"type": "Return", "value": value}

    def expr(self):
        token = self.tokens[self.pos]

        if token[0] == "IDENTIFIER":
            self.pos += 1
            node = {"type": "Identifier", "name": token[1]}
            
            # Verifica operadores binários
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == "OPERATOR":
                op = self.tokens[self.pos][1]
                self.pos += 1
                right = self.expr()
                node = {"type": "BinaryOp", "operator": op, "left": node, "right": right}
                
            return node
            
        elif token[0] == "NUMBER":
            self.pos += 1
            node = {"type": "Literal", "value": token[1]}
            
            # Verifica operadores binários
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == "OPERATOR":
                op = self.tokens[self.pos][1]
                self.pos += 1
                right = self.expr()
                node = {"type": "BinaryOp", "operator": op, "left": node, "right": right}
                
            return node
            
        elif token[0] == "STRING":
            self.pos += 1
            return {"type": "Literal", "value": token[1]}

        elif token == ("DELIMITER", "("):
            self.pos += 1
            node = self.expr()
            self.expect("DELIMITER", ")")
            return node

        else:
            raise SyntaxError(f"Expressão inválida: {token}")