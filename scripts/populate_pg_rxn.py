import pathlib
import os
from scripts.utils import (get_pg_conn, 
                           set_schema,
                           write_fixed_lines_into_table, 
                           create_rxn_tables, 
                           get_num_cols, 
                           get_row_count,
                           create_rxn_indexes)

def insertToDB(rrf_files_path, 
               create_tables, 
               rxnconso_table_name='rxnconso', 
               rxnsat_table_name='rxnsat', 
               rxnrel_table_name='rxnrel'):
    """
    load the RxNorm data into PostgreSQL database
    """
    print('\n-------- Loading RxNorm Files Into Postgres DB --------\n')
    print('Starting...\n')

    # path to sql script to create the tables
    create_table_sql_script_path = pathlib.Path(__file__).parent.parent.resolve() / 'psql_scripts' / 'create_tables_rxn.psql'

    # path to sql script to add indexes
    add_indexes_sql_script_path = pathlib.Path(__file__).parent.parent.resolve() / 'psql_scripts' / 'add_indexes_rxn.psql'

    # get connection to DB
    conn = get_pg_conn()
    conn.autocommit = False

    with conn:
        with conn.cursor() as curs:
            schema_to_use = os.getenv('SCHEMA')

            print(f'Schema to use: {schema_to_use}\n')

            # set the schema to use
            set_schema(curs, schema_to_use)

            if create_tables == True:
                # create the RxNorm tables
                print('Creating the RxNorm tables...')
                create_rxn_tables(curs, create_table_sql_script_path)
                print('Finished creating the tables.\n')
            
            # expected RFF file names
            rff_files_table_pairs = {'RXNCONSO': rxnconso_table_name, 
                                     'RXNREL': rxnrel_table_name, 
                                     'RXNSAT': rxnsat_table_name}

            # copy the data from RFF files into the tables and add indexes
            for filename in rff_files_table_pairs.keys():
                print(f'Loading {filename .upper()} data...')

                # get expected number of columns in the table
                expected_col_number = get_num_cols(curs, rff_files_table_pairs[filename], schema_to_use)
                print(f'Expected number of columns: {expected_col_number}')

                # path to the rrf file for the table
                rrf_filepath = pathlib.Path(rrf_files_path) / f'{filename}.RRF'

                # write fixed line in rrf file into the table
                print(f'Table for {filename} is {rff_files_table_pairs[filename]}')
                write_fixed_lines_into_table(curs, rff_files_table_pairs[filename], rrf_filepath, expected_col_number)

                row_added = get_row_count(curs, rff_files_table_pairs[filename])
                print(f'Added {row_added} rows to {rff_files_table_pairs[filename]}')
                print(f'Finished loading {filename} data...\n')

            # add indexes
            print('Adding indexes...\n')
            create_rxn_indexes(curs, 
                               add_indexes_sql_script_path, 
                               rxnconso_table_name, 
                               rxnsat_table_name, 
                               rxnrel_table_name)
            print('Finished adding indexes.\n')

    conn.close()

    print('Finished loading RxNorm data to database.\n')
    print('\n-------- CHANGES HAVE BEEN COMMITED --------\n')