import sys
import re

def is_number(x):
    try:
        int(x)
        return True
    except:
        return False

def is_operator(x):
    return x in ['+', '-', '*', '/']

tabela = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y }

def calculadora(equacao):
    # split the string by operators
    equacao = re.split(r'(\+|\-|\*|\/)', equacao)

    if len(equacao) < 3 or len(equacao) % 2 == 0:
        raise ValueError('A equação está errada')
        sys.stderr.write("A equação está errada")

    if is_number(equacao[0]):
        valor = int(equacao[0])
    else:
        raise TypeError('A equação deve começar com um número')
        sys.stderr.write("A equação está errada")

    for i in range(1, len(equacao)):
        if is_operator(equacao[i]):
            if i % 2 != 0:
                operador = equacao[i]
            else:
                raise ValueError('A equação está errada')
                sys.stderr.write("A equação está errada")
        
        elif is_number(equacao[i]):
            if i % 2 == 0:
                valor = tabela[operador](valor, int(equacao[i]))
            else:
                raise ValueError('A equação está errada')
                sys.stderr.write("A equação está errada")
        else:
            raise ValueError('A equação está errada')
            sys.stderr.write("A equação está errada")
    
    sys.stdout.write(str(valor))

if __name__ == '__main__':
    calculadora(sys.argv[1])