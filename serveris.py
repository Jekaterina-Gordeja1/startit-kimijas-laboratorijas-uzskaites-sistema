from flask import Flask, json, jsonify, render_template, request
import dati
import sqlite3


app = Flask(__name__)

# nepieciešams garum- un mīkstinājumzīmēm json formātā
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/publiski')
def publiski():
    return render_template("pub_data.html")


@app.route('/pieslegties')
def pieslegties():
    return render_template("login.html")


@app.route('/uzskaite')
def uzskaite():
    return render_template("vielu_aprikojuma_uzskaite.html")


@app.route('/pievienot')
def pievienot():
    return render_template("pievienot_vielu_aprikojumu.html")


@app.route('/lietotajs')
def lietotajs():
    return render_template("user_menu.html")


@app.route('/api/v1/vielas', methods=['GET'])
def vielas():
    # atveram datni
    with open("dati/vielas.json", "r") as f:
        # ielasām un pārvēršam par json
        dati = json.loads(f.read())
    
    # pārveidojam par string pirms atgriežam
    return jsonify(dati)


## 4. Individuālie uzdevumi
# 1. Nomainiet arī vielām datu avotu līdzīgi, kā to darījām ar inventāru
@app.route('/api/v2/vielas', methods=['GET'])
def v2vielas():
    try:
      with sqlite3.connect("Dati.db") as conn:
        c = conn.cursor()
        # Kolonu secībai ir jābūt tādai pašai, kā mainīgajā column_names
        c.execute("SELECT ID, NOSAUKUMS, TIPS, APAKSTIPS, SKAITS, DAUDZUMS, MERVIENIBAS, KOMENTARI FROM Vielas")
        data = c.fetchall()
        jsonData = []
        column_names = ['id', 'nosaukums', 'tips', 'apakstips', 'skaits', 'daudzums', 'mervienibas', 'komentari']
        for row in data:
          # Savienojam kolonu nosaukumus ar datiem no tabulas
          info = dict(zip(column_names, row))
          # Papildinam JSON failu ar jaunu rindiņu katrā cikla izpildē
          jsonData.append(info)
        # izveido atbildi ko sūtīt web lapai
        atbilde={"atb":""}
        atbilde["dati"]=jsonData
    except:
      conn.rollback()
      # atbilde, ja problēmas ar db
      atbilde={"atb":"Vielas nedabūju"}
      atbilde["dati"]=[]
    finally:
      conn.commit()
      c.close()
      conn.close()    
      return atbilde



@app.route('/api/v1/inventars', methods=['GET'])
def inventars():
    # atveram datni
    with open("dati/inventars.json", "r") as f:
        # ielasām un pārvēršam par json
        dati = json.loads(f.read())
    
    # pārveidojam par string pirms atgriežam
    return jsonify(dati)

@app.route('/api/v2/inventars', methods=['GET'])
def v2inventars():
    try:
      # Izveidojam savienojumu ar Datubāzi
      with sqlite3.connect("Dati.db") as conn:
        # Izveidojam kursoru
        c = conn.cursor()
        # Izsaucam datu no Inventars tabulas. DAUDZUMS paņemam kā tukšu kolonu, lai rezultātos nebūtu Undefied
        c.execute("SELECT ID, NOSAUKUMS, TIPS, APAKSTIPS, '' AS DAUDZUMS, '' AS MERVIENIBAS, SKAITS, KOMENTARI FROM Inventars")
        # Ielasam datus mainīgajā
        data = c.fetchall()
        jsonData = ""
        # Kolonu nosaukumi, kādi tiks izmantoti JSON failā. Tiem ir jābūt tādā pašā secībā, kā kolonas lasām no tabulas SELECT izsaukumā
        column_names = ['id','nosaukums','tips','apakstips','daudzums', 'mervienibas', 'skaits', 'komentari']
        for row in data:
          # Savienojam kolonu nosaukums ar datiem no tabulas
          info = dict(zip(column_names, row))
          # Pa vienai rindiņai papildimām jsonData mainīgo, līdz visi dati ir nolasīti no tabulas. Aiz katra ieraksta pieliekam komatu, lai atdalītu ierakstus.
          jsonData = jsonData + json.dumps(info) + ','
        # Noņemam pēdējo lieko komatu
        jsonData = jsonData[:-1]
        # Ieliekam visus datus kvadrātiekavās
        jsonData = "[" + jsonData + "]"        
        atbilde={"atb":""}
        atbilde["dati"]=json.loads(jsonData)
    except:
      conn.rollback()
      atbilde={"atb":"Inventāru nedabūju"}
      atbilde["dati"]=[]
    finally:
      conn.commit()
      c.close()
      conn.close()    
      return atbilde


@app.route('/api/v1/viela/<vielasID>', methods=['GET'])
def viela_id(vielasID):
    # Noklusēta vērtība, ja viela netiks atrasta
    viela = "Viela ar ID {} neeksistē".format(vielasID)
    
    # atveram datni
    with open("dati/vielas.json", "r") as f:
        # ielasām un pārvēršam par json
        dati = json.loads(f.read())

    # meklējam vielu sarakstā
    for v in dati:
        # vielas ID ir skaitlis, jāpārveido datu tips
        if v["id"] == int(vielasID):
            viela = v
    return jsonify(viela)


@app.route('/api/v1/viela',methods=['POST'])
def jauna_viela():
    # atveram datni, lai ielasītu esošos datus
    with open("dati/vielas.json", "r", encoding='utf-8') as f:
        # ielasām un pārvēršam par json
        dati = json.loads(f.read())
    
    # atrodam lielāko vielas ID
    lielais_id = 1
    for viela in dati:
        if viela["id"] > lielais_id:
            lielais_id = viela["id"]

    # ielasām ienākošos datus un pārvēršam par json
    jauna_viela = json.loads(request.data)
    # šeit vajadzētu veikt pārbaudi vai ir visi nepieciešamie dati
    if len(jauna_viela) < 7:
        return jsonify("Aizpildiet visus laukus!")
    if len(jauna_viela["nosaukums"]) < 3:
        return jsonify("Vielas nosaukums ir par īsu!")
    
    # ja viss ir OK, pievienojam jauno id
    jauna_viela["id"] = lielais_id + 1
    # pievienojam jauno vielu pie datiem
    dati.append(jauna_viela)
    # ierakstam atjaunotos datus atpakaļ datnē
    with open("dati/vielas.json", "w", encoding='utf-8') as f:
        # ielasām un pārvēršam par json
        # šeit nevar izmantot jsonify, jo rakstām datnē nevis atgriežam no Flask
        f.write(json.dumps(dati))
    # atgriežam jauno ID
    return jsonify(lielais_id+1)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
