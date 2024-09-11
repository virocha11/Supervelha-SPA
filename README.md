
# Supervelha-SPA

### Dependências

<b>Python 3.x.x <br>
MySql Server 8.0.x <br>
</b>

## Comandos: 

### Instalar bibliotecas Django e MySQL 

<div>
<b>python -m pip install Django <br>
python -m pip install mysqlclient <br>
</b>

### Configurar banco de dados

<p>No arquivo /back_end/supervelha/settings.py procurar por "DATABASES", alterando os valores para o seu banco.</p>
<img width="300px" src="https://github.com/virocha11/Supervelha-SPA/blob/main/database.png">
  
### Criar tabelas do banco de dados e executar projeto
<picture><source media="(min-width: 500px)" srcset="https://cdn-icons-png.flaticon.com/128/7207/7207376.png" width="90px" align="right"> <img media="(max-width: 501px)" src="https://cdn-icons-png.flaticon.com/128/7207/7207376.png" width="60px" align="right"  style="margin: 0; padding: 0;"></picture>

<i>Execute dentro da mesma pasta que se encontra o arquivo manage.py</i> <br>
<b>
python manage.py migrate <br>
python manage.py runserver <br>
</b>
</div>

### Testes de unidade

<i>Execute dentro da mesma pasta que se encontra o arquivo manage.py</i> <br>
<b>
python manage.py test <br>
</b>

Os códigos de teste encontram-se no arquivo /back_end/questionário/tests.py <br>
</div>

## Padrão utilizado: <a href="https://refactoring.guru/pt-br/design-patterns/strategy" target="_blank">Strategy</a>
Se encontra no método "verificar_respostas" na pasta de questionário, em views.py. A implementação do Strategy em sí está ná pasta "<a href="https://github.com/virocha11/Supervelha-SPA/tree/main/back_end/questionario/padrao_projeto" target="_blank">padrao_projeto</a>", dentro da pasta questionário, em "<a href="https://github.com/virocha11/Supervelha-SPA/blob/main/back_end/questionario/padrao_projeto/strategies.py" target="_blank">strategies.py</a>".

Com o strategy, podemos encapsular as diferentes partes do método (verificação se é ou não um professor e o que cada possibilidade acarretaria) em classes diferentes, fazendo com que o comportamento de um objeto varie dependendo da estratégia que está sendo chamada para a implementação de um método, tornando o código mais flexível.
Antes de aplicar o padrão Strategy, "verificar_respostas" era implementado diretamente na views.py e tinha uma lógica bem sedimentada, tornando difícil a manutenção caso se, por exemplo, no futuro, adicionássemos mais algum usuário que fosse capaz de verificar as respostas de um questionário que senão o professor, ou outros tipos de verificação.
