from data.config import StaticConfig, DynamicConfig
import os
import time
from datetime import datetime, timedelta
import csv


def populateClientListFromCSV():
    # Open the CSV file for reading
    with open('.\\clients\\client_list.csv', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.DictReader(csvfile)

        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row as a dictionary to the people list
            DynamicConfig.clients.append(row)
        


def selectClient():
    client = 0
    while True:
        clearScreen()
        printHelloMessage()
        printClientText()

        try:
            client = int(input('\nSelecione o cliente: '))
            if client in range(1, len(DynamicConfig.clients) + 1):
                print(f'Você selecionou: {DynamicConfig.clients[client - 1]['client_name']}')
                client = DynamicConfig.clients[client - 1]
                time.sleep(0.2)
                break
            else:
                print(f'Cliente inválido. Tente novamente.')
                time.sleep(0.2)
        except:
            print('O valor inserido está incorreto. Por favor, insira um número.')
            time.sleep(0.2)
    
    DynamicConfig.selected_client = client
    printHelloMessage()
         
    

def selectTimestamp():
    clearScreen()
    printHelloMessage()
    printTimestampText()

    date_or_days_choice = None
    unix_old_date = None

    while True:
        try:
            date_or_days_choice = input('Você deseja extrair os logs conforme uma quantidade de dias [DIAS] ou a partir de uma data [data]? ') or 'dias'
            if date_or_days_choice.lower() != 'dias' and date_or_days_choice.lower() != 'data':
                  raise Exception
            break
        except:
            print('Valor incorreto. Digite "dias" selecionar uma quantidade de dias ou "data" para selecionar uma data.')
            time.sleep(0.2)


    if date_or_days_choice.lower() == 'dias':
        days = int(input('Digite a quantidade de dias: '))
        if days != None:
            old_date = datetime.now() - timedelta(days=days)

            formated_old_date = None
            while True:
                try:
                    reset_time_choice = input('Você deseja resetar as horas, minutos e segundos para 00:00:00 [S/n]? ') or 's'
                    if reset_time_choice.lower() == 's':
                        formated_old_date = old_date.replace(hour=0, minute=0, second=0)
                        DynamicConfig.selected_old_date = formated_old_date
                        break
                    elif reset_time_choice.lower() == 'n':
                        formated_old_date = old_date
                        DynamicConfig.selected_old_date = formated_old_date
                        break
                    else:
                        print('Resposta inserida incorreta. Por favor, digite S para SIM ou N para NÃO.')
                except:
                    print("O valor inserido está incorreto. Por favor, digite S para SIM ou N para NÃO.")
                
            unix_old_date = int(formated_old_date.timestamp())

    elif date_or_days_choice.lower() == 'data':
        old_date = input('Digite a data mais antiga para começar a buscar os logs [dd/mm/YYYY]: ')
        formated_old_date = datetime.strptime(f'{old_date} 00:00:00', '%d/%m/%Y %H:%M:%S')

        while True:
            try:
                reset_time_choice = input('Você deseja resetar as horas, minutos e segundos para 00:00:00 [S/n]? ') or 's'
                if reset_time_choice.lower() == 's':
                    DynamicConfig.selected_old_date = formated_old_date
                    break
                elif reset_time_choice.lower() == 'n':
                    current_time = datetime.now()
                    formated_old_date = formated_old_date.replace(hour=current_time.hour, minute=current_time.minute, second=current_time.second)
                    DynamicConfig.selected_old_date = formated_old_date
                    break
                else:
                    print('Resposta inserida incorreta. Por favor, digite S para SIM ou N para NÃO.')
            except:
                print("O valor inserido está incorreto. Por favor, digite S para SIM ou N para NÃO.")
        
        unix_old_date = int(formated_old_date.timestamp())
    
    DynamicConfig.selected_timestamp = unix_old_date



def selectLogtype():
    clearScreen()
    printHelloMessage()
    printLogtypeText()

    logtype = None
    while True:
        try:
            logtype = int(input('\nSelecione o tipo de log desejado: '))
            if logtype in range(1, len(StaticConfig.LOG_TYPES) + 1):
                print(f'Você selecionou: {StaticConfig.LOG_TYPES[logtype - 1]['name']}')
                logtype = StaticConfig.LOG_TYPES[logtype - 1]
                time.sleep(0.2)
                break
            else:
                print(f'Tipo de log inválido. Tente novamente.')
                time.sleep(0.2)
        except:
            print('O valor inserido está incorreto. Por favor, insira um número.')
            time.sleep(0.2)
    
    DynamicConfig.selected_logtype = logtype
    DynamicConfig.selected_logtype_regex_patterns = StaticConfig.REGEX_PATTERNS[logtype['value']]



def printTimestampText():
    print('INTERVALO DE TEMPO')



def printLogtypeText():
    print('TIPO DE LOG')
    print('Você quer coletar logs sobre o que?')
    print('CUIDADO! Alguns tipos de log podem retornar milhares de registros (a depender do cliente), podendo travar a aplicação.')
    for index, logtype in enumerate(StaticConfig.LOG_TYPES):
        print(f'[{str(index + 1).rjust(2)}] - {logtype['name']}')



def printClientText():
    print('CLIENTE')
    print('Lista de clientes disponíveis')
    for index, client in enumerate(DynamicConfig.clients):
        print(f'[{index + 1}] - {client['client_name']}')



def printHelloMessage():
    print('CapyTrend Log Extractor\n')
    print(f'Cliente: {getCurrentClientName()}')
    print(f'Intervalo de tempo: {getCurrentTimestamp()}')
    print(f'Tipo de log: {getCurrentLogtype()}\n')



def printProcessing():
    clearScreen()
    printHelloMessage()
    input('Pressione ENTER caso as informações estejam corretas.')
    print('Fazendo as requisições e buscando os logs para gerar o CSV. Por favor, aguarde.')
    time.sleep(0.2)



def getCurrentClientName():
    if DynamicConfig.selected_client != None:
        return DynamicConfig.selected_client['client_name']
    else:
        return ''



def getCurrentTimestamp():
    if DynamicConfig.selected_timestamp != None:
        old_timestamp = DynamicConfig.selected_timestamp
        old_date = datetime.fromtimestamp(old_timestamp)
        old_date_converted = str(old_date.strftime('%d/%m/%Y %H:%M:%S'))
        actual_date = str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        days_in_between = (datetime.now() - old_date).days

        return f'{old_date_converted} - {actual_date} - ({days_in_between} dias)'
    else:
        return ''



def getCurrentLogtype():
    if DynamicConfig.selected_logtype != None:
        return DynamicConfig.selected_logtype['name']
    else:
        return ''


# NOT BEING USED!!!
def checkForDuplicatesAndAddToDection():
    # Create a dictionary to store occurrences of each unique array
    array_dict = {}
    
    # Iterate over the array
    for log in DynamicConfig.log_list:
        # Convert the array to a tuple to make it hashable
        log_tuple = tuple(log)

        # If the array is already in the dictionary, increment the "detect" count
        if log_tuple in array_dict:
            detection_value = int(array_dict[log_tuple][2])
            detection_value += 1
            array_dict[log_tuple][2] = str(detection_value)

        # Otherwise, add the array to the dictionary
        else:
            array_dict[log_tuple] = log
    
    # Convert the dictionary back to a list of lists
    updated_logs = list(array_dict.values())
    return updated_logs



def generateCSV():
    with open(DynamicConfig.csv_filename, 'w') as file:
        write = csv.writer(file, lineterminator='\n')
        write.writerow(StaticConfig.CSV_FIELDS[DynamicConfig.selected_logtype['value']])
        write.writerows(DynamicConfig.log_list)



def showResults():
    print(f'CSV gerado com sucesso em: {os.getcwd()}\\{DynamicConfig.csv_filename}') 
    print(f'Quantidade de logs extraídos: {len(DynamicConfig.log_list)}') 



def setCSVFileName():
    DynamicConfig.csv_filename = f'{DynamicConfig.selected_client['client_name']}-{DynamicConfig.selected_old_date.strftime("%d_%m_%Y")}-{datetime.now().strftime("%d_%m_%Y")}-{DynamicConfig.selected_logtype['value']}.csv'



def clearScreen():
    os.system('cls')
