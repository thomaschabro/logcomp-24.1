import sys
from abc import abstractmethod

class PrePro:
    def filter(code):
        filtered_lines = []
        output = ""
        for line in code.split('\n'):
            line = line.strip()
            if line and not line.startswith('--'):
                if line.find("--") != -1:
                    line = line[:line.find("--")]
                filtered_lines.append(line)
        for line in filtered_lines:
            output += line + "\n"
        return output
    
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
class Tokenizer():
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next
        self.list = [
            "print",
            "if",
            "then",
            "else",
            "end",
            "while",
            "do",
            "and",
            "or",
            "not",
            "read",
            "local"]
    
    def selectNext(self):
        if self.position >= len(self.source):
            self.next = None

        else:
            if self.source[self.position] == " ":
                self.position += 1
                self.selectNext()
            elif self.source[self.position] == "+":
                self.position += 1
                self.next = Token("PLUS", "+")
            elif self.source[self.position] == "-":
                self.position += 1
                self.next = Token("MINUS", "-")
            elif self.source[self.position] == "*":
                self.position +=1
                self.next = Token("TIMES", "*")
            elif self.source[self.position] == "/":
                self.position +=1
                self.next = Token("DIV", "/")
            elif self.source[self.position] == "(":
                self.position += 1
                self.next = Token("LPAREN", "(")
            elif self.source[self.position] == ")":
                self.position += 1
                self.next = Token("RPAREN", ")")
            elif self.source[self.position] == "\n":
                self.position += 1
                self.next = Token("NL", "\n")
            elif self.source[self.position] == ">":
                self.position += 1
                self.next = Token("GT", ">")
            elif self.source[self.position] == "<":
                self.position += 1
                self.next = Token("LT", "<")
            elif self.source[self.position] == "\"":
                string = ""
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] != "\"":
                    string += self.source[self.position]
                    self.position += 1
                if self.position == len(self.source):
                    sys.stderr.write("Erro de sintaxe. Aspas não fechadas. (1)")
                    sys.exit(1)
                self.position += 1
                self.next = Token("STR", string)
            elif self.source[self.position] == "=":
                self.position += 1
                if self.position < len(self.source) and self.source[self.position] == "=":
                    self.position += 1
                    self.next = Token("EQ", "==")
                else:
                    self.next = Token("ASSIGN", "=")
            elif self.source[self.position] == ".":
                self.position += 1
                if self.position < len(self.source) and self.source[self.position] == ".":
                    self.position += 1
                    self.next = Token("CONCAT", "..")
            elif self.source[self.position].isdigit():
                number = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    number += self.source[self.position]
                    self.position += 1
                self.next = Token("NUMBER", number)
            elif self.source[self.position].isalpha():
                iden = ""
                while self.position < len(self.source) and self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_':
                    iden += self.source[self.position]
                    self.position += 1
                if iden in self.list:
                    self.next = Token(iden.upper(), iden)
                else:
                    self.next = Token("IDEN", iden)
            else:
                sys.stderr.write("Erro de sintaxe. Caractere inválido. (1)")
                sys.exit(1)
                return
            

