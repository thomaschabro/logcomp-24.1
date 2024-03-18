import sys
from abc import abstractmethod

class PrePro():
    def filter(self, code):
        i = 0
        while i < len(code):
            if code[i] == "-":
                if code[i+1] == "-":
                    code = code[:i]
                    break
            i += 1
        return code

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
        if self.position < len(self.source):
            if self.source[self.position] == " ":
                while self.position < len(self.source) and self.source[self.position] == " ":
                    self.position += 1
            
            if self.position < len(self.source):
                if self.source[self.position] == "+":
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
                elif self.source[self.position].isdigit():
                    number = ""
                    while self.position < len(self.source) and self.source[self.position].isdigit():
                        number += self.source[self.position]
                        self.position += 1
                    self.next = Token("NUMBER", number)

        else:
            self.next = Token("EOF", None)

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

    def Evaluate(self):
        if self.value == "+":
            return int(self.children[0].Evaluate()) + int(self.children[1].Evaluate())
        elif self.value == "-":
            return int(self.children[0].Evaluate()) - int(self.children[1].Evaluate())
        elif self.value == "*":
            return int(self.children[0].Evaluate()) * int(self.children[1].Evaluate())
        elif self.value == "/":
            return int(self.children[0].Evaluate()) // int(self.children[1].Evaluate())

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self):
        if self.value == "+":
            return int(self.children[0].Evaluate())
        elif self.value == "-":
            return int(-self.children[0].Evaluate())
        
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

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parseExpression(tok):
        tok.selectNext()
        resultado = Parser.parseTerm(tok)

        while (1):
            if tok.next.type == "PLUS":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6)")
                else:
                    resultado = BinOp("+", [resultado, Parser.parseTerm(tok)])
            elif tok.next.type == "MINUS":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6)")
                else:
                    resultado = BinOp("-", [resultado, Parser.parseTerm(tok)])
            else:
                return resultado

    def parseTerm(tok):
        resultado = Parser.parseFactor(tok)

        while (1):
            if tok.next.type == "TIMES":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (7)")
                else:
                    resultado = BinOp("*", [resultado, Parser.parseFactor(tok)])

            elif tok.next.type == "DIV":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS" and tok.next.type != "MINUS":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (7)")
                else:
                    resultado = BinOp("/", [resultado, Parser.parseFactor(tok)])
            else:
                return resultado

    def parseFactor(tok):
        if tok.next.type == "NUMBER":
            numero = tok.next.value
            tok.selectNext()
            return IntVal(numero)
        elif tok.next.type == "PLUS":
            tok.selectNext()
            numero = UnOp("+", [Parser.parseFactor(tok)])
            return numero
        elif tok.next.type == "MINUS":
            tok.selectNext()
            numero = UnOp("-", [Parser.parseFactor(tok)])
            return numero
        elif tok.next.type == "LPAREN":
            resultado = Parser.parseExpression(tok)
            if tok.next.type != "RPAREN":
                sys.stderr.write("Erro de sintaxe. ')' esperado. (9)")
            else:
                tok.selectNext()
                return resultado
        else:
            sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (10)")
        

    def run(code):
        code_filtrado = PrePro().filter(code)
        tokenizer = Tokenizer(code_filtrado, 0, None)
        resultado = Parser.parseExpression(tokenizer)
        resultado = resultado.Evaluate()
        if tokenizer.next.type != "EOF":
            sys.stderr.write("Erro de sintaxe. Fim de arquivo esperado. (11)")
        else:
            print(resultado)

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <file>")
        print("  |-> EXEMPLO: python main.py teste.lua")
        return
    
    file = sys.argv[1]
    if file[-4:] != ".lua":
        print("Erro: Arquivo inválido. Deve ser do tipo .lua")
        sys.stderr.write("Erro: Arquivo inválido. Deve ser do tipo .lua")
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
        return

    else:
        Parser.run(file)

if __name__ == "__main__":
    main()