# Exceções customizadas para o processo de unificação e análise sintática.

class ErroDeFormatacao(Exception):
    # Lançada quando a sintaxe do literal de entrada é inválida.
    pass


class TamanhoDiferente(Exception):
    # Lançada quando há disparidade na aridade (número de argumentos).
    pass


class PredicadosDiferentes(Exception):
    # Lançada quando os símbolos dos predicados raiz são diferentes.
    pass


class ErroDeLoop(Exception):
    # Lançada quando ocorre falha no Occurs Check.
    pass
