from functions.unify import unify
from functions.parsing import remove
from functions.test import test_unification

#test_unification('input.txt', 'output.txt')

# Termos a serem unificados
#L1 = "p(x, f(y))"
#L2 = "p(f(a), f(g(b)))"
#L1 = "t(u, v, v)"
#L2 = "t(f(a), f(b), x)"
L1 = "k(f(a,c),c)"  
L2 = "k(x,y)"
#L1 = "q(f(x), x)"
#L2 = "q(y, g(y))"
#L1 = "m(x, x, j)"
#L2 = "m(g(y), y)"
#L1 = "p(f(x))"
#L2 = "p(x)"
#L1 = "p(f(g(x)), w, k)"
#L2 = "p(w, z, g(w))"
#L1 = "p(f(x), y, x)"
#L2 = "p(z, g(z), w)"
#L1 = "m(x, x)"
#L2 = "m(y, g(y))"
#L1 = "s(f(x), x, z)"
#L2 = "s(y, y, g(a))"

# Separando os argumentos dos predicados
literal1 = remove(L1)
literal2 = remove(L2)

# Verifica se os termos são válidos para unificação
if literal1 is None or literal2 is None:
    print("Erro ao processar os termos.")
elif len(literal1) != len(literal2): 
    print("Os termos nao sao unificaveis. Eles possuem diferentes numeros de argumentos. literal1 tem", len(literal1), "argumentos e literal2 tem", len(literal2), "argumentos.")
    print(f"Termos: {literal1} e {literal2}")
else:
    result = unify(literal1, literal2)

    if result is None:
        print("Os termos nao sao unificaveis!")
        ###Fzr mostrar as subs q n deram certo. Talvez criar um arquivo só para printar os erros###
        #for i in range(len(literal1)):
         #   if literal1[i] != literal2[i]:
          #      print(f"Termos que causaram a falha: {literal1[i]} -> {literal2[i]}")
    else: 
        print("\nSubstituicoes encontradas:")
        for var, val in result.items():
            print(f"{var} -> {val}")



