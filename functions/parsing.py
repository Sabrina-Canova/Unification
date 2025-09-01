import re
from functions.erros import ErroDeFormatacao

def remove(literal: str):
    # Extrai o nome do predicado e a lista de argumentos/termos, validando a formatação

    # Valida se a entrada é uma string válida e não vazia
    if not literal or not isinstance(literal, str):
        raise ErroDeFormatacao("Formatação errada! Literal vazio.")

    literal = literal.strip()

    # Expressão regular para isolar o nome do predicado e o conteúdo entre parênteses
    match = re.match(r'^(\w+)\s*\((.*)\)$', literal)
    if not match:
        raise ErroDeFormatacao("Formatação errada! Termos não unificáveis.")

    pred_name, re_args = match.group(1), match.group(2)
    temp = ''
    terms: list[str] = []
    reading_func = 0  # Contador de profundidade de parênteses aninhados

    # Itera sobre os caracteres dos argumentos separando por vírgula no nível 0
    for char in re_args:
        if char == ',':
            if reading_func == 0:
                # Vírgula no nível mais externo
                if not temp.strip():
                    raise ErroDeFormatacao("Formatação errada! Argumento vazio.")
                terms.append(temp.strip())
                temp = ''
            else:
                # Vírgula dentro de parênteses aninhados
                temp += char
        elif char == '(':
            reading_func += 1
            temp += char
        elif char == ')':
            reading_func -= 1
            # Se negativo, há parênteses fechados a mais
            if reading_func < 0:
                raise ErroDeFormatacao("Formatação errada! Termos não unificáveis. Parênteses não balanceados.")
            temp += char
        else:
            temp += char

    # Valida e adiciona o último argumento após a última vírgula
    if not temp.strip():
        raise ErroDeFormatacao("Formatação errada! Argumento vazio.")
    terms.append(temp.strip())

    # Se a profundidade final não for zero, há parênteses abertos que não foram fechados
    if reading_func != 0:
        raise ErroDeFormatacao("Formatação errada! Termos não unificáveis. Parênteses não fechados.")

    return pred_name, terms
