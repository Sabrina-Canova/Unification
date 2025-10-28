from functions.unify import unify
from functions.parsing import remove
from functions.erros import *

def test_unification(entrada, saida):
    resultados = []
    try:
        with open(entrada, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
    except FileNotFoundError: 
        print(f"Arquivo {entrada} não encontrado.")
        return  
    
    for i, linha in enumerate(linhas, 1):
        linha = linha.strip()
        if ';' not in linha:
            resultados.append(f"Linha {i}: Formato inválido, esperado 'L1; L2'.")
            continue
        
        L1, L2 = linha.split(';', 1)
        try:
            literal1 = remove(L1.strip())
        except ErroDeFormatacao as e:
            resultados.append(f"Exercício {i}: {e} - Problema no Literal 1")
            continue

        try:
            literal2 = remove(L2.strip())
        except ErroDeFormatacao as e:
            resultados.append(f"Exercício {i}: {e} - Problema no Literal 2")
            continue
    
        #print(f"literal1: {literal1}")
        #print(f"literal2: {literal2}")

        try:
            resultado = unify(literal1, literal2)
        except TamanhoDiferente as e:
            resultados.append(f"Exercício {i}: {e}")
            continue

        print("-------------------------")
        print(f"lit1: {literal1}")
        print(f"lit2: {literal2}")
        print("-------------------------")
        try:
            if resultado is None:
                raise ErroDeLoop(f"Exercicio {i}: Os termos não são unificáveis devido a um loop de substituição.")
        except ErroDeLoop as e:
            resultados.append(str(e))
            continue
        else:
            subst = ", ".join([f"{var} -> {val}" for var, val in resultado.items()])
            resultados.append(f"Exercício {i}: Substituições encontradas: {subst}")

    # Salva os resultados
    with open(saida, 'w', encoding='utf-8') as saida:
        for linha in resultados:
            saida.write(linha + '\n')