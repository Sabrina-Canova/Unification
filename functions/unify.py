from functions.utils import occurs_check, apply_substitutions, find_disagreement, is_variable, parse_compound_term, normalize_term
from functions.erros import PredicadosDiferentes, TamanhoDiferente, ErroDeLoop

def unify(literal1: list[str], literal2: list[str], pred1_name=None, pred2_name=None):
    """
    Implementa o Algoritmo de Unificação
    Recebe dois literais e gera o unificador mais geral
    
    Retorna um dicionário contendo:
      - 'success': Booleano indicando se a unificação foi bem-sucedida.
      - 'substitutions': Dicionário com o MGU final {var: valor}.
      - 'table': Histórico completo dos passos para exibição didática (k, theta_k, L1, L2, Dk).
    """
    from functions.parsing import remove

    # Permite chamada direta com strings completas, ex: unify("p(x)", "p(a)")
    if isinstance(literal1, str) and isinstance(literal2, str):
        p1, l1 = remove(literal1)
        p2, l2 = remove(literal2)
        return unify(l1, l2, pred1_name=p1, pred2_name=p2)

    # theta: acumula as substituições mais gerais (MGU)
    subst: dict[str, str] = {}

    # table: armazena cada passo da execução para visualização didática
    table = []

    try:
        # Normaliza espaços em todos os argumentos de entrada
        literal1 = [normalize_term(t) for t in literal1]
        literal2 = [normalize_term(t) for t in literal2]

        # Verifica se os nomes dos predicados principais são idênticos
        if pred1_name and pred2_name and pred1_name != pred2_name:
            table.append({
                "theta": dict(subst),
                "l1": f"({', '.join(literal1)})",
                "l2": f"({', '.join(literal2)})",
                "dk": f"{{{pred1_name},{pred2_name}}}",
                "falha": True,
            })
            exc = PredicadosDiferentes(f"Símbolos de predicados diferentes: '{pred1_name}' e '{pred2_name}'.")
            exc.table = table
            raise exc

        # Verifica se a quantidade de argumentos é igual
        if len(literal1) != len(literal2):
            table.append({
                "theta": dict(subst),
                "l1": f"({', '.join(literal1)})",
                "l2": f"({', '.join(literal2)})",
                "dk": "-",
                "falha": True,
            })
            exc = TamanhoDiferente("Número de argumentos diferentes")
            exc.table = table
            raise exc

        # Loop principal
        while True:
            # Aplica a substituição acumulada
            l1_curr = [apply_substitutions(t, subst).strip() for t in literal1]
            l2_curr = [apply_substitutions(t, subst).strip() for t in literal2]

            # Localiza o primeiro par de termos discordantes
            disagreement = None
            for t1, t2 in zip(l1_curr, l2_curr):
                diff = find_disagreement(t1, t2)
                if diff is not None:
                    disagreement = diff
                    break

            # Se não há desacordo, a unificação terminou com sucesso!
            if disagreement is None:
                table.append({
                    "theta": dict(subst),
                    "l1": f"({', '.join(l1_curr)})",
                    "l2": f"({', '.join(l2_curr)})",
                    "dk": "",
                    "falha": False,
                })
                break

            d1, d2 = disagreement

            # Registra o passo corrente na tabela
            table.append({
                "theta": dict(subst),
                "l1": f"({', '.join(l1_curr)})",
                "l2": f"({', '.join(l2_curr)})",
                "dk": f"{{{d1},{d2}}}",
                "falha": False,
            })

            # Se os termos em D_k forem compostos, verifica símbolo e aridade
            parsed1 = parse_compound_term(d1)
            parsed2 = parse_compound_term(d2)
            if parsed1 and parsed2:
                symbol1, args1 = parsed1
                symbol2, args2 = parsed2
                if symbol1 != symbol2 or len(args1) != len(args2):
                    table[-1]["falha"] = True
                    exc = TamanhoDiferente(f"Termos compostos diferentes ou aridade diferente: '{symbol1}' e '{symbol2}'.")
                    exc.table = table
                    raise exc

            # Identifica qual termo é a variável e qual é o valor da substituição (var <- val)
            if is_variable(d1):
                var, val = d1, d2
            elif is_variable(d2):
                var, val = d2, d1
            else:
                # Nenhum dos dois é variável
                table[-1]["falha"] = True
                exc = TamanhoDiferente(f"Termos não unificáveis: '{d1}' e '{d2}'.")
                exc.table = table
                raise exc

            #  Occurs Check - Evita substituições infinitas
            if occurs_check(var, val, subst):
                table[-1]["falha"] = True
                exc = ErroDeLoop(f"Os termos não são unificáveis, erro de loop de substituições")
                exc.table = table
                raise exc

            # Composição de substituições theta_{k+1} = theta_k o {var <- val}
            # Propaga a nova atribuição em todas as substituições previamente acumuladas
            for k in list(subst.keys()):
                subst[k] = apply_substitutions(subst[k], {var: val})
            subst[var] = normalize_term(val)

        return {
            "sucesso": True,
            "substituicoes": subst,
            "tabela": table,
            "success": True,
            "substitutions": subst,
            "table": table,
        }
    except Exception as exc:
        # Anexa a tabela de passos à exceção para que o frontend possa renderizar onde ocorreu a falha
        if not hasattr(exc, "table"):
            if table:
                table[-1]["falha"] = True
            exc.table = table
        raise exc