class Node():
    def __init__ (self, value:int, children=None):
        self.value = value
        self.children = children if children is not None else []

    @abstractmethod
    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st):
        print(self.value, self.children[0].Evaluate(st), self.children[1].Evaluate(st))
        if self.value == "..":
            return ["STR", str(self.children[0].Evaluate(st)[1]) + str(self.children[1].Evaluate(st)[1])]
        if self.children[0].Evaluate(st)[0] == "INT" and self.children[1].Evaluate(st)[0] == "INT":    
            if self.value == "+":
                return ["INT", int(self.children[0].Evaluate(st)[1]) + int(self.children[1].Evaluate(st)[1])]
            elif self.value == "-":
                return ["INT", int(self.children[0].Evaluate(st)[1]) - int(self.children[1].Evaluate(st)[1])]
            elif self.value == "*":
                return ["INT", int(self.children[0].Evaluate(st)[1]) * int(self.children[1].Evaluate(st)[1])]
            elif self.value == "/":
                return ["INT", int(self.children[0].Evaluate(st)[1]) // int(self.children[1].Evaluate(st)[1])]
            elif self.value == "and":
                return ["INT", int(self.children[0].Evaluate(st)[1]) and int(self.children[1].Evaluate(st)[1])]
            elif self.value == "or":
                return ["INT", int(self.children[0].Evaluate(st)[1]) or int(self.children[1].Evaluate(st)[1])]
            elif self.value == "==":
                return ["INT", int(int(self.children[0].Evaluate(st)[1]) == int(self.children[1].Evaluate(st)[1]))]
        elif self.children[0].Evaluate(st)[0] == self.children[1].Evaluate(st)[0]:
            if self.value == "==":
                return [self.children[0].Evaluate(st)[0], int(int(self.children[0].Evaluate(st)[1]) == int(self.children[1].Evaluate(st)[1]))]
            elif self.value == ">":
                return [self.children[0].Evaluate(st)[0], int(int(self.children[0].Evaluate(st)[1]) > int(self.children[1].Evaluate(st)[1]))]
            elif self.value == "<":
                return [self.children[0].Evaluate(st)[0], int(int(self.children[0].Evaluate(st)[1]) < int(self.children[1].Evaluate(st)[1]))]
        else:
            sys.stderr.write("Tipo dos operadores inválido.")
            sys.exit(1)
            return

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st):
        if self.children[0].Evaluate(st)[0] == "INT":
            if self.value == "+":
                return ["INT", int(self.children[0].Evaluate(st)[1])]
            elif self.value == "-":
                return ["INT", int(-self.children[0].Evaluate(st)[1])]
            elif self.value == "not":
                return ["INT", int(not self.children[0].Evaluate(st)[1])]
        else:
            sys.stderr.write("Tipo dos operadores inválido para UnOp")
            sys.exit(1)
            return
        
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self, st):
        return ["INT", int(self.value)]
    
class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self, st):
        return ["STR", self.value]
    
class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def Evaluate(self, st):
        pass

