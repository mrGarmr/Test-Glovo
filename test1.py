# Task. Imagine there are 6 cities in which Glovo operates in Ukraine (UA). Calculate following:	
# 1.	Average delivered order duration in UA
# 2.	Average delivered order duration in Kyiv
# 3.	Average percentage of cancelled orders (cancelled orders/total orders) for each city
# 4.	Average percentage of cancelled orders in UA
# 5.	Cost per delivered order in UA
# 6.	Cost per delivered order in Kyiv

import pandas as pd
from pathlib import Path
import datetime

def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except:
            result = input_error()
            return main()
    return inner  


@error_handler
def main():
    data_i=loader()
    flag=True

    while flag:
        command=choose()
        ANSWEARS[command](data_i)
        if flag:
            choise=input('Do you want to continue(Yes) or exit (No)?  ')
            if choise.lower() not in YES:
                print('Have a nice day!')
                break         
        
def av_ua(data_i):
    duration=data_i['Delivered order duration, min'].tolist()
    result=sum(duration)/len(duration)
    summary=f'Average delivered order duration in UA: {result} min'
    print(summary)
    return summary

def av_kiev(data_i):
    cities=data_i['City'].tolist()
    duration=data_i['Delivered order duration, min'].tolist()
    df= pd.Series(data=duration, index=cities)
    duration_kiev=[]
    for i in cities:
        if 'Kyiv' in i:
            duration_kiev.append(df[i])

    if len(duration_kiev)>0:
        result=sum(duration_kiev)/len(duration_kiev)
    else:
        result=0        
    summary=f'Average delivered order duration in Kyiv: {result} min'
    print(summary)
    return summary

def av_p_city(data_i):
    delivered=data_i['Delivered orders'].tolist()
    failed=data_i['Cancelled orders'].tolist()
    cities=data_i['City'].tolist()
    order={'Delivered orders':delivered, 'Cancelled orders': failed}
    order_to_city= pd.DataFrame(data=order, index=cities)
    summary=[]
    for i in cities:
        canc=order_to_city.loc[i]['Cancelled orders']
        deliv=order_to_city.loc[i]['Delivered orders']
        summary.append(f'Average percentage of cancelled orders (cancelled orders/total orders) for  {i} {(canc/(deliv+canc))*100} %')
        print(f'Average percentage of cancelled orders (cancelled orders/total orders) for  {i} {(canc/(deliv+canc))*100} %')  
    return summary

def av_p_ua(data_i):
    delivered=data_i['Delivered orders'].tolist()
    failed=data_i['Cancelled orders'].tolist()

    failed_to_delivery= pd.Series(data=failed, index=delivered)
    percent=[]
    for i in delivered:
        percent.append(failed_to_delivery[i]/(failed_to_delivery[i]+i))  

    result=(sum(percent)/len(percent))*100 
    summary=f'Average percentage of cancelled orders in UA: {result} %'
    print(summary)
    return summary

def cost_ua(data_i):
    delivered=data_i['Delivered orders'].tolist()
    price=data_i['Total cost, UAH'].tolist()

    amount_of_delivery= pd.Series(data=price, index=delivered)
    av_amount=[]

    for i in delivered:
        av_amount.append(amount_of_delivery[i]/i)
    result=(sum(av_amount)/len(av_amount))
    summary=f'Average Cost per delivered order in UA {result} UAH'
    print(summary)
    return summary

def cost_kiev(data_i):
    cities=data_i['City'].tolist()
    delivered=data_i['Delivered orders'].tolist()
    price=data_i['Total cost, UAH'].tolist()
    pr_del={'Delivered orders':delivered, 'Total cost, UAH': price}
    amount_of_delivery= pd.DataFrame(data=pr_del, index=cities)
    av_amount=[]
    for i in cities:
        if 'Kyiv' in i:
            price_o=amount_of_delivery.loc[i]['Total cost, UAH']
            deliv=amount_of_delivery.loc[i]['Delivered orders']
            av_amount.append(price_o/deliv)
    if len(av_amount)>0:
        result=(sum(av_amount)/len(av_amount))
    else:
        result=0
    summary=f'Average Cost per delivered order in Kyiv {result} UAH'

    print(summary)
    return summary


def all_in(data_i):
    now = datetime.datetime.now()
    datestamp=now.strftime("%d.%m.%Y")
    file_name=f"Report{datestamp}.txt"
    path=Path(__file__).parent.resolve()/file_name

    with open(path, "w+") as file:
        file.write(av_ua(data_i)+'\n')
        file.write(av_kiev(data_i)+'\n')
        list_of_av=av_p_city(data_i)
        for i in list_of_av:
            file.write(i+'\n')
        file.write(av_p_ua(data_i)+'\n')
        file.write(cost_ua(data_i)+'\n')
        file.write(cost_kiev(data_i)+'\n')
    exit(data_i)

def choose():
    print(107*'_')
    print(44*'*'+'Possible commands:'+45*'*')
    print(107*'_')
    print('|  Command to enter |                                    Task                                             |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|        1          | Average delivered order duration in UA                                              |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|        2          | Average delivered order duration in Kyiv                                            |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|        3          | Average percentage of cancelled orders (cancelled orders/total orders) for each city|')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|        4          | Average percentage of cancelled orders in UA                                        |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|        5          | Cost per delivered order in UA                                                      |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|        6          | Cost per delivered order in Kyiv                                                    |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|        7          | Save all above output to file                                                       |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    print('|       exit        | Exit without saving                                                                 |')
    print('|'+19*'_'+'|'+85*'_'+'|')
    return input('Choose your command: ')

@error_handler
def loader():
    file=Path(__file__).parent.resolve()/'task.xlsx'
    data_i=pd.read_excel(file)
     
    while True:
        print(107*'_')  
        file=input('Please enter the exact path to data in *.xlsx format.\nIf you want to test this program just press enter.\n')
        print(107*'_')
        try:
            data_i=pd.read_excel(file)
            print(40*'*'+'The file is successfully loaded'+40*'*')
            return data_i
        except:
            if not file:
                return data_i
            print('Wrong path! Be sure file is in the same directory or the path is right!')


def exit(data_i):
    flag=False
    return flag

def input_error():
    print('Wrong input! Type exact command you want to do, "exit" to exit.')

ANSWEARS = {'1': av_ua, '2':av_kiev, '3': av_p_city, '4':av_p_ua, '5':cost_ua, '6':cost_kiev, '7':all_in, 'close': exit, 'exit': exit,'учше': exit}
YES=['yes', 'y', 'yeah','ye','lf', 'нуі','неы', 'н', 'да' ]

if __name__ == '__main__':
    main()