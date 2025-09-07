import re
from functions.erros import *

def remove(literal):
    """Remove variáveis de um literal, retornando apenas a parte fixa."""
    match = re.match(r'(\w+)\s*\((.*)\)', literal) 
    if match:
        re_args = match.group(2) #group(2) contém os argumentos da função
        temp = ''
        termos = []
        lendoFunc = 0
        for caractere in re_args:
            if caractere == ',':
                if lendoFunc == 0:
                    termos.append(temp.strip())
                    temp = ''
                else:
                    temp += caractere
            elif caractere == '(':
                lendoFunc += 1
                temp += caractere
            elif caractere == ')':
                lendoFunc -= 1
                temp += caractere
            else:
                temp += caractere
        termos.append(temp.strip())  # Adiciona o último argumento
        if lendoFunc != 0:
            raise ErroDeFormatacao("Formatação errada! Termos não unificáveis. Parênteses não fechados.")
        return termos
    raise ErroDeFormatacao("Formatação errada! Termos não unificáveis.")

