Projeto de Iniciação Científica — SOFTWARE DIDÁTICO PARA UNIFICAÇÃO DE PREDICADOS EM LÓGICA PARA COMPUTAÇÃO

Este repositório contém o desenvolvimento de uma aplicação web criada no contexto de um Projeto de Iniciação Científica, utilizando Python e Flask.

O objetivo da aplicação é apresentar conteúdos teóricos de forma didática e permitir que o usuário interaja com exercícios práticos, recebendo uma resposta explicativa gerada a partir das entradas fornecidas.


Objetivo do Projeto

O projeto tem como objetivos principais:

- Desenvolver uma interface web simples para apoio ao aprendizado;
- Separar conteúdo teórico de exercícios interativos;
- Utilizar código Python para processar entradas do usuário e gerar o passo a passo do exercício;

Estrutura da Aplicação

A aplicação possui duas páginas principais:

- Conteúdo: página destinada à explicação teórica do tema abordado;
- Exercícios: página interativa onde o usuário insere dados e recebe uma resposta explicativa.

Tecnologias Utilizadas

- Python 3
- Flask
- HTML5
- CSS3
- Git / GitHub


Estrutura do Repositório

```text
.
├── flaskr/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── conteudo.html
│   │   └── exercicios.html
│   └── static/
│       ├── style.css
│       └── images/
│
├── functions/
│   └── (funções auxiliares e lógica do projeto)
│
├── main.py
├── run.py
├── input.txt
├── output.txt
├── in.txt
├── .gitignore
└── README.md
