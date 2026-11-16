# Roteiro prático 03. Introdução ao Jupyter no Codespace

**Disciplina:** Sistemas de Banco de Dados I. Sistemas de Informação. UNIPAM.
**Itens da ementa:** 2.3, linguagens e interfaces do SGBD. 4.3, consulta de recuperação básica. 7.1, consultas com junção e agregação.
**Referência:** ELMASRI, R. NAVATHE, S. *Sistemas de Banco de Dados*. 7. ed. São Paulo: Pearson. Capítulos 2, 6 e 7.
**Ambiente:** PostgreSQL 17 em contêiner Docker, no Codespace da disciplina, acessado por um notebook Jupyter no VS Code.
**Cenário:** banco de dados `bd_cantina`, das vendas de uma cantina em uma semana.

---

## Sumário

1. Objetivo
2. Preparação
3. O notebook
4. O SQL no notebook
5. As tabelas e os dados da cantina
6. Do resultado ao gráfico
7. Salvar, executar tudo e reabrir
8. Erros frequentes e leitura das mensagens
9. Exercícios
10. Gabarito
11. Referências

---

## 1. Objetivo

Até aqui, todo o SQL da disciplina foi executado pela extensão Database Client, que envia ao servidor o comando do arquivo `.sql` e mostra o resultado em uma tabela. Um notebook Jupyter é outra interface para o mesmo servidor. Nele, o SQL é escrito em células, o resultado aparece logo abaixo de cada uma, e o resultado de uma consulta pode ser transformado em gráfico. O comando, o resultado e o gráfico ficam gravados no mesmo arquivo.

Este roteiro prepara o Codespace para usar notebooks, apresenta o funcionamento das células e percorre, sobre um banco pequeno, o caminho completo que a Prática 02 vai exigir: criar o banco e as tabelas, inserir os dados, consultar e desenhar o gráfico.

| Resultado | Descrição |
|---|---|
| Ambiente | Instalar o Jupyter no Codespace e escolher o kernel da disciplina |
| Células | Criar células de texto e de código, executá-las e interpretar o número de execução |
| SQL no notebook | Conectar a um banco, criar tabelas, inserir dados e consultar a partir do notebook |
| Gráficos | Guardar o resultado de uma consulta e desenhá-lo com as funções `barras` e `linha` |

### 1.1 Delimitação

O notebook usa a linguagem Python por baixo, mas este roteiro não trata de Python. As únicas linhas fora do SQL são as da célula de preparação, explicada na seção 4.1, e as chamadas às funções de gráfico, que seguem sempre o mesmo modelo. O conteúdo da disciplina continua sendo o SQL de cada célula.

---

## 2. Preparação 

### 2.1 O servidor

O Codespace é o mesmo das aulas anteriores. No terminal, na raiz do repositório, o comando abaixo deve mostrar `postgres_container` com o estado `healthy`.

```bash
docker compose ps
```

Caso o contêiner não esteja em execução, o comando `docker compose up -d` o inicia.

### 2.2 Os arquivos da aula

O arquivo `aula-7.zip`, disponível no Portal UNIPAM, é arrastado para a raiz do repositório, no explorador de arquivos do Codespace. No terminal, ele é descompactado e removido.

```bash
unzip aula-7.zip
rm aula-7.zip
cd aula07
```

A pasta `aula07` contém este roteiro, a pasta `figuras` e dois arquivos usados pelo notebook:

| Arquivo | Função |
|---|---|
| `preparar-jupyter.sh` | instala o Jupyter no Codespace |
| `graficos.py` | contém as funções `barras` e `linha`, que desenham os gráficos. Não deve ser alterado |

### 2.3 Instalação do Jupyter

Ainda no terminal, dentro da pasta `aula07`, executa-se o script de preparação.

```bash
bash preparar-jupyter.sh
```

O script mostra cinco etapas. Ele confere o servidor, instala o Python, cria o ambiente da disciplina na pasta `~/.venv-sbd`, registra o kernel **SBD (Python 3)** e instala no VS Code as extensões **Python** e **Jupyter**, ambas da Microsoft. A instalação é feita uma única vez por Codespace e vale também para a Prática 02. Ao final aparece a mensagem `Pronto`.

