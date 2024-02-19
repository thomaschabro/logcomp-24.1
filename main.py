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
        resultado = 0
        tokenAtual = self.tokenizer.selectNext() 
        if tokenAtual.type == "NUMBER":
            resultado = int(tokenAtual.value)
            tokenAtual = self.tokenizer.selectNext()
            while (tokenAtual.type == "PLUS" or tokenAtual.type == "MINUS"):
                if tokenAtual.type == "PLUS":
                    tokenAtual = self.tokenizer.selectNext()
                    if tokenAtual.type == "NUMBER":
                        resultado += int(tokenAtual.value)
                        tokenAtual = self.tokenizer.selectNext()
                    else:
                        raise Exception("Erro de sintaxe. Número esperado.")
                elif tokenAtual.type == "MINUS":
                    tokenAtual = self.tokenizer.selectNext()
                    if tokenAtual.type == "NUMBER":
                        resultado -= int(tokenAtual.value)
                        tokenAtual = self.tokenizer.selectNext()
                    else:
                        raise Exception("Erro de sintaxe. Número esperado.")
            if tokenAtual.type == "EOF":
                return resultado
            else:
                raise Exception("Erro de sintaxe. Fim do arquivo esperado.")
        else:
            raise Exception("Erro de sintaxe. Número esperado.")

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
        print(Parser.run(sys.argv[1]))

if __name__ == "__main__":
    main()