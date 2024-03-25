import sys
from abc import abstractmethod

class PrePro:
    def filter(code):
        code_limpo = ""
        i = 0
        while i < len(code):
            if code[i] == '-' and i + 1 < len(code) and code[i + 1] == '-':
                while i < len(code) and code[i] != '\n':
                    i += 1
                if i == len(code) or code[i] != '\n':
                    code_limpo += "\n"
            elif code[i] == '\n':
                code_limpo += code[i]
                while i + 1 < len(code) and code[i + 1] == '\n':
                    i += 1
            else:
                code_limpo += code[i]
            i += 1

        return code_limpo

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
class Tokenizer():
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next
    
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
            elif self.source[self.position] == "=":
                self.position += 1
                self.next = Token("ASSIGN", "=")
            elif self.source[self.position].isdigit():
                number = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    number += self.source[self.position]
                    self.position += 1
                self.next = Token("NUMBER", number)
            elif self.source[self.position].isalpha():
                iden = ""
                while self.position < len(self.source) and self.source[self.position].isalpha():
                    iden += self.source[self.position]
                    self.position += 1
                if iden == "print":
                    self.next = Token("PRINT", iden)
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
        if self.value == "+":
            return int(self.children[0].Evaluate(st)) + int(self.children[1].Evaluate(st))
        elif self.value == "-":
            return int(self.children[0].Evaluate(st)) - int(self.children[1].Evaluate(st))
        elif self.value == "*":
            return int(self.children[0].Evaluate(st)) * int(self.children[1].Evaluate(st))
        elif self.value == "/":
            return int(self.children[0].Evaluate(st)) // int(self.children[1].Evaluate(st))

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st):
        if self.value == "+":
            return int(self.children[0].Evaluate(st))
        elif self.value == "-":
            return int(-self.children[0].Evaluate(st))
        
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self):
        return int(self.value)
    
class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def Evaluate(self):
        pass

class Block(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class Identifier(Node):
    def _init_(self, value):
        super()._init_(value, [])

    def evaluate(self, st):
        return st.get(self.value)

class Assign(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def evaluate(self, st):
        st.set(self.children[0].value, self.children[1].evaluate(st))

class Print(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def evaluate(self, st):
        print(self.children[0].evaluate(st))
        sys.stdout.write(str(self.children[0].evaluate(st)))
        
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parseExpression(tok):
        resultado = Parser.parseTerm(tok)
        while (1):
            if tok.next is not None and tok.next.type == "PLUS":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6)")
                    sys.exit(1)
                else:
                    resultado = BinOp("+", [resultado, Parser.parseTerm(tok)])
            elif tok.next is not None and tok.next.type == "MINUS":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6)")
                    sys.exit(1)
                else:
                    resultado = BinOp("-", [resultado, Parser.parseTerm(tok)])
            else:
                return resultado

    def parseTerm(tok):
        resultado = Parser.parseFactor(tok)
        while (1):
            if tok.next is not None and tok.next.type == "TIMES":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (7)")
                    sys.exit(1)
                else:
                    resultado = BinOp("*", [resultado, Parser.parseFactor(tok)])

            elif tok.next is not None and tok.next.type == "DIV":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
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
        elif tok.next != None and tok.next.type == "PLUS":
            tok.selectNext()
            numero = UnOp("+", [Parser.parseFactor(tok)])
            return numero
        elif tok.next != None and tok.next.type == "MINUS":
            tok.selectNext()
            numero = UnOp("-", [Parser.parseFactor(tok)])
            return numero
        elif tok.next != None and tok.next.type == "LPAREN":
            resultado = Parser.parseExpression(tok)
            if tok.next.type != "RPAREN":
                sys.stderr.write("Erro de sintaxe. ')' esperado. (9)")
                sys.exit(1)
            else:
                tok.selectNext()
                return resultado
        elif tok.next.type == "IDEN":
            id = Identifier(tok.next.value)
            tok.selectNext()
            return id
        else:
            sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (10)")
            sys.exit(1)

    def parseStatement(tok):
        if tok.next.type == "IDEN":
            id = tok.next.value
            tok.selectNext()
            if tok.next.type == "ASSIGN":
                tok.selectNext()
                saida = Parser.parseExpression(tok)
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. New Line esperado. (11)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return Assign([Identifier(id), saida])
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
                saida = Parser.parseExpression(tok)
                if tok.next.type != "RPAREN":
                    sys.stderr.write("Erro de sintaxe. ')' esperado. (5)")
                    sys.exit(1)
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada. (6)")
                    sys.exit(1)
                tok.selectNext()
                print = Print([saida])
                return print
        else:
            sys.stderr.write("Erro de sintaxe. '=' esperado. (3)")
            sys.exit(1)
            
    def parseStatementList(tok):
        resultado = []
        while tok.next is not None:
            resultado.append(Parser.parseStatement(tok))
        return resultado

    def parseBlock(tok):
        saida = []
        while tok.next is not None:
            saida = Parser.parseStatementList(tok)
        return Block(saida)

    def run(code):
        code_filtrado = PrePro.filter(code=code)
        tokenizer = Tokenizer(code_filtrado, 0, None)
        ast = Parser.parseBlock(tokenizer)
        st = SymbolTable()
        resultado = ast.evaluate(st)
        if tokenizer.next is not None:
            sys.stderr.write("Erro de sintaxe. EOF esperado. (2)")
            sys.exit(1)
        else:
            sys.stdout.write(str(resultado))
            return resultado


class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def set(self, key, value):
        self.table[key] = value
    
    def get(self, key):
        if key not in self.table:
            sys.stderr.write("Erro: GET de variável não existente.")
            sys.exit(1)
        else:
            return self.table[key]

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