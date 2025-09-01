# UM SOFTWARE DIDÁTICO PARA O ENSINO DE UNIFICAÇÃO DE PREDICADOS EM LÓGICA PARA COMPUTAÇÃO

Software didático para demonstração e resolução passo a passo do algoritmo de unificação de predicados, desenvolvido em Python como parte de Trabalho de Conclusão de Curso (TCC).



## Pré-requisitos

- Python 3.10 ou superior
- `pip`

## Instalação

1. Clone o repositório.

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```


## Como Rodar a Aplicação

Inicie o servidor de desenvolvimento:

```bash
python run.py
```

Abra o navegador e acesse:
```
http://localhost:5000/exercicios
```


## Como Rodar os Testes

Para executar os testes unitários automatizados com o `pytest`:

```bash
python -m pytest -v
```

## Estrutura do Projeto

```text
├── flaskr/               # Camada web 
├── functions/            # Núcleo lógico 
│   ├── erros.py          # Exceções customizadas
│   ├── parsing.py        # Validação sintática e extração de termos
│   ├── unify.py          # Algoritmo de Robinson e tabela de passos
│   └── utils.py          # Occurs check e substituição de termos
├── tests/                # Testes unitários 
│   ├── conftest.py       # Configuração de caminhos para os testes
│   ├── test_parser.py    # Testes de validação de entrada
│   └── test_unificacao.py# Testes dos casos de unificação
└── run.py                # Ponto de entrada do servidor Flask
```
