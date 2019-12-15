from flask import Flask, render_template, request
from neo4j import GraphDatabase, basic_auth

data = None
data2 = None
driver = GraphDatabase.driver("bolt://hobby-iajifgnijmdigbkepcanjfdl.dbs.graphenedb.com:24787", auth=basic_auth("admin", "b.RYnAuhHxFubo.G6oqKom8tw1pyuYx"))
session = driver.session()
''' Conneciont test
session.run("CREATE (n:Person {name:'Bob'})")   
result = session.run("MATCH (n:Person) RETURN n.name AS name")
for record in result:
    print(record["name"])
'''
app = Flask(__name__)
@app.route('/')
def index_html():
    return render_template('index.html')

@app.route('/goToIndex', methods=['POST'])
def goToIndex_html():
    if request.method == 'POST':
        return render_template('index.html')

@app.route('/submitNewPlane', methods=['POST'])
def submitSuccess_html():
    if request.method == 'POST':
        aircraft = request.form['aircraft']
        battlerating = request.form['battlerating']
        country = request.form['country']
        if aircraft == '' or battlerating == '' or country == '':
            return render_template('index.html', message='Fill empty brackets')
        if ' ' in aircraft or ' ' in battlerating or ' ' in country:
            return render_template('index.html', message='Words cannot have whitespaces')
        session.run("CREATE (" + aircraft + ":Aircraft{name:" + "\"" + aircraft + "\"" + ", country:" + "\"" + country +"\"" + ", BattleRating:" + "\"" + battlerating + "\"" +"})")
        return render_template('submitSuccess.html')
 
@app.route('/submitNewMap', methods=['POST'])
def goToNewMapPage_html():
    if request.method == 'POST':
        mapname = request.form['mapname']
        year = request.form['year']
        if mapname == '' or year == '':
            return render_template('index.html', message='Fill empty brackets')
        if ' ' in mapname or ' ' in year:
            return render_template('index.html', message='Words cannot have whitespaces')
        session.run("CREATE (" + mapname + ":Map{name:" + "\"" + mapname + "\"" + ", year:" + "\"" + year + "\"" +"})")
        return render_template('submitSuccess.html')

@app.route('/goToRateAircract', methods=['POST'])
def goToRateAircract_html():
    if request.method == 'POST':
        data = session.run("Match (ee:Aircraft) Return ee.name as name")
        data2 = session.run("Match (ee:Aircraft) Return ee.name as name")
        return render_template('RateAircraft.html', data=data, data2=data2)

@app.route('/AircraftMapRel', methods=['POST'])
def goToAircraftMapRel_html():
    if request.method == 'POST':
        data = session.run("Match (ee:Aircraft) Return ee.name as name")
        data2 = session.run("Match (cc:Map) Return cc.name as name")
        return render_template('AircraftMapRelation.html', data=data, data2=data2)

@app.route('/AircraftMapInfo', methods=['POST'])
def goToAircraftMapInfo_html():
    if request.method == 'POST':
        aircraftrel = request.form['Air']
        maprel = request.form['Map']
        session.run("MATCH("+aircraftrel+":Aircraft{name:"+"\""+aircraftrel+ "\""+"}),("+maprel+":Map{name:"+"\""+maprel+"\""+"}) CREATE("+aircraftrel+")-[:used{role:["+"\""+"Fighter"+"\""+"]}]->("+maprel+")")
        return render_template('submitSuccess.html')

@app.route('/submitRating', methods=['POST'])
def submitRating_html():
    if request.method == 'POST':
        Air1 = request.form['Air1']
        Air2 = request.form['Air2']
        rating = request.form['rating']
        session.run("MATCH("+Air1+":Aircraft{name:"+"\""+Air1+ "\""+"}),("+Air2+":Aircraft{name:"+"\""+Air2+"\""+"}) CREATE("+Air1+")-[:meets{performance:"+rating+"}]->("+Air2+")")
        return render_template('submitSuccess.html')
    
@app.route('/goToFindMapsBasedOnAircraft', methods=['POST'])
def goToFindAircraftBasedOnMap_html():
    if request.method == 'POST':
        data = session.run("Match (ee:Aircraft) Return ee.name as name")
        return render_template('FindMap.html', data=data)

@app.route('/findMapsbyAircraft', methods=['POST'])
def findAircraftByMap_html():
    if request.method == 'POST':
        Air = request.form['Air']
        data = session.run("MATCH(plane:Aircraft{name:"+" \""+ Air + "\"" + "})-[:used]->(area) return area.name as name")
        return render_template('MapsFound.html', data=data)

if __name__ == '__main__':
    app.run()


