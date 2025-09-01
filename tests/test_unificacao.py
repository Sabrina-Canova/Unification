import pytest
from functions.unify import unify
from functions.erros import PredicadosDiferentes, TamanhoDiferente, ErroDeLoop

casos_sucesso = [
    ("caso_01", "p(x,y)", "p(a,b)", {"x": "a", "y": "b"}),
    ("caso_02", "p(x,f(y))", "p(f(a),f(g(b)))", {"x": "f(a)", "y": "g(b)"}),
    ("caso_03", "p(x,x)", "p(a,a)", {"x": "a"}),
    ("caso_04", "t(u,v,v)", "t(f(a),f(b),x)", {"u": "f(a)", "v": "f(b)", "x": "f(b)"}),
    ("caso_05", "p(g(h(x)))", "p(g(h(y)))", {"x": "y"}),
    ("caso_06", "p(f(x),y)", "p(y,f(x))", {"y": "f(x)"}),
    ("caso_07", "p(x,f(x,g(x,h(x))))", "p(a,f(a,g(a,h(a))))", {"x": "a"}),
    ("caso_08", "r(f(g(h(i(j(x))))))", "r(f(g(h(i(j(a))))))", {"x": "a"}),
    ("caso_09", "w(f(g(h(i(x),y),z)))", "w(f(g(h(i(a),b),c)))", {"x": "a", "y": "b", "z": "c"}),
    ("caso_10", "m(x,y)", "m(f(y),y)", {"x": "f(y)"}),
    ("caso_15", "p(a,b,c,x)", "p(d,f(a),g(b),f(g(c)))", {"a": "d", "b": "f(d)", "c": "g(f(d))", "x": "f(g(g(f(d))))"}),
]

@pytest.mark.parametrize("nome, l1, l2, esperado", casos_sucesso, ids=[c[0] for c in casos_sucesso])
def test_unificacao_sucesso(nome, l1, l2, esperado):
    res = unify(l1, l2)
    assert res["sucesso"] is True
    assert res["substituicoes"] == esperado

casos_falha = [
    ("caso_11", "p(x)", "q(x)", PredicadosDiferentes),
    ("caso_12", "m(x,x,j)", "m(g(y),y)", TamanhoDiferente),
    ("caso_13", "q(f(a,b))", "q(f(a))", TamanhoDiferente),
    ("caso_14", "r(f(g(x)))", "r(f(h(x)))", TamanhoDiferente),
    ("caso_16", "p(a)", "p(f(a))", ErroDeLoop),
    ("caso_17", "p(x,x)", "p(f(c),g(c))", TamanhoDiferente),
    ("caso_18", "p(f(x))", "p(x)", ErroDeLoop),
    ("caso_19", "q(f(x),x)", "q(y,g(y))", ErroDeLoop),
    ("caso_20", "m(x,x)", "m(y,g(y))", ErroDeLoop),
]

@pytest.mark.parametrize("nome, l1, l2, erro_esperado", casos_falha, ids=[c[0] for c in casos_falha])
def test_unificacao_falha(nome, l1, l2, erro_esperado):
    with pytest.raises(erro_esperado):
        unify(l1, l2)


def test_tabela_passos_caso_01():
    res = unify("p(x,y)", "p(a,b)")
    tabela = res["table"]
    
    assert len(tabela) == 3
    assert tabela[0]["dk"] == "{x,a}"
    assert tabela[1]["dk"] == "{y,b}"
    assert tabela[2]["dk"] == ""