O ambiente fica fora do repositório, na pasta pessoal do Codespace, e por isso não é enviado ao GitHub no `commit`.

---

## 3. O notebook

### 3.1 Criação do arquivo

Um notebook é um arquivo com a extensão `.ipynb`. Para criá-lo:

1. Abrir a paleta de comandos com **Ctrl + Shift + P**.
2. Digitar `Create: New Jupyter Notebook` e confirmar com Enter. Abre-se um notebook vazio, ainda sem nome.
3. Salvar com **Ctrl + S**, escolher a pasta `aula07` e dar ao arquivo o nome `cantina.ipynb`.

O notebook precisa ficar na mesma pasta que o arquivo `graficos.py`, porque é ali que ele procura as funções de gráfico.

### 3.2 O kernel

O **kernel** é o programa que executa as células. No canto superior direito do notebook há o botão **Select Kernel**. Ao clicar nele, escolher **Jupyter Kernel** e, na lista, **SBD (Python 3)**. O nome do kernel passa a aparecer no lugar do botão.

Se a opção **SBD (Python 3)** não aparecer, executar o comando **Developer: Reload Window**, pela paleta de comandos, e repetir a escolha.

### 3.3 Os dois tipos de célula

O notebook é formado por células, uma abaixo da outra. Há dois tipos.

| Tipo | Conteúdo | Aparência |
|---|---|---|
| Markdown | texto formatado: títulos, parágrafos, listas | depois de executada, aparece como texto comum |
| Código | instruções executadas pelo kernel. Neste roteiro, SQL | caixa com fundo cinza e colchetes à esquerda |

Ao passar o mouse entre duas células, ou abaixo da última, aparecem os botões **+ Code** e **+ Markdown**, que inserem uma célula nova naquele ponto.

A primeira célula do notebook é de Markdown, com o título do trabalho. Inserir uma célula com **+ Markdown** e escrever:

```text
# Aula 07. Cantina

Aluno(a): nome completo
```

O símbolo `#` no início da linha faz dela um título. Para sair da edição e ver o texto formatado, pressionar **Shift + Enter**. Um clique duplo sobre o texto abre a célula para edição de novo.

### 3.4 Execução de uma célula

Uma célula é executada com **Shift + Enter**, que roda a célula e passa para a seguinte, ou pelo triângulo à esquerda dela. Enquanto a célula está em execução, aparece um indicador ao lado. Ao terminar, surge entre os colchetes um número, como `[1]`, e o resultado aparece logo abaixo.

O número indica a **ordem em que as células foram executadas**, e não a posição delas no arquivo. Uma célula executada duas vezes recebe um número novo a cada execução. Por isso o notebook não lê as células de cima para baixo por conta própria: cada célula usa o estado deixado pelas que já foram executadas, em qualquer ordem. Quando os números ficam fora de sequência, a forma segura de conferir o trabalho é executar tudo de novo, como descreve a seção 7.

### 3.5 Atalhos

Os atalhos abaixo valem quando a célula está selecionada, mas fora da edição. Para sair da edição, pressionar **Esc**.

| Atalho | Efeito |
|---|---|
| **Shift + Enter** | executa a célula e passa para a seguinte |
| **Ctrl + Enter** | executa a célula e permanece nela |
| **A** | insere uma célula acima |
| **B** | insere uma célula abaixo |
| **M** | transforma a célula em Markdown |
| **Y** | transforma a célula em código |
| **D D** | apaga a célula (a letra D duas vezes) |

---

## 4. O SQL no notebook

### 4.1 A célula de preparação

A segunda célula do notebook, de código, prepara o ambiente. Ela é inserida com **+ Code** e contém exatamente as quatro linhas abaixo.

```python
%load_ext sql
%config SqlMagic.displaylimit = 50
%config SqlMagic.displaycon = False
from graficos import barras, linha
```

| Linha | Efeito |
|---|---|
| `%load_ext sql` | ativa os comandos `%sql` e `%%sql`, que enviam SQL ao servidor |
| `%config SqlMagic.displaylimit = 50` | mostra até 50 linhas de cada resultado |
| `%config SqlMagic.displaycon = False` | omite, em cada resultado, a linha que repete o endereço da conexão |
| `from graficos import barras, linha` | carrega as duas funções de gráfico do arquivo `graficos.py` |

