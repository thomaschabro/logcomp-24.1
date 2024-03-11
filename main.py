import sys

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
        if self.position >= len(self.source):
            if self.next.type != "EOF":
                sys.stderr.write("Erro de sintaxe. Fim de expressão inesperado.")
            return

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

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parseExpression(tok):
        resultado = Parser.parseTerm(tok)

        while (1):
            if tok.next.type == "PLUS":
                tok.selectNext()
                numero = Parser.parseTerm(tok)
                resultado += int(numero)
            elif tok.next.type == "MINUS":
                tok.selectNext()
                numero = Parser.parseTerm(tok)
                resultado -= int(numero)
            else:
                return resultado

    def parseTerm(tok):
        resultado = Parser.parseFactor(tok)

        while (1):
            if tok.next.type == "TIMES":
                tok.selectNext()
                numero = Parser.parseFactor(tok)
                resultado *= int(numero)
            elif tok.next.type == "DIV":
                tok.selectNext()
                numero = Parser.parseFactor(tok)
                resultado //= (int(numero))
            else:
                return resultado

    def parseFactor(tok):
        if tok.next.type == "NUMBER":
            numero = tok.next.value
            tok.selectNext()
            if tok.next.type == "NUMBER":
                sys.stderr.write("Erro de sintaxe. Número não esperado. (8)")
            return int(numero)
        elif tok.next.type == "PLUS":
            tok.selectNext()
            numero = Parser.parseFactor(tok)
            return int(numero)
        elif tok.next.type == "MINUS":
            tok.selectNext()
            numero = Parser.parseFactor(tok)
            return -int(numero)    
        elif tok.next.type == "LPAREN":
            tok.selectNext()
            resultado = Parser.parseExpression(tok)
            if tok.next.type != "RPAREN":
                sys.stderr.write("Erro de sintaxe. ')' esperado. (9)")
            else:
                tok.selectNext()
                return resultado
        else:
            sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (10)")
        

    def run(code):
        tokenizer = Tokenizer(code, 0, None)
        tokenizer.selectNext()
        resultado = Parser.parseExpression(tokenizer)
        print(resultado)         

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <expressão>")
        print("  |-> EXEMPLO: python main.py '1+2-3'")
        return
    
    expression = sys.argv[1]
    left, right = 0, 0
    for char in expression:
        if char == '(':
            left += 1
        if char == ')':
            right += 1
    
    if left != right:
        print("Erro: Número de parênteses inválido.")
        sys.stderr.write("Erro de sintaxe. Número de parênteses inválido.")
        return

    else:
        Parser.run(sys.argv[1])

if __name__ == "__main__":
    main()