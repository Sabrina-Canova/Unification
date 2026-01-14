from flask import Blueprint, render_template, request
from functions.unify import unify

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
        # sua função unify PRECISA retornar tabela e substituições depois
        resultado = unify(pred1, pred2)

        return render_template(
            "resultado.html",
            tabela=resultado,
            erro=None
        )
    except Exception as e:
        return render_template(
            "resultado.html",
            tabela=None,
            erro=str(e)
        )
