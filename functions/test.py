from functions.unify import unify
from functions.parsing import remove

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
        literal1 = remove(L1)
        literal2 = remove(L2)
        print(f"literal1: {literal1}")
        print(f"literal2: {literal2}")

        if literal1 is None or literal2 is None or len(literal1) != len(literal2):
            resultados.append(f"Exercício {i}: Os termos não são unificáveis! Possuem tamanhos diferentes")
            continue

        resultado = unify(literal1, literal2)
        print("-------------------------")
        print(f"lit1: {literal1}")
        print(f"lit2: {literal2}")
        print("-------------------------")
        if resultado is None:
            resultados.append(f"Exercício {i}: Os termos não são unificáveis! NONE")
        else:
            subst = ", ".join([f"{var} -> {val}" for var, val in resultado.items()])
            resultados.append(f"Exercício {i}: Substituições encontradas: {subst}")

    # Salva os resultados
    with open(saida, 'w', encoding='utf-8') as saida:
        for linha in resultados:
            saida.write(linha + '\n')