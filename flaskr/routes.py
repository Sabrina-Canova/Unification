from flask import Blueprint, render_template, request
from functions.unify import unify
from functions.parsing import remove
from functions.erros import *

bp = Blueprint("routes", __name__)

@bp.route("/")
def conteudo():
    return render_template("conteudo.html")

@bp.route("/exercicios")
def exercicios():
    return render_template("exercicios.html")


@bp.route("/resultado", methods=["POST"])
def resultado():
    pred1 = request.form.get("pred1")
    pred2 = request.form.get("pred2")

    try:
        function1, literal1 = remove(pred1)
        function2, literal2 = remove(pred2)

        resultado = unify(literal1, literal2)

        if resultado is None:
            raise ErroDeLoop("Os termos não são unificavéis, erro de loop de substituições")

        return render_template(
            "resultado.html",
            tabela=resultado["tabela"],
            function1=function1,
            function2=function2
        )
    except Exception as e:
        return render_template(
            "resultado.html",
            tabela=[],
            erro=str(e)
        )