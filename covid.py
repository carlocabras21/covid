# python3

# piccolo script che mi plotta l'andamento dei dati di contagio 

# FARE ATTENZIONE ALLE COLONNE CON VALORI VUOTI.
# il programma si interrompe, e per ora lo lascio così
# in quanto quelle colonne non mi interessano. 
# Ci sto lavorando.

from urllib import request
import matplotlib.pyplot as plt
import datetime
from ast import literal_eval



# ************          Setup

scarica_ultima_versione_dati = True

stampa_dati_nazionale        = True
stampa_grafico_nazionale     = True

stampa_dati_regioni          = True
stampa_grafico_regioni       = True
grafici_regioni_singole      = True

andamento_settimanale        = True



# ************          Funzioni

# da stringa formattata come "yyyy-mm-dd" restituisce la stessa come Date
def to_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d').date()

# stampa i dati relativi al singolo giorno
def stampa_dati(date, dati, colonne):
    print("data", colonne)
    dati_t = list(map(list, zip(*dati))) # trasposta dei dati, per facilità di stampa
    for i in range(len(date)):
        print(date[i], dati_t[i])

# restituisce gli array con le date singoli e con i dati per i grafici
def get_array_dati(lines, indici_colonne, stampa_dati):
    n = len(indici_colonne)
    dati = [[] for x in range(n)]
    date = []

    for line in lines[1:]:
        splitted_line = line.split(",")

        date.append(to_date(splitted_line[0].split("T")[0]))

        for i in range(n):
            dati[i].append(literal_eval(splitted_line[indici_colonne[i]]))

    return date, dati

def stampa_grafico(x, y, label):
    plt.plot(x, y, label = label)
    plt.legend(loc = "upper left")

# ************          Nazionale
nomi_colonne_nazionale = ["data","stato","ricoverati_con_sintomi","terapia_intensiva","totale_ospedalizzati","isolamento_domiciliare","totale_positivi","variazione_totale_positivi","nuovi_positivi","dimessi_guariti","deceduti","casi_da_sospetto_diagnostico","casi_da_screening","totale_casi","tamponi","casi_testati","note"]
# ---- questi sono gli indici delle colonne del csv
# [0] data                        
# [1] stato                      
# [2] ricoverati_con_sintomi      
# [3] terapia_intensiva         
# [4] totale_ospedalizzati        
# [5] isolamento_domiciliare      
# [6] totale_positivi        
# [7] variazione_totale_positivi 
# [8] nuovi_positivi              
# [9] dimessi_guariti           
# [10] deceduti                   
# [11] casi_da_sospetto_diagnostico 
# [12] casi_da_screening           
# [13] totale_casi                
# [14] tamponi                     
# [15] casi_testati                
# [16] note                        



if stampa_dati_nazionale or stampa_grafico_nazionale:
    filename = "dpc-covid19-ita-andamento-nazionale.csv"

    if scarica_ultima_versione_dati:
        print ("scaricando l'ultima versione di " + filename + "...")
        url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/" + filename
        request.urlretrieve (url, filename)
        print("...fatto: " + filename)


    with open(filename) as f:
        lines = f.readlines()

        # indici_colonne = [13] # totale_casi
        indici_colonne = [8] # nuovi_positivi
        date, dati = get_array_dati(lines, indici_colonne, stampa_dati_nazionale)

        if stampa_dati_nazionale:
            stampa_dati(date, dati, [nomi_colonne_nazionale[i] for i in indici_colonne])

        if stampa_grafico_nazionale: 
            fig = plt.figure(0)
            fig.suptitle('Nazionale', fontsize=20)

            for i in range(len(indici_colonne)):
                # plt.plot(date, dati[i], label = nomi_colonne_nazionale[indici_colonne[i]])
                # plt.legend(loc = "upper left")
                stampa_grafico(date, dati[i], label = nomi_colonne_nazionale[indici_colonne[i]])
                
                # andamento settimanale
                if andamento_settimanale:
                    # ad ogni data, faccio la media dei 7 giorni precedenti
                    weekly_avg = [0 for x in range(len(date))]

                    for j in range(6, len(date)):
                        weekly_avg[j] = (sum(dati[i][j-6:j+1]))/7
                    
                    stampa_grafico(date, weekly_avg, label = "settimanale")

