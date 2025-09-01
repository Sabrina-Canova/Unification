import re

def normalize_term(term: str) -> str:
    # Padroniza o espaçamento em termos lógicos, removendo espaços redundantes
    if not term:
        return term
    s = re.sub(r'\s*([(),])\s*', r'\1', term.strip())
    return re.sub(r',', ', ', s)


def split_arguments(args_str: str) -> list[str]:
   # Separa argumentos delimitados por vírgula, respeitando e preservando parênteses aninhados de funções internas.
    
    args = []
    temp = ''
    depth = 0  # Controla a profundidade dos parênteses

    for char in args_str:
        if char == ',' and depth == 0:
            # Vírgula encontrada fora de qualquer par de parênteses
            args.append(normalize_term(temp))
            temp = ''
        else:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            temp += char

    if temp.strip():
        args.append(normalize_term(temp))

    return args


def parse_compound_term(term: str):
    # Reconhece se o termo é uma função composta válida
    term = normalize_term(term)

    # Identifica o padrão nome_da_funcao(conteudo_dos_argumentos)
    match = re.match(r'^(\w+)\s*\((.*)\)$', term)
    if not match:
        return None

    functor, inner = match.group(1), match.group(2)

    # Validação do balanceamento de parênteses no conteúdo interno
    depth = 0
    for char in inner:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth < 0:
                return None
    if depth != 0:
        return None

    return functor, split_arguments(inner)


def is_variable(term: str) -> bool:
    # Determina se um termo é uma variável
    return '(' not in term and ')' not in term


def find_disagreement(t1: str, t2: str):
    # Encontra o primeiro par de subtermos discordantes entre t1 e t2

    t1 = normalize_term(t1)
    t2 = normalize_term(t2)
    if t1 == t2:
        return None

    parsed1 = parse_compound_term(t1)
    parsed2 = parse_compound_term(t2)

    # Se ambos são termos compostos
    if parsed1 and parsed2:
        symbol1, args1 = parsed1
        symbol2, args2 = parsed2
        # Se possuem o mesmo símbolo e mesma quantidade de argumentos
        if symbol1 == symbol2 and len(args1) == len(args2):
            for a1, a2 in zip(args1, args2):
                diff = find_disagreement(a1, a2)
                if diff is not None:
                    return diff

    # Ponto de discordância encontrado
    return (t1, t2)


def _var_pattern(var: str) -> str:
    # Constrói regex seguro para casar a variável como identificador isolado
    return rf"(?<!\w){re.escape(var)}(?!\w)(?!\s*\()"


def occurs_check(var: str, term: str, subst: dict) -> bool:
    # Verifica se a variável 'var' ocorre dentro do termo 'term'
    term = apply_substitutions(term, subst)

    if var == term:
        return True

    return re.search(_var_pattern(var), term) is not None


def apply_substitutions(literal: str, subst: dict) -> str:
    """
    Aplica o conjunto de substituições acumulado (theta) a um literal ou termo.
    Itera recursivamente até ponto fixo para resolver cadeias transitivas.
    Ordena variáveis por tamanho decrescente para evitar substituições parciais de substrings.
    """
    if not subst or not literal:
        return literal

    for _ in range(len(literal) + 5):
        new_literal = literal
        # Substitui os identificadores mais longos primeiro
        for var in sorted(subst.keys(), key=len, reverse=True):
            val = subst[var]
            new_literal = re.sub(_var_pattern(var), lambda _m: val, new_literal)

        # Se nenhuma substituição alterou a string, atingiu ponto fixo
        if new_literal == literal:
            break
        literal = new_literal

    return normalize_term(literal)
