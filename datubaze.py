# Imports
import sqlite3
import requests
import json

# Nostabilizējam savienojumu ar dadtubāzi
conn = sqlite3.connect('Dati.db')

# Kursors
c = conn.cursor()

# Izveidojam tabulu Inventārs
# c.execute('CREATE TABLE IF NOT EXISTS Inventars (ID INTEGER PRIMARY KEY, NOSAUKUMS TEXT, TIPS TEXT, APAKSTIPS TEXT, SKAITS INTEGER, KOMENTARI TEXT)')

# Datu ievietošana Inventārs tabulā
# c.execute("INSERT INTO Inventars (NOSAUKUMS, TIPS, APAKSTIPS, SKAITS, KOMENTARI) VALUES ('Mērkolba','Trauks','Mērtrauks',2,'Trauks ar tiplumu 300ml, kas paredzēts šķidrumu mērīšanai')")

# Izdzēst lieko no datubāzes
# c.execute("DELETE FROM Inventars WHERE ID > 1")

# Piekļūšana datiem, kas glabājas pythonanywhere
# inventars_api_res = requests.get('https://pytonc.eu.pythonanywhere.com/api/v1/inventars')

# Datu pārveidošana JSON datu formātā
# inventars = inventars_api_res.json()

# Izprintējam saņemtos datus
# print(inventars)

# Saņemto datu ierakstīšana tabulā
# for inv in inventars:
#     c.execute("INSERT INTO Inventars (ID, NOSAUKUMS, TIPS, APAKSTIPS, SKAITS, KOMENTARI) values (?, ?, ?, ?, ?, ?)", [inv['id'], inv['nosaukums'], inv['tips'], inv['apakstips'], inv['skaits'], inv['komentari']])

# Datu atjaunošana tabulā
# c.execute("UPDATE Inventars SET APAKSTIPS = 'Trauki' WHERE ID = 1")

# Datu meklēšana ar parametriem
# t = ('Trauks', 'trauks',)
# c.execute('SELECT * FROM Inventars WHERE TIPS IN (?,?)', t)

# Jauna tabula Users
# c.execute('CREATE TABLE IF NOT EXISTS Users (id TEXT RIMARY KEY, vards TEXT, uzvards TEXT, loma TEXT, parole TEXT, Komentāri TEXT)')

# Piekļūšana datiem, kas glabājas JSON failā
# users_json = json.load(open('dati/users.json'))

# Kolonas tabulā
# kolonas = ['id', 'vards', 'uzvards', 'loma', 'parole', 'Komentāri']

# Cikls, kas salasa datus balstoties uz 'kolonas' datiem
# for data in users_json['users']:
#   # 'tuple' izveidos sarakstu ar datiem par vienu tabulas rindiņu
#   dati = tuple( data[c] for c in kolonas)
#   c.execute("INSERT INTO  Users values (?,?,?,?,?,?)", dati)







## 2. Individuālie uzdevumi
# 1.	Harmonizējiet datus tabulā ‘Inventars’, tas ir, ja kolona “TIPS” satur 2 vienādas vērtības, bet viena no tām ir ar mazo burtu, bet otra ir ar lielo burtu ( ‘Trauks’ un ‘trauks’), tad izdariet tā, lai ieraksti tabulā būtu ierakstīti vai nu tikai ar lielo burtu, vai nu tikai ar mazo burtu šai kolonai. Izmantojot ‘UPDATE’.
# Visu TIPS ierakstu pārveidošana uz maziem burtiem
# c.execute('UPDATE Inventars SET APAKSTIPS = LOWER(APAKSTIPS)') #APAKSTIPS

# 2.	Izveidojiet savā datubāzē tabulu ‘Vielas’ ar ‘ID’ kolonu, kā primāro atslēgu. Visiem Tabulas kolonu nosaukumiem ir jābūt uzrakstītiem ar lieliem burtu
# izveidojam tabulu Vielas
# c.execute('CREATE TABLE IF NOT EXISTS Vielas (ID INTEGER PRIMARY KEY, NOSAUKUMS TEXT, TIPS TEXT, APAKSTIPS TEXT, SKAITS INTEGER, DAUDZUMS TEXT, MERVIENIBAS TEXT, KOMENTARI TEXT)')

# 3. Piepildiet tabulu ‘Vielas’  ar datiem no https://pytonc.eu.pythonanywhere.com/api/v1/vielas avota. ID laukumam ir jūt secīgi numurētam no 1 līdz 54 (oriģinālās ID vērtības nederēs)
# Piekļūšana datiem, kas glabājas pythonanywhere
# vielas_api_res = requests.get('https://pytonc.eu.pythonanywhere.com/api/v1/vielas')
# Datu pārveidošana mums saprotamā json formātā
# vielas = vielas_api_res.json()
# Saņemto datu ierkstīšana tabulā
# for viel in vielas:
    # c.execute("INSERT INTO Vielas (NOSAUKUMS, TIPS, APAKSTIPS, SKAITS, DAUDZUMS, MERVIENIBAS, KOMENTARI) values (?, ?, ?, ?, ?, ?, ?)", [viel['nosaukums'], viel['tips'], viel['apakstips'], viel['skaits'], viel['daudzums'], viel['mervienibas'], viel['komentari']])



# Saglabājam izmaiņas datubāzē
conn.commit()

# Datu izsaukšana no tabulas
c.execute("SELECT * FROM Vielas")
print(c.fetchall())
# Savienojuma aizvēršana
c.close()
conn.close()