A célula não produz resultado visível. Ela deve ser executada **sempre que o notebook for aberto**, antes de qualquer outra, porque o kernel começa vazio a cada abertura.

### 4.2 A conexão

Uma linha que começa com `%sql`, seguida de um endereço, conecta o notebook a um banco de dados. O endereço reúne as informações da conexão cadastrada no Database Client.

```text
postgresql://root:root@localhost:5432/bd_aula
           usuário:senha@servidor:porta/banco
```

A célula seguinte conecta ao `bd_aula`, o banco das primeiras aulas.

```sql
%sql postgresql://root:root@localhost:5432/bd_aula
```

O resultado é a mensagem `Connecting to 'postgresql://root:***@localhost:5432/bd_aula'`.

### 4.3 As células `%%sql`

Uma célula que começa com `%%sql`, com dois sinais de porcentagem, envia ao servidor **todo** o seu conteúdo, que pode ter várias instruções separadas por ponto e vírgula. É o formato usado no restante do roteiro.

| Início da célula | Alcance |
|---|---|
| `%sql` | só o que está na mesma linha |
| `%%sql` | a célula inteira, a partir da linha seguinte |

### 4.4 A criação do banco

Com a conexão em `bd_aula`, a célula abaixo cria o banco da cantina.

```sql
%%sql
CREATE DATABASE bd_cantina
```

O banco só pode ser criado uma vez. Executada de novo, a mesma célula produz o erro `database "bd_cantina" already exists`. Para que a instrução fique registrada no notebook sem ser executada outra vez, a célula é transformada em Markdown: selecioná-la, pressionar **Esc** e depois **M**. O texto continua visível, mas deixa de ser executado.

Em seguida, uma célula nova troca a conexão para o banco recém-criado. A partir dela, todo o SQL é executado em `bd_cantina`.

```sql
%sql postgresql://root:root@localhost:5432/bd_cantina
```

---

## 5. As tabelas e os dados da cantina

### 5.1 O minimundo

A cantina vende lanches, cada um com um nome, que não se repete, um tipo, Salgado, Bebida ou Doce, e um preço. Cada venda registra o lanche, o dia e a quantidade vendida. Os dados são os da semana de 09/11/2026 a 13/11/2026. O valor de uma venda é a quantidade multiplicada pelo preço do lanche e não é armazenado.

### 5.2 As tabelas

Em uma única célula, as duas tabelas são removidas, caso existam, e criadas. A tabela `lanche` é criada antes de `venda`, porque `venda` a referencia.

```sql
%%sql
DROP TABLE IF EXISTS venda, lanche;

CREATE TABLE lanche (
    id    INTEGER       GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome  TEXT          NOT NULL UNIQUE,
    tipo  TEXT          NOT NULL,
    preco NUMERIC(10,2) NOT NULL CHECK (preco > 0)
);

CREATE TABLE venda (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lanche_id  INTEGER NOT NULL REFERENCES lanche (id),
    data_venda DATE    NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0)
);
```

Como o `DROP TABLE IF EXISTS` vem antes, a célula pode ser executada quantas vezes for preciso.

### 5.3 A carga

Em outra célula, os sete lanches e as vinte vendas da semana.

```sql
%%sql
INSERT INTO lanche (nome, tipo, preco)
VALUES
    ('Pão de queijo',   'Salgado', 4.50),
    ('Coxinha',         'Salgado', 6.00),
    ('Misto quente',    'Salgado', 7.50),
    ('Suco natural',    'Bebida',  6.50),
    ('Café',            'Bebida',  3.00),
    ('Bolo de cenoura', 'Doce',    5.00),
    ('Brigadeiro',      'Doce',    2.50);

INSERT INTO venda (lanche_id, data_venda, quantidade)
VALUES
    (1, '2026-11-09', 30), (2, '2026-11-09', 18), (5, '2026-11-09', 25), (4, '2026-11-09', 10),
    (1, '2026-11-10', 26), (3, '2026-11-10', 12), (5, '2026-11-10', 22), (6, '2026-11-10',  8),
    (1, '2026-11-11', 35), (2, '2026-11-11', 20), (4, '2026-11-11', 15), (5, '2026-11-11', 30),
    (2, '2026-11-12', 16), (3, '2026-11-12', 14), (5, '2026-11-12', 20), (6, '2026-11-12', 10),
    (1, '2026-11-13', 40), (2, '2026-11-13', 25), (4, '2026-11-13', 18), (5, '2026-11-13', 28);
```

