from flask import Blueprint, render_template, request
from functions.unify import unify
from functions.parsing import remove
from functions.erros import *

bp = Blueprint("routes", __name__)

@bp.route("/exercicios")
def exercicios():
    return render_template("exercicios.html")


@bp.route("/resultado", methods=["POST"])
def resultado():
    pred1 = request.form.get("pred1")
    pred2 = request.form.get("pred2")

    function1, function2 = "", ""
    try:
        function1, literal1 = remove(pred1)
        function2, literal2 = remove(pred2)

        result = unify(literal1, literal2, pred1_name=function1, pred2_name=function2)

        if result is None:
            raise ErroDeLoop("Os termos não são unificavéis, erro de loop de substituições")

        return render_template(
            "resultado.html",
            tabela=result["table"],
            function1=function1,
            function2=function2
        )
    except Exception as e:
        table_data = getattr(e, "table", [])
        return render_template(
            "resultado.html",
            tabela=table_data,
            erro=str(e),
            function1=function1,
            function2=function2
        )