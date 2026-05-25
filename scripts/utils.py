import psycopg
from psycopg import sql
import os
from dotenv import load_dotenv
import re

def get_pg_conn():
    """
    get psycopg connection to postgres DB
    """
    load_dotenv()

    db_user = os.getenv('PG_USER')
    db_password = os.getenv('PG_PASSWORD')
    db_host = os.getenv('PG_HOST')
    db_name = os.getenv('PG_DATABASE')
    db_port = os.getenv('PG_PORT')

    conn = psycopg.connect(f"dbname={db_name} user={db_user} host={db_host} port={db_port} password={db_password}")

    return conn

def set_schema(curs, schema_to_use):
    """
    set the schema to use before loading data to DB
    """
    curs.execute(                                             
        sql.SQL("CREATE SCHEMA IF NOT EXISTS {schema}").format(
            schema = sql.Identifier(schema_to_use)
        )
    )

    curs.execute(                                             
        sql.SQL("SET search_path TO {schema}").format(
            schema = sql.Identifier(schema_to_use)
        )
    )

def create_rxn_tables(curs, sql_scripts_path):
    """
    create the tables using the SQL script 
    (SQL script is adapted from the downloaded RxNorm files)
    """
    curs.execute(open(f'{sql_scripts_path}', 'r').read())

def create_rxn_indexes(curs, 
                       sql_script_path, 
                       rxnconso_table_name, 
                       rxnsat_table_name, 
                       rxnrel_table_name):
    """
    add indexes to the RxNorm tables
    """
    query = sql.SQL(open(f'{sql_script_path}', 'r').read()).format(
        # RXNCONSO table and indexes
        rxnconso_table = sql.Identifier(rxnconso_table_name), 
        rxnconso_str_index=sql.Identifier(f"x_{rxnconso_table_name}_str"),
        rxnconso_rxcui_index=sql.Identifier(f"x_{rxnconso_table_name}_rxcui"),
        rxnconso_tty_index=sql.Identifier(f"x_{rxnconso_table_name}_tty"),
        rxnconso_code_index=sql.Identifier(f"x_{rxnconso_table_name}_code"),

        # RXNSAT table and indexes
        rxnsat_table = sql.Identifier(rxnsat_table_name), 
        rxnsat_rxcui_index = sql.Identifier(f"x_{rxnsat_table_name}_rxcui"),
        rxnsat_atv_index = sql.Identifier(f"x_{rxnsat_table_name}_atv"),
        rxnsat_atn_index = sql.Identifier(f"x_{rxnsat_table_name}_atn"),

        # RXNREL table and indexes
        rxnrel_table = sql.Identifier(rxnrel_table_name), 
        rxnrel_rxcui1_index = sql.Identifier(f"x_{rxnrel_table_name}_rxcui1"),
        rxnrel_rxcui2_index = sql.Identifier(f"x_{rxnrel_table_name}_rxcui2"),
        rxnrel_rela_index = sql.Identifier(f"x_{rxnrel_table_name}_rela")
    )

    curs.execute(query)

def get_num_cols(curs, table_name, table_schema):
    """
    get the original number of columns in a
    specified RxNorm table
    """
    curs.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = %s and table_schema = %s", (table_name, table_schema))
    return curs.fetchone()[0]


def write_fixed_lines_into_table(curs, table_name, filepath, expected_ori_delim_num):
    """
    for each line in rrf file specified in filepath,
    fix the line by replacing \ into \\ to escape backslashes
    and removing trailing | so the line can be inserted into
    the table specified as a row.
    
    this function is a psycopg (PostgreSQL) implementation of
    the RxNorm's Load_scripts_mysql_rxn_win.sql script with 
    the following source metadata:
    -- Title: Load_scripts_mysql_rxn_win.sql

    -- Author: National Library of Medicine (No individual author was named)

    -- Date: 2026-04-06

    -- Code version: Unknown

    -- Availability: https://download.nlm.nih.gov/rxnorm/RxNorm_full_prescribe_04062026.zip (after downloading, unzip and go to scripts/mysql/Load_scripts_mysql_rxn_win.sql)
    """
    with curs.copy(
        sql.SQL("COPY {} FROM stdin (FORMAT text, NULL '', DELIMITER '|')").format(sql.Identifier(table_name))) as copy:
            with open(str(filepath), encoding='utf-8') as file:
                for line in file:
                    # check if original number of | match what's expected
                    if(line.count('|') != expected_ori_delim_num):
                        print(line.count('|'))
                        raise ValueError(f'Original number of delimiter in line is not {expected_ori_delim_num}')

                    # if number of columns match, fix the line
                    line = re.sub('\|$','', line.replace('\\', '\\\\'))

                    # check if the number | match what's expected
                    if line.count('|') != (expected_ori_delim_num - 1):
                        raise ValueError(f'Number of delimiter after edit is not {expected_ori_delim_num - 1}')
                    
                    # copy the line into the table
                    copy.write(line)

def get_row_count(curs, table_name):
    """
    get row count for a table
    """
    curs.execute(                                             
        sql.SQL("SELECT COUNT(*) FROM {table_name}").format(
            table_name = sql.Identifier(table_name)
        )
    )

    return curs.fetchone()[0]