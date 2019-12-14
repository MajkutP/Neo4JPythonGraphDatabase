from flask import Flask, render_template, request
from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://hobby-iajifgnijmdigbkepcanjfdl.dbs.graphenedb.com:24787", auth=basic_auth("admin", "b.RYnAuhHxFubo.G6oqKom8tw1pyuYx"))
session = driver.session()

app = Flask(__name__)
@app.route('/')
def index_html():
    return render_template('index.html')

@app.route('/submitRating', methods=['POST'])
def submitSuccess_html():
    if request.method == 'POST':
        aircraft = request.form['aircraft']
        comment = request.form['comment']
        if aircraft == '' or comment == '':
            return render_template('index.html', message='Fill empty brackets')
        return render_template('submitSuccess.html')


if __name__ == '__main__':
    app.run()


