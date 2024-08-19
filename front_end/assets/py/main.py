from urllib import request


@app_route("/cadastro_professor")
def cadastrar_professor():
    nome = request.form.get('nome_prof')
    email = request.form.get('email_prof')
    senha = request.form.get('senha_prof')
    print(f'{nome}')
    print(f'{email}')
    print(f'{senha}')
    return redirect('../paginas/inicio')
