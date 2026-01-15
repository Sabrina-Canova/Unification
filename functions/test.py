from functions.unify import unify
from functions.parsing import remove
from functions.erros import *

def test_unification(linhas):
    resultados = []

    
    for i, linha in enumerate(linhas, 1):
        linha = linha.strip()

        if ';' not in linha:
            resultados.append({
                    "Exercicio": i,
                    "Erro":"Formato inválido, esperado 'L1; L2'."
            })
            continue
        
        L1, L2 = linha.split(';', 1)
        
        try:   
            literal1 = remove(L1.strip())
            literal2 = remove(L2.strip())
        except ErroDeFormatacao as e:
            resultados.append({
                "Exercício": i,
                "erro": str(e)
                })
            continue

    
        #print(f"literal1: {literal1}")
        #print(f"literal2: {literal2}")

        try:
            resultado = unify(literal1, literal2)
        except TamanhoDiferente as e:
            resultados.append({
                "Exercício": i,
                "erro": str(e)
                })
            continue

        
        if resultado is None:
                resultados.append({
                "Exercício": i,
                "erro": "Os termos não são unificáveis (loop de substituições)"
                })
        else:
            subst = [
                {"var" : var, "valor": val }
                for var, val in resultado.items()
            ]
            resultados.append({
                "exercicio": i,
                "sucesso": True,
                "substituicoes": subst
            })

    return resultados
