from flask import Flask, render_template, url_for
from datetime import datetime
import requests

def extract_after_hash(s):
    return s.split('#')[-1]

app = Flask(__name__)

data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

#GraphDB
graphDB_endpoint = "http://localhost:7200/repositories/tabelaPeriodica"

@app.route('/')
def index():
    return render_template('index.html', data= {"data": data_iso_formatada})

@app.route('/grupo')
def grupo():
    sparql_query = """
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select ?s ?n ?num where{
    ?s a :Group .
    OPTIONAL {?s :number ?num} .
    OPTIONAL {?s :name ?n} .
}
"""
    
    resposta = requests.get(graphDB_endpoint, 
                            params = {'query': sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})

    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        for item in dados:
            item['s']['value'] = extract_after_hash(item['s']['value'])

        return render_template('groups.html', data= dados)
    else:
        return render_template('error.html', data= {"data": data_iso_formatada})

@app.route('/elementos')
def elementos():
    sparql_query = """
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
select ?n ?simb ?nome ?g where{
    ?s a :Element ;
    :atomicNumber ?n ;
    :symbol ?simb ;
    :name ?nome ;
    :group ?g .
} ORDER BY ?n
"""
    resposta = requests.get(graphDB_endpoint, 
                            params = {'query': sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})

    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        for item in dados:
            item['g']['value'] = extract_after_hash(item['g']['value'])

        return render_template('elementos.html', dados= dados, data= {"data": data_iso_formatada})
    else:
        return render_template('error.html', data= {"data": data_iso_formatada})


@app.route('/element/<id>')
def element(id):
    sparql_query = f'''
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select ?n ?simb ?g where{{
    ?s a :Element ;
    :atomicNumber ?n ;
    :symbol ?simb ;
    :name "{id}" ;
    :group ?g .
}}
'''
    resposta = requests.get(graphDB_endpoint, 
                            params = {'query': sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})

    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        for item in dados:
            item['g']['value'] = extract_after_hash(item['g']['value'])
        return render_template('element.html', elemento= dados[0],  nome=id, data= {"data": data_iso_formatada})
    else:
        return render_template('error.html', data= {"data": data_iso_formatada})


@app.route('/grupo/<id>')
def grup(id):
    sparql_query = f'''
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select ?n ?num ?nome  where{{
    :{id} a :Group .
    OPTIONAL {{ :{id} :number ?num}} .
    OPTIONAL {{ :{id} :name ?n}} .
    ?e a :Element;
       :group :{id} ;
       :name ?nome .
}}
''' 
    resposta = requests.get(graphDB_endpoint, 
                            params = {'query': sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})

    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']

        return render_template('group.html', data= dados)
    else:
        return render_template('error.html', data= {"data": data_iso_formatada})



if __name__ == '__main__':
    app.run(debug=True)