# plt.close() # per evitare l'errore ValueError: view limit minimum -36893.8 is less than 1 and is an invalid Matplotlib date value. This often happens if you pass a non-datetime value to an axis that has datetime units
# quell'errore non me lo dà più e lo script funiona

# ************          Regioni
nomi_colonne_regioni = ["data","stato","codice_regione","denominazione_regione","lat","long","ricoverati_con_sintomi","terapia_intensiva","totale_ospedalizzati","isolamento_domiciliare","totale_positivi","variazione_totale_positivi","nuovi_positivi","dimessi_guariti","deceduti","casi_da_sospetto_diagnostico","casi_da_screening","totale_casi","tamponi","casi_testati","note"]
# ---- questi sono gli indici delle colonne del csv
# [0] data                       
# [1] stato                      
# [2] codice_regione           
# [3] denominazione_regione         
# [4] lat                         
# [5] long                       
# [6] ricoverati_con_sintomi     
# [7] terapia_intensiva            
# [8] totale_ospedalizzati       
# [9] isolamento_domiciliare      
# [10] totale_positivi           
# [11] variazione_totale_positivi 
# [12] nuovi_positivi                
# [13] dimessi_guariti              
# [14] deceduti                     
# [15] casi_da_sospetto_diagnostico 
# [16] casi_da_screening         
# [17] totale_casi                 
# [18] tamponi                     
# [19] casi_testati                  
# [20] note                         

if stampa_dati_regioni or stampa_grafico_regioni: 
    regioni = []

    # ------ scegliere quali regioni visualizzare
    # regioni.append("Abruzzo")
    # regioni.append("Basilicata")
    # regioni.append("Calabria")
    # regioni.append("Campania")
    # regioni.append("Emilia-Romagna")
    # regioni.append("Friuli Venezia Giulia")
    # regioni.append("Lazio")
    # regioni.append("Liguria")
    # regioni.append("Lombardia")
    # regioni.append("Marche")
    # regioni.append("Molise")
    # regioni.append("P.A. Bolzano")
    # regioni.append("P.A. Trento")
    # regioni.append("Piemonte")
    # regioni.append("Puglia")
    regioni.append("Sardegna")
    # regioni.append("Sicilia")
    # regioni.append("Toscana")
    # regioni.append("Umbria")
    # regioni.append("Valle d'Aosta")
    # regioni.append("Veneto")


    filename = "dpc-covid19-ita-regioni.csv"

    if scarica_ultima_versione_dati:
        print ("scaricando l'ultima versione di " + filename + "...")
        url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/" + filename
        request.urlretrieve (url, filename)
        print("...fatto: " + filename)


    with open(filename) as f:
        all_lines = f.readlines()

        plot_index = 1
        casi_regioni = []
        for regione in regioni:
            if stampa_dati_regioni:
                print("\n\n ********** " + regione)

            lines = [line for line in all_lines if regione in line]

            # indici_colonne = [12, 17] # nuovi_positivi, totale_casi
            indici_colonne = [12] # nuovi_positivi
            date, dati = get_array_dati(lines, indici_colonne, stampa_dati_regioni)

            # andamento settimanale
            if andamento_settimanale:
                # ad ogni data, faccio la media dei 7 giorni precedenti
                weekly_avg = [0 for x in range(len(date))]

                for j in range(6, len(date)):
                    weekly_avg[j] = (sum(dati[i][j-6:j+1]))/7
            


            if stampa_dati_regioni:
                stampa_dati(date, dati, [nomi_colonne_regioni[i] for i in indici_colonne])

            if stampa_grafico_regioni:
                if grafici_regioni_singole:
					# grafici regioni in finestre separate
                    fig = plt.figure(plot_index)
                    fig.suptitle(regione, fontsize=20)
                    
                    for i in range(len(indici_colonne)):
                        stampa_grafico(date, dati[i], label = nomi_colonne_regioni[indici_colonne[i]])
                        if andamento_settimanale:
                            stampa_grafico(date, weekly_avg, label = "settimanale")
                    plot_index += 1

                else:
                    # grafici regioni nella stessa finestra
                    fig = plt.figure(1)
                    fig.suptitle("Regioni", fontsize=20)
                    for i in range(len(indici_colonne)):
                        stampa_grafico(date, dati[i], label = nomi_colonne_regioni[indici_colonne[i]])
                        if andamento_settimanale:
                            stampa_grafico(date, weekly_avg, label = "settimanale")


if stampa_grafico_nazionale or stampa_grafico_regioni:
    plt.show()
