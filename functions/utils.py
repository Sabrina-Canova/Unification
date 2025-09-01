import re

"""Verifica se a var ocorre em term para evitar loops"""
def occurs_check(var, term, subst):
    # Segue substituições até chegar no valor final do termo
    while term in subst:
        term = subst[term]

    # Se var for igual ao termo final 
    if var == term:
        return True
    
    # Se for string, verifica se é um termo com formato nome(arg1, arg2, ...)
    if isinstance(term, str):
        match = re.match(r'(\w+)\s*\((.*)\)', term)
        if match:
            # Separa os argumentos dentro dos parênteses
            args = match.group(2).split(',')
            # Verifica recursivamente se var aparece em algum argumento
            return any(occurs_check(var, arg.strip(), subst) for arg in args)
    
    # Se não encontrou, retorna False
    return False

    

def apply_substitutions(literal, subst): # Aplica a substituição de variáveis em um literal
    for i in range(len(literal)):
       
        novo_literal = literal
        for var, val in subst.items():
            novo_literal = re.sub(rf"\b{var}\b", val, novo_literal) # Substitui var por val apenas se var for uma palavra completa
        if novo_literal == literal:  # Se nada mudou, encerra
            break
        literal = novo_literal
    return literal