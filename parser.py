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
        return True

    def expect(self, expected_type=None, expected_value=None):
        if not self.match(expected_type, expected_value):
            raise SyntaxError(f"Erro de sintaxe na posição {self.pos}: esperado {expected_type} '{expected_value}'.")

    def parse(self):
        self.program()

    def program(self):
        self.expect("RESERVED", "func")
        self.expect("IDENTIFIER")
        self.expect("DELIMITER", "(")
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        self.stmt_list()
        self.expect("DELIMITER", "}")

    def stmt_list(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] != "}":
            self.stmt()

    def stmt(self):
        token = self.tokens[self.pos]
        if token[0] == "RESERVED":
            if token[1] in {"int", "string", "float"}:
                self.var_decl()
                self.expect("DELIMITER", ";")
            elif token[1] == "if":
                self.if_stmt()
            elif token[1] == "while":
                self.while_stmt()
            elif token[1] == "for":
                self.for_stmt()
            elif token[1] == "print":
                self.print_stmt()
                self.expect("DELIMITER", ";")
            elif token[1] == "return":
                self.return_stmt()
        elif token[0] == "IDENTIFIER":
            self.assignment()
            self.expect("DELIMITER", ";")
        else:
            raise SyntaxError(f"Comando inesperado: {token}")

    def var_decl(self):
        self.match("RESERVED")  # tipo
        self.expect("IDENTIFIER")
        self.expect("OPERATOR", "=")
        self.expr()

    def assignment(self):
        self.expect("IDENTIFIER")
        self.expect("OPERATOR", "=")
        self.expr()

    def if_stmt(self):
        self.expect("RESERVED", "if")
        self.expect("DELIMITER", "(")
        self.expr()
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        self.stmt_list()
        self.expect("DELIMITER", "}")
        if self.match("RESERVED", "else"):
            self.expect("DELIMITER", "{")
            self.stmt_list()
            self.expect("DELIMITER", "}")

    def while_stmt(self):
        self.expect("RESERVED", "while")
        self.expect("DELIMITER", "(")
        self.expr()
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        self.stmt_list()
        self.expect("DELIMITER", "}")

    def for_stmt(self):
        self.expect("RESERVED", "for")
        self.expect("DELIMITER", "(")
        self.var_decl()
        self.expect("DELIMITER", ";")
        self.expr()
        self.expect("DELIMITER", ";")
        self.assignment()
        self.expect("DELIMITER", ")")
        self.expect("DELIMITER", "{")
        self.stmt_list()
        self.expect("DELIMITER", "}")

    def print_stmt(self):
        self.expect("RESERVED", "print")
        self.expect("DELIMITER", "(")
        self.expect("STRING")
        self.expect("DELIMITER", ")")

    def return_stmt(self):
        self.expect("RESERVED", "return")
        self.expr()
        self.expect("DELIMITER", ";")

    def expr(self):
        # Para simplificação: expr = IDENTIFIER | NUMBER | STRING
        token = self.tokens[self.pos]
        if token[0] in {"IDENTIFIER", "NUMBER", "STRING"}:
            self.pos += 1
            # Aceita operadores binários simples (expr OP expr)
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == "OPERATOR":
                self.pos += 1
                self.expr()
        elif token == ("DELIMITER", "("):
            self.pos += 1
            self.expr()
            self.expect("DELIMITER", ")")
        else:
            raise SyntaxError(f"Expressão inválida: {token}")