O resultado mostra `7 rows affected.` e `20 rows affected.`, uma linha para cada `INSERT`. Esta célula, ao contrário da anterior, não deve ser executada duas vezes: a segunda execução falha no `UNIQUE` de `nome`. Para recarregar os dados, executa-se primeiro a célula das tabelas, que as recria vazias.

O Brigadeiro foi cadastrado e não aparece em nenhuma venda. Ele é usado na seção 6.4.

### 5.4 Conferência

```sql
%%sql
SELECT * FROM lanche ORDER BY id
```

| id | nome | tipo | preco |
|---|---|---|---|
| 1 | Pão de queijo | Salgado | 4.50 |
| 2 | Coxinha | Salgado | 6.00 |
| 3 | Misto quente | Salgado | 7.50 |
| 4 | Suco natural | Bebida | 6.50 |
| 5 | Café | Bebida | 3.00 |
| 6 | Bolo de cenoura | Doce | 5.00 |
| 7 | Brigadeiro | Doce | 2.50 |

O resultado de uma célula `%%sql` aparece como tabela logo abaixo dela, como no Database Client.

---

## 6. Do resultado ao gráfico

### 6.1 Guardar o resultado

Para desenhar um gráfico, o resultado da consulta precisa ficar guardado com um nome. A primeira linha da célula passa a ser `%%sql resultado <<`. O sinal `<<` guarda o resultado com o nome escrito antes dele, e, nesse caso, a tabela não é exibida. O nome `resultado` é usado em todo o roteiro e na Prática 02.

### 6.2 Gráfico de barras

A consulta abaixo calcula a quantidade vendida de cada lanche, juntando as duas tabelas.

```sql
%%sql resultado <<
SELECT l.nome AS lanche, SUM(v.quantidade) AS quantidade
FROM lanche AS l
INNER JOIN venda AS v ON v.lanche_id = l.id
GROUP BY l.nome
ORDER BY quantidade DESC
```

O resultado mostra apenas `6 rows affected.`. Na célula seguinte, uma única linha desenha o gráfico.

```python
barras(resultado, "Quantidade vendida por lanche", horizontal=True)
```

A função recebe o resultado guardado e o título do gráfico. A opção `horizontal=True` deita as barras, o que facilita a leitura de nomes longos. Sem ela, as barras ficam em pé. A função mostra primeiro a tabela do resultado e, abaixo dela, o gráfico.

![Quantidade vendida por lanche](figuras/barras-quantidade.png)

As duas funções de gráfico seguem uma regra, que vale para todas as consultas deste roteiro e da Prática 02: **a primeira coluna do `SELECT` dá o nome de cada barra e a segunda coluna dá o valor.** Uma consulta com as colunas na ordem inversa produz um gráfico sem sentido.

O Brigadeiro não aparece, porque o `INNER JOIN` só mantém os lanches que têm par em `venda`.

### 6.3 Gráfico de linha

Para valores ao longo do tempo, a função é `linha`. A consulta abaixo calcula o faturamento de cada dia, isto é, a soma de quantidade vezes preço das vendas daquele dia.

```sql
%%sql resultado <<
SELECT v.data_venda AS dia,
       SUM(v.quantidade * l.preco) AS faturamento
FROM venda AS v
INNER JOIN lanche AS l ON l.id = v.lanche_id
GROUP BY v.data_venda
ORDER BY v.data_venda
```

```python
linha(resultado, "Faturamento por dia")
```

| dia | faturamento |
|---|---|
| 2026-11-09 | 383.00 |
| 2026-11-10 | 313.00 |
| 2026-11-11 | 465.00 |
| 2026-11-12 | 311.00 |
| 2026-11-13 | 531.00 |

![Faturamento por dia](figuras/linha-faturamento.png)

