import sys
from abc import abstractmethod

saida_asm = []

label_index = 0

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
        self.if_index = 0
        self.while_index = 0

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
        self.children[1].Evaluate(st)
        saida_asm.append("PUSH EAX")
        self.children[0].Evaluate(st)
        saida_asm.append("POP EBX")

        if self.value == "+":
            saida_asm.append("ADD EAX, EBX")
        elif self.value == "-":
            saida_asm.append("SUB EAX, EBX")
        elif self.value == "*":
            saida_asm.append("IMUL EBX")
        elif self.value == "/":
            saida_asm.append("IDIV EBX")
        elif self.value == "and":
            saida_asm.append("AND EAX, EBX")
        elif self.value == "or":
            saida_asm.append("OR EAX, EBX")
        elif self.value == "<":
            saida_asm.append("CMP EAX, EBX")
            saida_asm.append("CALL binop_jl")
        elif self.value == ">":
            saida_asm.append("CMP EAX, EBX")
            saida_asm.append("CALL binop_jg")
        elif self.value == "==":
            saida_asm.append("CMP EAX, EBX")
            saida_asm.append("CALL binop_je")
        else:
            sys.stderr.write("Tipo da operação inválido. -> BINOP")
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
        saida_asm.append("MOV EAX, " + str(self.value))

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
        resultado = ""
        for child in self.children:
            if child != None:
                resultado += str(child.Evaluate(st))

        return resultado

class Identifier(Node):
    def _init_(self, value):
        super()._init_(value, [])

    def Evaluate(self, st):
        saida_asm.append("MOV EAX, [EBP-" + str(st.get(self.value)) + "] ;")

class Assign(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        self.children[1].Evaluate(st)
        value = st.get(self.children[0].value)
        saida_asm.append("MOV [EBP-" + str(value) + "], EAX ;")

class VarDec(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        if self.children[1] is not None:
            sys.stderr.write("Tipo dos operadores inválido.")
            sys.exit(1)
            return
        else:
            st.create(self.children[0].value)
            saida_asm.append("PUSH DWORD 0 ;")

class FuncDec(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        pass

class Print(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        self.children[0].Evaluate(st)
        saida_asm.append("PUSH EAX")
        saida_asm.append("PUSH formatout")
        saida_asm.append("CALL printf")
        saida_asm.append("ADD ESP, 8")

class If(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        global label_index
        label_index += 1

        saida_asm.append("IF_" + str(label_index) + ":")
        self.children[0].Evaluate(st)
        saida_asm.append("CMP EAX, False")
        saida_asm.append("JE ELSE_" + str(label_index))
        if self.children[1] is not None:
            self.children[1].Evaluate(st)
        saida_asm.append("JMP ENDIF_" + str(label_index))
        saida_asm.append("ELSE_" + str(label_index) + ":")
        if len(self.children) == 3:
            self.children[2].Evaluate(st)
        saida_asm.append("ENDIF_" + str(label_index) + ":")

class While(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        global label_index
        label_index += 1

        saida_asm.append("LOOP_" + str(label_index) + ":")
        # Executa a condição
        self.children[0].Evaluate(st)
        saida_asm.append("CMP EAX, False")
        saida_asm.append("JE END_" + str(label_index))
        # Executa o bloco
        for child in self.children[1]:
            child.Evaluate(st)
        saida_asm.append("JMP LOOP_" + str(label_index))
        saida_asm.append("END_" + str(label_index) + ":")

class Read(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st):
        saida_asm.append("PUSH scanint")
        saida_asm.append("PUSH formatin")
        saida_asm.append("call scanf")
        saida_asm.append("ADD ESP, 8")
        saida_asm.append("MOV EAX, DWORD [scanint]")

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
            bloco1 = None
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
            else:
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
            whi =  While(value="while", children=[condicao, lista_statements])
            return whi
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
            sys.stderr.write("Erro de sintaxe. Comando inválido. (15)")
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
        self.size = 0

    # def set(self, key, value, type):
    #     if key in self.table:
    #         self.table[key] = [value, type, self.table[key][2]]
    #     else:
    #         sys.stderr.write("Variável sendo definida sem ser declarada [ " + key + " ]")
    #         sys.exit(1)

    def get(self, key):
        return self.table[key]

    def create(self, key):
        if key not in self.table:
            self.size += 4
            self.table[key] = self.size
        else:
            sys.stderr.write("Variável sendo redefinida [ " + key + " ]")
            sys.exit(1)

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

        nome_inteiro = sys.argv[1]
        file = nome_inteiro[:-4]
        with open(str(file) + ".asm", "w") as f:
            f.write('; constantes\n')
            f.write('SYS_EXIT equ 1\n')
            f.write('SYS_READ equ 3\n')
            f.write('SYS_WRITE equ 4\n')
            f.write('STDIN equ 0\n')
            f.write('STDOUT equ 1\n')
            f.write('True equ 1\n')
            f.write('False equ 0\n')
            f.write('segment .data\n')
            f.write('formatin: db "%d", 0\n')
            f.write('formatout: db "%d", 10, 0 ; newline, nul terminator\n')
            f.write('scanint: times 4 db 0 ; 32-bits integer = 4 bytes\n')
            f.write('segment .bss  ; variaveis\n')
            f.write('res RESB 1\n')
            f.write('section .text\n')
            f.write('global main ; linux\n')
            f.write(';global _main ; windows\n')
            f.write('extern scanf ; linux\n')
            f.write('extern printf ; linux\n')
            f.write(';extern _scanf ; windows\n')
            f.write(';extern _printf; windows\n')
            f.write('extern fflush ; linux\n')
            f.write(';extern _fflush ; windows\n')
            f.write('extern stdout ; linux\n')
            f.write(';extern _stdout ; windows\n')
            f.write('; subrotinas if/while\n')
            f.write('binop_je:\n')
            f.write('JE binop_true\n')
            f.write('JMP binop_false\n')
            f.write('binop_jg:\n')
            f.write('JG binop_true\n')
            f.write('JMP binop_false\n')
            f.write('binop_jl:\n')
            f.write('JL binop_true\n')
            f.write('JMP binop_false\n')
            f.write('binop_false:\n')
            f.write('MOV EAX, False  \n')
            f.write('JMP binop_exit\n')
            f.write('binop_true:\n')
            f.write('MOV EAX, True\n')
            f.write('binop_exit:\n')
            f.write('RET\n')
            f.write('main:\n')
            f.write('PUSH EBP ; guarda o base pointer\n')
            f.write('MOV EBP, ESP ; estabelece um novo base pointer\n\n')
            f.write('; codigo gerado pelo compilador abaixo\n\n')

            i = 0
            while i < len(saida_asm):
                if i == (len(saida_asm) - 1):
                    f.write(saida_asm[i])
                else:
                    f.write(saida_asm[i] + "\n")
                i+=1


            f.write('\n\n; interrupcao de saida (default)\n\n')
            f.write('PUSH DWORD [stdout]\n')
            f.write('CALL fflush\n')
            f.write('ADD ESP, 4\n')
            f.write('MOV ESP, EBP\n')
            f.write('POP EBP\n')
            f.write('MOV EAX, 1\n')
            f.write('XOR EBX, EBX\n')
            f.write('INT 0x80\n')

if __name__ == "__main__":
    main()