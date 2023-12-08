# Replicador de Banco de Dados Postgres

## TLDR

Este programa é utilizado para replicar um servidor PostgreSQL usando gatilhos (triggers) para inserções e exclusões, e o RabbitMQ para transmitir as alterações para todos os replicadores de banco de dados.

## Como Funciona

O PostgreSQL suporta os comandos LISTEN e NOTIFY, o que significa que um cliente pode escutar eventos em um determinado 'canal' e o servidor pode notificar os ouvintes usando o comando NOTIFY.

Definimos gatilhos SQL em inserções e atualizações (e possivelmente mais) para que em cada alteração notifiquemos os ouvintes sobre as alterações realizadas.

O arquivo changes_publisher.py é um ouvinte dessas notificações de banco de dados. Quando recebe os dados de entrada, os transmite para os replicadores por meio do serviço de mensagens RabbitMQ. Dessa forma, é feita apenas uma conexão com o servidor PostgreSQL, utilizando funções assíncronas.

As mensagens sobre alterações são persistidas no servidor RabbitMQ.

As alterações são então recebidas pelo arquivo changes_listener.py, que então confirma as alterações no banco de dados de réplica, também utilizando funções assíncronas.


## Configuração

- Primeiro, execute o servidor PostgreSQL.
- Adicione os gatilhos para as tabelas (neste caso, a tabela é chamada de users)

```sql
CREATE OR REPLACE FUNCTION notify_account_changes()
    RETURNS trigger AS
$$
BEGIN
    PERFORM pg_notify(
            'users_changed',
            json_build_object(
                    'table', TG_TABLE_NAME,
                    'operation', TG_OP,
                    'new_record', row_to_json(NEW),
                    'old_record', row_to_json(OLD)
                )::text
        );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_changed
    AFTER INSERT OR UPDATE
    ON users
    FOR EACH ROW
EXECUTE PROCEDURE notify_account_changes();
```

- Inicie o servidor RabbitMQ e configure as credenciais nos arquivos Python.
- Execute pipenv install e pipenv shell (instale o pipenv se não estiver instalado).
- Inicie o publisher de alterações python3 changes_publisher.py.
- Inicie o programa listener de alterações para quantas réplicas desejar.
- Insira ou atualize linhas e observe os logs do listener e dos bancos de dados.

Obs:

Certifique-se de que os passos abaixo correspondam ao processo descrito acima:

Instale o servidor PostgreSQL e crie os usuários necessários.
    https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart

Crie o banco de dados e as tabelas do projeto conforme os arquivos.

    https://www.atlassian.com/data/admin/how-to-list-databases-and-tables-in-postgresql-using-psql#:~:text=To%20view%20all%20of%20the,command%20or%20its%20shortcut%20%5Cl%20.
    
    https://blog.devart.com/create-table-in-postgresql.html#:~:text=accessed%20and%20retrieved.-,Creating%20a%20table%20using%20the%20PostgreSQL%20CREATE%20TABLE%20statement,(length)%20column_contraint%2C%20table_constraints%20)%3B

Execute os gatilhos do projeto.

Instale e execute o RabbitMQ.
    https://www.cherryservers.com/blog/how-to-install-and-start-using-rabbitmq-on-ubuntu-22-04

Instale e execute as dependências mencionadas nos logs.
(pipenv, psycopg2, pika, uvloop, etc.)

Inicialize o publisher e o listener.

Insira no banco de dados e observe se a replicação ocorreu.