O `ORDER BY v.data_venda` é indispensável no gráfico de linha. Sem ele, os pontos podem sair fora da ordem dos dias, e a linha passa a ligar datas fora de sequência.

### 6.4 O `LEFT JOIN` no gráfico

Para que o gráfico mostre também os lanches sem venda, a junção passa a ser `LEFT JOIN`, com `lanche` à esquerda. Para o Brigadeiro, a soma das quantidades é nula, porque não há linha de `venda` para somar, e o `COALESCE` troca o nulo por zero.

```sql
%%sql resultado <<
SELECT l.nome AS lanche, COALESCE(SUM(v.quantidade), 0) AS quantidade
FROM lanche AS l
LEFT JOIN venda AS v ON v.lanche_id = l.id
GROUP BY l.nome
ORDER BY quantidade DESC
```

```python
barras(resultado, "Quantidade vendida por lanche, com LEFT JOIN", horizontal=True)
```

![Quantidade vendida por lanche, com LEFT JOIN](figuras/barras-left-join.png)

A comparação com o gráfico da seção 6.2 mostra a diferença entre as duas junções: o resultado do `LEFT JOIN` tem sete linhas, e o do `INNER JOIN` tem seis. Na Prática 02, o mesmo raciocínio se aplica ao `RIGHT JOIN` e ao `FULL JOIN`.

---

## 7. Salvar, executar tudo e reabrir

O notebook é salvo com **Ctrl + S**. O arquivo guarda o SQL, as tabelas de resultado e os gráficos, e pode ser aberto em outro computador com tudo visível.

Antes de entregar um notebook, ele é executado do início ao fim, para garantir que as células funcionam na ordem em que estão. Na barra superior do notebook, **Restart** reinicia o kernel, apagando tudo o que estava em memória, e **Run All** executa todas as células, de cima para baixo. Ao final, os números de execução ficam em sequência, `[1]`, `[2]`, `[3]`, e nenhuma célula mostra erro. A célula do `CREATE DATABASE`, já transformada em Markdown, não é executada.

Ao reabrir o notebook em outra aula, os resultados continuam visíveis, mas o kernel começa vazio. Antes de executar uma consulta nova, é preciso executar a célula de preparação e a de conexão.

---

## 8. Erros frequentes e leitura das mensagens

| Mensagem | Causa | Correção |
|---|---|---|
| `UsageError`, seguido de `Line magic function` ou de `Cell magic` e de `not found` | a célula de preparação não foi executada desde que o notebook foi aberto | executar a célula de preparação |
| `ModuleNotFoundError: No module named 'graficos'` | o notebook não está na mesma pasta que `graficos.py` | salvar o notebook na pasta `aula07` |
| `database "bd_cantina" already exists` | a célula do `CREATE DATABASE` foi executada de novo | transformar a célula em Markdown, seção 4.4 |
| `relation "lanche" does not exist` | a conexão está em `bd_aula`, ou a célula das tabelas ainda não foi executada | executar a célula de conexão a `bd_cantina` e a das tabelas |
| `duplicate key value violates unique constraint "lanche_nome_key"` | a célula da carga foi executada duas vezes | executar a célula das tabelas e depois a da carga |
| `NameError: name 'resultado' is not defined` | a célula do gráfico foi executada antes da célula da consulta | executar a célula `%%sql resultado <<` e depois a do gráfico |
| a lista de kernels não mostra **SBD (Python 3)** | o script de preparação não terminou ou a janela não foi recarregada | conferir a mensagem `Pronto` do script e executar **Developer: Reload Window** |

Nos erros de SQL, a mensagem do notebook começa com algumas linhas sobre a extensão e só depois traz o erro do PostgreSQL, a partir da linha `Original error message from DB driver`. É essa parte que interessa. Para uma tabela com o nome escrito errado, por exemplo, o trecho é:

```text
Original error message from DB driver:
(psycopg2.errors.UndefinedTable) relation "lancha" does not exist
LINE 1: SELECT * FROM lancha
                      ^
```

A linha `LINE 1` repete o comando, e o sinal `^` aponta o ponto em que o PostgreSQL encontrou o problema, como no Database Client.

---

## 9. Exercícios

Cada exercício é resolvido no próprio notebook `cantina.ipynb`, em uma célula `%%sql resultado <<`, seguida da célula do gráfico.

