import sys

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
class Tokenizer:
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next
    
    def selectNext(self):
        if self.position < len(self.source):
            if self.source[self.position] == "+":
                self.position += 1
                return Token("PLUS", "+")
            elif self.source[self.position] == "-":
                self.position += 1
                return Token("MINUS", "-")
            elif self.source[self.position] == "*":
                self.position +=1
                return Token("TIMES", "*")
            elif self.source[self.position] == "/":
                self.position +=1
                return Token("DIV", "/")
            elif self.source[self.position].isdigit():
                number = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    number += self.source[self.position]
                    self.position += 1
                return Token("NUMBER", number)
            elif self.source[self.position] == " ":
                self.position += 1
                return self.selectNext()

        else:
            return Token("EOF", None)

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def parseExpression(self):
        tokenAtual = self.tokenizer.selectNext()
        resultado, tokenAtual = Parser.parseTerm(self, tokenAtual)

        while (1):
            if tokenAtual.type == "PLUS":
                tokenAtual = self.tokenizer.selectNext()
                if tokenAtual.type == "NUMBER":
                    numero, tokenAtual = Parser.parseTerm(self, tokenAtual)
                    resultado += int(numero)
                else:
                    sys.stderr.write("Erro de sintaxe. Número esperado. (1)")
            elif tokenAtual.type == "MINUS":
                tokenAtual = self.tokenizer.selectNext()
                if tokenAtual.type == "NUMBER":
                    numero, tokenAtual = Parser.parseTerm(self, tokenAtual)
                    resultado -= int(numero)
                else:
                    sys.stderr.write("Erro de sintaxe. Número esperado. (2)")
            elif tokenAtual.type == "EOF":
                sys.stdout.write(str(int(resultado)))
                return resultado
            else:
                sys.stderr.write("Erro de sintaxe. Operador esperado. (3)") 

    def parseTerm(self, tokenAtual):
        resultado = 0
        if tokenAtual.type == "NUMBER":
            resultado = int(tokenAtual.value)
            while (1):
                tokenAtual = self.tokenizer.selectNext()
                if tokenAtual.type == "TIMES":
                    tokenAtual = self.tokenizer.selectNext()
                    if tokenAtual.type == "NUMBER":
                        resultado *= int(tokenAtual.value)
                    else:
                        sys.stderr.write("Erro de sintaxe. Número esperado. (4)")
                elif tokenAtual.type == "DIV":
                    tokenAtual = self.tokenizer.selectNext()
                    if tokenAtual.type == "NUMBER":
                        resultado /= int(tokenAtual.value)
                    else:
                        sys.stderr.write("Erro de sintaxe. Número esperado. (5)")
                elif tokenAtual.type == "NUMBER":
                    sys.stderr.write("Erro de sintaxe. Operador esperado. (6)")
                else:
                    return resultado, tokenAtual
        else:
            sys.stderr.write("Erro de sintaxe. Número esperado. (7)")

    def run(code):
        tokenizer = Tokenizer(code, 0, None)
        parser = Parser(tokenizer)
        return parser.parseExpression()         

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <expressão>")
        print("  |-> EXEMPLO: python main.py '1+2-3'")
        return
    else:
        Parser.run(sys.argv[1])

if __name__ == "__main__":
    main()