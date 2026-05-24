from scripts.download_rxn_files import download_current_prescribable_content 
from scripts.populate_pg_rxn import insertToDB
import pathlib

path_to_downloaded_files = None

def get_table_names_input_and_load_data(path_to_rff, create_tables):
    """
    get table names input and load data
    """
    rxnconso_table_name_input = input('Your table name for RXNCONSO.RFF: ')
    rxnsat_table_name_input = input('Your table name for RXNSAT.RFF: ')
    rxnrel_table_name_input = input('Your table name for RXNREL.RFF: ')

    insertToDB(path_to_rff, 
               create_tables, 
               rxnconso_table_name_input, 
               rxnsat_table_name_input, 
               rxnrel_table_name_input)

def path_menu(create_tables):
    """
    show menu to select path to folder with the .RFF files
    and load the data accordingly
    """
    while True:
        rff_path_menu_input = input("\n-------- PATH MENU --------\n"
                                    f"1. Use latest download path: {path_to_downloaded_files} \n"
                                    "2. Specify path to folder with .RRF files manually\n"
                                    "3. Back\n\n")
        
        if rff_path_menu_input == '1':
            if path_to_downloaded_files:
                path = pathlib.Path(path_to_downloaded_files) / 'rrf'
            else:
                print('No existing path to downloaded files')
                continue

        elif rff_path_menu_input == '2':
            path = input('Absolute path to folder with .RFF files: ')

        elif rff_path_menu_input == '3':
            break

        else:
            print('Invalid input')

        if pathlib.Path(path).is_dir():
            if create_tables == False:
                get_table_names_input_and_load_data(path, False)
                break
            else:
                insertToDB(path, True)
        else:
            print('Path is not an existing directory')

# the main menu
while True:    
    main_menu_input = input("\n------------ MAIN MENU ------------\n"
                            "1. Download current RxNorm prescribable content\n"
                            "2. Load RxNorm data into PostgreSQL database\n"
                            "3. Quit\n\n"
                            "Your choice: ")

    if  main_menu_input == '1':
        while True:
            monthly_weekly_input = input("\n-------- DOWNLOAD MENU --------\n"
                                         "Do you want to download the full monthly release or weekly update?\n"
                                         "1. Full monthly release\n"
                                         "2. Weekly update\n"
                                         "3. Back\n\n"
                                         "Your choice: ")
            
            # download monthly release and store path to directory conataining downloaded files
            if monthly_weekly_input == '1':
                path_to_downloaded_files = download_current_prescribable_content('monthly')

            # download weekly release and store path to directory conataining downloaded files
            elif monthly_weekly_input == '2':
                path_to_downloaded_files = download_current_prescribable_content('weekly')

            elif monthly_weekly_input == '3':
                break

            else:
                print('Invalid input')

    elif main_menu_input == '2':
        while True:
            load_menu_input = input("\n-------- LOAD MENU --------\n"
                                    "1. Load without creating tables (you have existing tables for RXNCONSO, RXNSAT and RXNREL data)\n"
                                    "2. Create tables named rxnconso, rxnsat and rxnrel then load data\n(IMPORTANT: if tables with those names exist, they will be dropped first)\n"
                                    "3. Back\n\n")
            
            if load_menu_input == '1':
                # path menu for loading data without creating tables
                path_menu(False)

            elif load_menu_input == '2':
                # path menu for loading data after creting tables first
                path_menu(True)

            elif load_menu_input == '3':
                break

            else:
                print('Invalid input')

    elif main_menu_input == '3':
        print('Goodbye')
        break

    else:
        print('Invalid input')