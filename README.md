# Supervelha-SPA

python -m pip install Django
python -m pip install mysqlclient
Python 3.x.x
MySql Server 8.0.x

python manage.py migrate
python manage.py runserver

## Padrão utilizado: <a href="https://refactoring.guru/pt-br/design-patterns/strategy" target="_blank">Strategy</a>
Se encontra no método "verificar_respostas" na pasta de questionário, em views.py. A implementação do Strategy em sí está ná pasta "<a href="https://github.com/virocha11/Supervelha-SPA/tree/main/back_end/questionario/padrao_projeto" target="_blank">padrao_projeto</a>", dentro da pasta questionário, em "<a href="https://github.com/virocha11/Supervelha-SPA/blob/main/back_end/questionario/padrao_projeto/strategies.py" target="_blank">strategies.py</a>".

Com o strategy, podemos encapsular as diferentes partes do método (verificação se é ou não um professor e o que cada possibilidade acarretaria) em classes diferentes, fazendo com que o comportamento de um objeto varie dependendo da estratégia que está sendo chamada para a implementação de um método, tornando o código mais flexível.
Antes de aplicar o padrão Strategy, "verificar_respostas" era implementado diretamente na views.py e tinha uma lógica bem sedimentada, tornando difícil a manutenção caso se, por exemplo, no futuro, adicionássemos mais algum usuário que fosse capaz de verificar as respostas de um questionário que senão o professor, ou outros tipos de verificação.
