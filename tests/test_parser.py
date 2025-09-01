import pytest
from functions.parsing import remove
from functions.erros import ErroDeFormatacao

def test_parsing_predicados_validos():
    pred, termos = remove("p(x)")
    assert pred == "p"
    assert termos == ["x"]

    pred, termos = remove("p(x, y)")
    assert pred == "p"
    assert termos == ["x", "y"]

    pred, termos = remove("q(f(a), g(b))")
    assert pred == "q"
    assert termos == ["f(a)", "g(b)"]


def test_literal_vazio():
    with pytest.raises(ErroDeFormatacao):
        remove("")
    with pytest.raises(ErroDeFormatacao):
        remove("   ")
    with pytest.raises(ErroDeFormatacao):
        remove(None)


def test_parenteses_invalidos():
    # Parênteses não fechados
    with pytest.raises(ErroDeFormatacao):
        remove("p(f(x)")

    # Parênteses fechados a mais
    with pytest.raises(ErroDeFormatacao):
        remove("p(a))")


def test_argumentos_vazios():
    with pytest.raises(ErroDeFormatacao):
        remove("p()")
    with pytest.raises(ErroDeFormatacao):
        remove("p(a,)")
    with pytest.raises(ErroDeFormatacao):
        remove("p(,b)")
