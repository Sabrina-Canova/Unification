import re
from functions.utils import occurs_check, apply_substitutions
from tabulate import tabulate  # Biblioteca para formatar a tabela
from functions.erros import *


def unify(literal1, literal2):
    """Tenta unificar dois termos e exibe o processo passo a passo como uma tabela."""
    
    subst = {}  # Dicionário de substituições
    tabela = []  # Matriz para armazenar as etapas da unificação

    if len(literal1) != len(literal2):
        raise TamanhoDiferente("Número de argumentos diferentes")
    
    for termo1, termo2 in zip(literal1, literal2):
        
        # Aplica substituições anteriores
        while termo1 in subst:
            termo1 = subst[termo1]
        while termo2 in subst:
            termo2 = subst[termo2]

        # Se os termos já são iguais, não há necessidade de substituição
        if termo1 == termo2:
            continue

        # Caso 1: termo1 é uma variável
        if re.match(r"^[a-zA-Z_]\w*$", termo1) and not re.match(r"^\w+\(.*\)$", termo1):
            if occurs_check(termo1, termo2, subst):
                return None  # Evita loops como x -> f(x)
            subst[termo1] = apply_substitutions(termo2, subst)

        # Caso 2: termo2 é uma variável
        elif re.match(r"^[a-zA-Z_]\w*$", termo2) and not re.match(r"^\w+\(.*\)$", termo2):
            if occurs_check(termo2, termo1, subst):
                return None  # Evita loops como x -> f(x)
            subst[termo2] = apply_substitutions(termo1, subst)

        # Caso 3: ambos são funções/termos complexos
        else:
            match1 = re.match(r'(\w+)\((.*)\)', termo1)
            match2 = re.match(r'(\w+)\((.*)\)', termo2)

            if not match1 or not match2:
                return None

            func1, args1 = match1.group(1), [a.strip() for a in match1.group(2).split(',')]
            func2, args2 = match2.group(1), [a.strip() for a in match2.group(2).split(',')]

                # nomes das funções diferentes -> falha
            if func1 != func2 or len(args1) != len(args2):
                raise TamanhoDiferente("Funcoes diferentes ou numero de argumentos diferente")

                # recursivamente unificar cada par de argumentos
            for a1, a2 in zip(args1, args2):
                resultado = unify([a1], [a2])
                if resultado is None:
                        return None 
                subst.update(resultado["substituicoes"])

            #algumas alterações para o flask
            tabela.append({
                "theta": dict(subst),
                "l1": apply_substitutions(" ".join(literal1), subst),
                "l2": apply_substitutions(" ".join(literal2), subst),
                "dk": f"{{{termo1},{termo2}}}"
            })

    return{
        "sucesso" : True,
        "substituicoes": subst,
        "tabela": tabela
    }
            #else:
                #return None  # um é função, outro não -> falha

        # Aplicando as substituições nos literais antes de exibir
        #L1_aplicado = apply_substitutions(" ".join(literal1), subst)
        #L2_aplicado = apply_substitutions(" ".join(literal2), subst)
        #tabela.append([str(subst), L1_aplicado, L2_aplicado, f"{{{termo1}, {termo2}}}"])

    # Exibir a tabela formatada
    #if tabela:
    #    print(tabulate(tabela, headers=["Theta_k", "L1Theta_k", "L2Theta_k", "Dk"], tablefmt="grid"))
    #print("Termos unificados:")
   # print(f"p({tabela[-1][1].replace(' ', ',')})")
    #return subst  # Retorna as substituições finais