**Exercício 1.** Calcular o faturamento de cada tipo de lanche, do maior para o menor, com as colunas `tipo` e `faturamento`, e desenhar o gráfico de barras com o título `Faturamento por tipo`.

**Exercício 2.** Calcular a quantidade de bebidas vendidas em cada dia, em ordem de dia, com as colunas `dia` e `quantidade`, e desenhar o gráfico de linha com o título `Bebidas vendidas por dia`.

**Exercício 3.** Listar somente os lanches com faturamento acima de R$ 300,00, do maior para o menor, com as colunas `lanche` e `faturamento`, e desenhar o gráfico de barras horizontais com o título `Lanches com faturamento acima de R$ 300,00`.

**Exercício 4.** Executar o notebook inteiro com **Restart** e **Run All**, conferir que os números de execução estão em sequência e que nenhuma célula mostra erro, e salvar.

---

## 10. Gabarito

### Exercício 1

```sql
%%sql resultado <<
SELECT l.tipo, SUM(v.quantidade * l.preco) AS faturamento
FROM lanche AS l
INNER JOIN venda AS v ON v.lanche_id = l.id
GROUP BY l.tipo
ORDER BY faturamento DESC
```

```python
barras(resultado, "Faturamento por tipo")
```

| tipo | faturamento |
|---|---|
| Salgado | 1258.50 |
| Bebida | 654.50 |
| Doce | 90.00 |

![Faturamento por tipo](figuras/exercicio-1.png)

O tipo é coluna de `lanche`, e a quantidade é coluna de `venda`. Por isso o faturamento por tipo depende da junção das duas tabelas.

### Exercício 2

```sql
%%sql resultado <<
SELECT v.data_venda AS dia, SUM(v.quantidade) AS quantidade
FROM venda AS v
INNER JOIN lanche AS l ON l.id = v.lanche_id
WHERE l.tipo = 'Bebida'
GROUP BY v.data_venda
ORDER BY v.data_venda
```

```python
linha(resultado, "Bebidas vendidas por dia")
```

| dia | quantidade |
|---|---|
| 2026-11-09 | 35 |
| 2026-11-10 | 22 |
| 2026-11-11 | 45 |
| 2026-11-12 | 20 |
| 2026-11-13 | 46 |

![Bebidas vendidas por dia](figuras/exercicio-2.png)

O `WHERE` filtra as linhas antes do agrupamento, e só as vendas de Suco natural e de Café entram nas somas.

### Exercício 3

```sql
%%sql resultado <<
SELECT l.nome AS lanche, SUM(v.quantidade * l.preco) AS faturamento
FROM lanche AS l
INNER JOIN venda AS v ON v.lanche_id = l.id
GROUP BY l.nome
HAVING SUM(v.quantidade * l.preco) > 300
ORDER BY faturamento DESC
```

```python
barras(resultado, "Lanches com faturamento acima de R$ 300,00", horizontal=True)
```

| lanche | faturamento |
|---|---|
| Pão de queijo | 589.50 |
| Coxinha | 474.00 |
| Café | 375.00 |

![Lanches com faturamento acima de R$ 300,00](figuras/exercicio-3.png)

A condição é sobre a soma de cada grupo e, por isso, fica no `HAVING`, e não no `WHERE`. No `WHERE`, a soma ainda não existe, porque ele é avaliado antes do agrupamento.

### Exercício 4

Depois do **Run All**, as células de código ficam numeradas em sequência, a partir de `[1]`, e a última célula de gráfico mostra o gráfico do Exercício 3.

---

## 11. Referências

ELMASRI, R. NAVATHE, S. B. *Sistemas de Banco de Dados*. 7. ed. São Paulo: Pearson, 2018. Seções 2.3 (linguagens e interfaces do SGBD), 6.3 (consultas de recuperação básicas) e 7.1 (consultas com junção e agregação).

PROJECT JUPYTER. *Jupyter Notebook documentation*. Disponível em: https://docs.jupyter.org. Acesso em: 16 nov. 2026.

PLOOMBER. *JupySQL documentation*. Disponível em: https://jupysql.ploomber.io. Acesso em: 16 nov. 2026.