class Block(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class Identifier(Node):
    def _init_(self, value):
        super()._init_(value, [])

    def Evaluate(self, st):
        try:
            try:
                true = st.get(self.value).isalpha()
                return ["STR", st.get(self.value)]
            except:
                return ["INT", st.get(self.value)]
        except:
            sys.stderr.write("Variável sendo usada sem ser declarada [ " + self.value + " ]")
            sys.exit(1)

class Assign(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        st.set(self.children[0].value, self.children[1].Evaluate(st)[1], self.children[1].Evaluate(st)[0])

class VarDec(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        if self.children[1] is not None:
            st.create(self.children[0].value)
            st.set(self.children[0].value, self.children[1].Evaluate(st)[1], self.children[1].Evaluate(st)[0])
        else:
            st.create(self.children[0].value)   

class Print(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        var = self.children[0].Evaluate(st)
        print(var)
        if var[0] == "STR":
            sys.stdout.write(str(var[1]) + "\n")
        elif var[0] == "INT":
            sys.stdout.write(str(var[1]) + "\n")

class If(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)
        elif len(self.children) == 3:
            self.children[2].Evaluate(st)

class While(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        while self.children[0].Evaluate(st):
            for child in self.children[1]:
                child.Evaluate(st)

class Read(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        return ["INT", self.value]
        
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parseExpression(tok):
        resultado = Parser.parseTerm(tok)
        while (1):
            if tok.next is not None and tok.next.type == "PLUS":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6 0 1)")
                    sys.exit(1)
                else:
                    resultado = BinOp("+", [resultado, Parser.parseTerm(tok)])
            elif tok.next is not None and tok.next.type == "MINUS":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6 1 )")
                    sys.exit(1)
                else:
                    resultado = BinOp("-", [resultado, Parser.parseTerm(tok)])
            elif tok.next is not None and tok.next.type == "CONCAT":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6 2 )")
                    sys.exit(1)
                else:
                    resultado = BinOp("..", [resultado, Parser.parseTerm(tok)])
            else:
                return resultado

    def parseTerm(tok):
        resultado = Parser.parseFactor(tok)
        while (1):
            if tok.next is not None and tok.next.type == "TIMES":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (7)")
                    sys.exit(1)
                else:
                    resultado = BinOp("*", [resultado, Parser.parseFactor(tok)])

            elif tok.next is not None and tok.next.type == "DIV":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (7)")
                    sys.exit(1)
                else:
                    resultado = BinOp("/", [resultado, Parser.parseFactor(tok)])
            else:
                return resultado

    def parseFactor(tok):
        if tok.next.type == "NUMBER":
            numero = tok.next.value
            tok.selectNext()
            return IntVal(numero)
        elif tok.next is not None and tok.next.type == "PLUS":
            tok.selectNext()
            numero = UnOp("+", [Parser.parseFactor(tok)])
            return numero
        elif tok.next is not None and tok.next.type == "MINUS":
            tok.selectNext()
            numero = UnOp("-", [Parser.parseFactor(tok)])
            return numero
        elif tok.next is not None and tok.next.type == "NOT":
            tok.selectNext()
            numero = UnOp("not", [Parser.parseFactor(tok)])
            return numero
        elif tok.next is not None and tok.next.type == "LPAREN":
            tok.selectNext()
            resultado = Parser.parseBoolExp(tok)
            if tok.next.type != "RPAREN":
                sys.stderr.write("Erro de sintaxe. ')' esperado. (9)")
                sys.exit(1)
            else:
                tok.selectNext()
                return resultado
        elif tok.next.type == "IDEN":
            id_saida = Identifier(tok.next.value)
            tok.selectNext()
            return id_saida
        elif tok.next.type == "READ":
            tok.selectNext()
            if tok.next.type != "LPAREN":
                sys.stderr.write("Erro de sintaxe. '(' esperado. (10)")
                sys.exit(1)
            else:
                tok.selectNext()
                if tok.next.type != "RPAREN":
                    sys.stderr.write("Erro de sintaxe. ')' esperado. (11)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return Read(value=int(input()))
        elif tok.next.type == "STR":
            string = tok.next.value
            tok.selectNext()
            return StrVal(value=string)
        else:
            sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (10)")
            sys.exit(1)

    def parseStatement(tok):
        if tok.next.type == "IDEN":
            iden = tok.next.value
            tok.selectNext()
            if tok.next.type == "ASSIGN":
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. New Line esperado. (11)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return Assign(value="assign",children=[Identifier(iden), saida])
            else:
                sys.stderr.write("Erro de sintaxe. '=' esperado. (31)")
                sys.exit(1)
        elif tok.next.type == "PRINT":
            tok.selectNext()
            if tok.next.type != "LPAREN":
                sys.stderr.write("Erro de sintaxe. '(' esperado. (4)")
                sys.exit(1)
            else:
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "RPAREN":
                    sys.stderr.write("Erro de sintaxe. ')' esperado. (5)")
                    sys.exit(1)
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após RPAREN. (6)")
                    sys.exit(1)
                tok.selectNext()
                return Print(value="print", children=[saida])
        elif tok.next.type == "IF":
            tok.selectNext()
            condicao = Parser.parseBoolExp(tok)
            if tok.next.type != "THEN":
                sys.stderr.write("Erro de sintaxe. 'then' esperado. (7)")
                sys.exit(1)
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após THEN. (8)")
                sys.exit(1)
            tok.selectNext()
            bloco1 = Parser.parseStatement(tok)
            if tok.next.type == "ELSE":
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após ELSE. (9)")
                    sys.exit(1)
                tok.selectNext()
                bloco2 = Parser.parseStatement(tok)
                if tok.next.type != "END":
                    sys.stderr.write("Erro de sintaxe. 'end' esperado. (8)")
                    sys.exit(1)
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após END. (9)")
                    sys.exit(1)
                tok.selectNext()
                return If(value="if", children=[condicao, bloco1, bloco2])
            elif tok.next.type == "END":
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após END. (10)")
                    sys.exit(1)
                tok.selectNext()
                return If(value="if", children=[condicao, bloco1])
            else:
                sys.stderr.write("Erro de sintaxe. 'end' esperado. (9)")
                sys.exit(1)
        elif tok.next.type == "WHILE":
            tok.selectNext()
            condicao = Parser.parseBoolExp(tok)
            if tok.next.type != "DO":
                sys.stderr.write("Erro de sintaxe. 'do' esperado. (10)")
                sys.exit(1)
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após DO. (11)")
                sys.exit(1)
            tok.selectNext()
            lista_statements = []
            while (tok.next.type != "END"):
                lista_statements.append(Parser.parseStatement(tok))
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após END. (12)")
                sys.exit(1)
            tok.selectNext()
            return While(value="while", children=[condicao, lista_statements])
        elif tok.next.type == "LOCAL":
            tok.selectNext()
            if tok.next.type != "IDEN":
                sys.stderr.write("Erro de sintaxe. Identificador esperado. (12)")
                sys.exit(1)
            iden = tok.next.value
            tok.selectNext()
            if tok.next.type == "ASSIGN":
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após NL. (13)")
                    sys.exit(1)
                tok.selectNext()
                return VarDec(value="assign", children=[Identifier(iden), saida])
            elif tok.next.type == "NL":
                tok.selectNext()
                return VarDec(value="assign", children=[Identifier(iden), None])
            else:
                sys.stderr.write("Erro de sintaxe. Erro após LOCAL. (14)")
                sys.exit(1)
        else:
            sys.stderr.write("Erro de sintaxe. '=' esperado. (3)")
            sys.exit(1)

    def parseBoolExp(tok):
        resultado = Parser.parseBoolTerm(tok)

        while (1):
            if tok.next.type == "OR":
                tok.selectNext()
                resultado = BinOp("or", [resultado, Parser.parseBoolTerm(tok)])
            else:
                return resultado
            
    def parseBoolTerm(tok):
        resultado = Parser.parseRelExp(tok)

        while (1):
            if tok.next.type == "AND":
                tok.selectNext()
                resultado = BinOp("and", [resultado, Parser.parseRelExp(tok)])
            else:
                return resultado
            
    def parseRelExp(tok):
        resultado = Parser.parseExpression(tok)
        if tok.next.type == "GT":
            tok.selectNext()
            return BinOp(">", [resultado, Parser.parseExpression(tok)])
        elif tok.next.type == "LT":
            tok.selectNext()
            return BinOp("<", [resultado, Parser.parseExpression(tok)])
        elif tok.next.type == "EQ":
            tok.selectNext()
            return BinOp("==", [resultado, Parser.parseExpression(tok)])
        else:
            return resultado

    def parseBlock(tok):
        saida = Block([])
        while tok.next is not None:
            saida.children.append(Parser.parseStatement(tok))
        return saida

    def run(code):
        code_filtrado = PrePro.filter(code=code)
        tokenizer = Tokenizer(code_filtrado, 0, None)
        tokenizer.selectNext()
        ast = Parser.parseBlock(tokenizer)
        st = SymbolTable()
        resultado = ast.Evaluate(st)
        if tokenizer.next is not None:
            sys.stderr.write("Erro de sintaxe. EOF esperado. (2)")
            sys.exit(1)
        else:
            return resultado


class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def set(self, key, value, type):
        if key in self.table:
            self.table[key] = [value, type]
        else:
            sys.stderr.write("Variável sendo definida sem ser declarada [ " + key + " ]")
            sys.exit(1)

    def get(self, key):
        return self.table[key][0]
    
    def create(self, key):
        self.table[key] = None

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <file>")
        print("  |-> EXEMPLO: python main.py teste.lua")
        return
    
    file = sys.argv[1]
    if file[-4:] != ".lua":
        print("Erro: Arquivo inválido. Deve ser do tipo .lua")
        sys.stderr.write("Erro: Arquivo inválido. Deve ser do tipo .lua")
        sys.exit(1)
        return
    with open(file, "r") as f:
        file = f.read()
    
    left, right = 0, 0
    for char in file:
        if char == '(':
            left += 1
        if char == ')':
            right += 1
    
    if left != right:
        print("Erro: Número de parênteses inválido.")
        sys.stderr.write("Erro de sintaxe. Número de parênteses inválido.")
        sys.exit(1)
        return

    else:
        Parser.run(file)

if __name__ == "__main__":
    main()