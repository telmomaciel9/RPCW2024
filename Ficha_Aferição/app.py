from flask import Flask, jsonify, request
import requests

def extract_after_hash(s):
    return s.split('#')[-1]

app = Flask(__name__)

graphDB_endpoint = "http://localhost:7200/repositories/AvaliacaoAlunos"


# Rota para obter todos os alunos
@app.route('/api/alunos', methods=['GET'])
def get_alunos():
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

SELECT ?idAluno ?nomeAluno ?curso
WHERE {
  ?aluno rdf:type :Aluno .
  ?aluno :idAluno ?idAluno .
  ?aluno :nomeAluno ?nomeAluno .
  ?aluno :temCurso ?curso .
    
  FILTER(?curso != "{aluno['curso']}")
  FILTER(?idAluno != "{aluno['idAluno']}")
  FILTER(?nomeAluno != "{aluno['nome']}")
}
    """
    # Enviar a consulta SPARQL para o GraphDB
    response = requests.get(graphDB_endpoint, params={'query': query}, headers = {'Accept': 'application/sparql-results+json'})

    # Verificar se a resposta é bem-sucedida
    if response.status_code == 200:
        data = response.json()
        # Extrair os dados dos alunos da resposta SPARQL
        alunos = [{
            'idAluno': aluno['idAluno']['value'],
            'nomeAluno': aluno['nomeAluno']['value'],
            'curso': aluno['curso']['value']
        } for aluno in data['results']['bindings']]
        return jsonify(alunos)
    else:
        return jsonify({"error": "Falha ao buscar os alunos"}), 500

# Rota para obter informações completas de um aluno pelo ID
@app.route('/api/alunos/<string:id_aluno>', methods=['GET'])
def get_aluno_by_id(id_aluno):
    # Construir a consulta SPARQL para obter as informações do aluno com o ID fornecido
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?nomeAluno ?curso
    WHERE {
      ?aluno rdf:type :Aluno .
      ?aluno :nomeAluno ?nomeAluno .
      ?aluno :temCurso ?curso .
        
        FILTER(?curso != "{aluno['curso']}")
  FILTER(?idAluno != "{aluno['idAluno']}")
  FILTER(?nomeAluno != "{aluno['nome']}")
        FILTER (?curso = xsd:string(?curso))
    }
    """

    # Enviar a consulta SPARQL para o GraphDB
    response = requests.get(graphDB_endpoint, params={'query': query}, headers={'Accept': 'application/sparql-results+json'})

    # Verificar se a resposta é bem-sucedida
    if response.status_code == 200:
        data = response.json()
        if data['results']['bindings']:  # Verificar se há resultados
            aluno = {
                'idAluno': id_aluno,
                'nomeAluno': data['results']['bindings'][0]['nomeAluno']['value'],
                'curso': data['results']['bindings'][0]['curso']['value']
            }
            return jsonify(aluno)
        else:
            return jsonify({"error": "Aluno não encontrado"}), 404
    else:
        return jsonify({"error": "Falha ao buscar o aluno"}), 500

# Rota para obter uma lista de alunos de um curso específico, ordenada alfabeticamente por nome
@app.route('/api/alunos', methods=['GET'])
def get_alunos_by_curso():
    # Obter o parâmetro de consulta 'curso' da URL
    curso = request.args.get('curso')

    # Verificar se o parâmetro 'curso' foi fornecido
    if curso is None:
        return jsonify({"error": "Parâmetro 'curso' não fornecido"}), 400

    # Construir a consulta SPARQL para obter os alunos do curso específico, ordenados alfabeticamente por nome
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?idAluno ?nomeAluno ?curso
    WHERE {
      ?aluno rdf:type :Aluno .
      ?aluno :idAluno ?idAluno .
      ?aluno :nomeAluno ?nomeAluno .
      ?aluno :temCurso ?curso .
		FILTER(?curso != "{aluno['curso']}")
  FILTER(?idAluno != "{aluno['idAluno']}")
  FILTER(?nomeAluno != "{aluno['nome']}")
        FILTER (?curso = xsd:string(?curso))
    }
    ORDER BY ?nomeAluno
    """

    # Enviar a consulta SPARQL para o GraphDB
    response = requests.get(graphDB_endpoint, params={'query': query}, headers={'Accept': 'application/sparql-results+json'})

    # Verificar se a resposta é bem-sucedida
    if response.status_code == 200:
        data = response.json()
        # Extrair os dados dos alunos da resposta SPARQL
        alunos = [{
            'idAluno': aluno['idAluno']['value'],
            'nomeAluno': aluno['nomeAluno']['value'],
            'curso': aluno['curso']['value']
        } for aluno in data['results']['bindings']]
        return jsonify(alunos)
    else:
        return jsonify({"error": "Falha ao buscar os alunos"}), 500


# Rota para obter a lista de alunos com o número de TPCs realizados
@app.route('/api/alunos/tpc', methods=['GET'])
def get_alunos_with_tpc():
    # Construir a consulta SPARQL para obter os alunos e o número de TPCs realizados por cada aluno
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?idAluno ?nomeAluno ?curso (COUNT(?tpc) as ?numTPC)
    WHERE {
      ?aluno rdf:type :Aluno .
      ?aluno :idAluno ?idAluno .
      ?aluno :nomeAluno ?nomeAluno .
      ?aluno :temCurso ?curso .
      OPTIONAL {
        ?aluno :fezTPC ?tpc .
      }
    FILTER(?curso != "{aluno['curso']}")
  FILTER(?idAluno != "{aluno['idAluno']}")
  FILTER(?nomeAluno != "{aluno['nome']}")
        FILTER (?curso = xsd:string(?curso))
    }
    GROUP BY ?idAluno ?nomeAluno ?curso
    ORDER BY ?nomeAluno
    """

    # Enviar a consulta SPARQL para o GraphDB
    response = requests.get(graphDB_endpoint, params={'query': query}, headers={'Accept': 'application/sparql-results+json'})

    # Verificar se a resposta é bem-sucedida
    if response.status_code == 200:
        data = response.json()
        # Extrair os dados dos alunos da resposta SPARQL
        alunos = [{
            'idAluno': aluno['idAluno']['value'],
            'nomeAluno': aluno['nomeAluno']['value'],
            'curso': aluno['curso']['value'],
            'numTPC': int(aluno['numTPC']['value']) if 'numTPC' in aluno else 0
        } for aluno in data['results']['bindings']]
        return jsonify(alunos)
    else:
        return jsonify({"error": "Falha ao buscar os alunos"}), 500



# Rota para obter a lista de cursos e o número de alunos registrados em cada curso
@app.route('/api/alunos', methods=['GET'])
def get_cursos_and_alunos_count():
    # Obter o parâmetro de consulta 'groupBy' da URL
    group_by = request.args.get('groupBy')

    # Verificar se o parâmetro 'groupBy' foi fornecido e é igual a 'curso'
    if group_by != 'curso':
        return jsonify({"error": "Parâmetro 'groupBy' inválido"}), 400

    # Construir a consulta SPARQL para obter a lista de cursos e o número de alunos registrados em cada curso
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?curso (COUNT(?aluno) as ?numAlunos)
    WHERE {
      ?aluno rdf:type :Aluno .
      ?aluno :temCurso ?curso .
    
    FILTER(?curso != "{aluno['curso']}")
  FILTER(?idAluno != "{aluno['idAluno']}")
  FILTER(?nomeAluno != "{aluno['nome']}")
        FILTER (?curso = xsd:string(?curso))
    }
    GROUP BY ?curso
    ORDER BY ?curso
    """

    # Enviar a consulta SPARQL para o GraphDB
    response = requests.get(graphDB_endpoint, params={'query': query}, headers={'Accept': 'application/sparql-results+json'})

    # Verificar se a resposta é bem-sucedida
    if response.status_code == 200:
        data = response.json()
        # Extrair os dados dos cursos e número de alunos da resposta SPARQL
        cursos = [{
            'curso': curso['curso']['value'],
            'numAlunos': int(curso['numAlunos']['value'])
        } for curso in data['results']['bindings']]
        return jsonify(cursos)
    else:
        return jsonify({"error": "Falha ao buscar os cursos e número de alunos"}), 500


# Rota para obter a lista de notas registradas no projeto e o total de alunos que as obtiveram
@app.route('/api/alunos', methods=['GET'])
def get_notas_and_alunos_count():
    # Obter o parâmetro de consulta 'groupBy' da URL
    group_by = request.args.get('groupBy')

    # Verificar se o parâmetro 'groupBy' foi fornecido e é igual a 'projeto'
    if group_by != 'projeto':
        return jsonify({"error": "Parâmetro 'groupBy' inválido"}), 400

    # Construir a consulta SPARQL para obter a lista de notas registradas no projeto e o total de alunos que as obtiveram
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>


SELECT ?notaProjeto (COUNT(?aluno) AS ?numAlunos)
WHERE {
  ?aluno rdf:type :Aluno .
  ?aluno :notaProjeto ?notaProjeto .
}
GROUP BY ?notaProjeto
ORDER BY ?notaProjeto
    """

    # Enviar a consulta SPARQL para o GraphDB
    response = requests.get(graphDB_endpoint, params={'query': query}, headers={'Accept': 'application/sparql-results+json'})

    # Verificar se a resposta é bem-sucedida
    if response.status_code == 200:
        data = response.json()
        # Extrair os dados dos projetos e total de alunos que obtiveram as notas da resposta SPARQL
        notas = [{
            'projeto': projeto['projeto']['value'],
            'numAlunos': int(projeto['numAlunos']['value'])
        } for projeto in data['results']['bindings']]
        return jsonify(notas)
    else:
        return jsonify({"error": "Falha ao buscar as notas e número de alunos"}), 500



# Rota para obter a lista de alunos que realizaram o exame de recurso
@app.route('/api/alunos', methods=['GET'])
def get_alunos_recurso():
    # Obter o parâmetro de consulta 'groupBy' da URL
    group_by = request.args.get('groupBy')

    # Verificar se o parâmetro 'groupBy' foi fornecido e é igual a 'recurso'
    if group_by != 'recurso':
        return jsonify({"error": "Parâmetro 'groupBy' inválido"}), 400

    # Construir a consulta SPARQL para obter a lista de alunos que realizaram o exame de recurso
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?idAluno ?nomeAluno ?curso ?notaExame
WHERE {
  ?aluno rdf:type :Aluno .
  ?aluno :realizouExame ?exame .
  ?exame rdf:type :Exame .
  ?exame :notaExame ?notaExame .
  ?aluno :nomeAluno ?nomeAluno .
  ?aluno :idAluno ?idAluno .
  ?aluno :temCurso ?curso .
  FILTER (CONTAINS(str(?exame), "recurso_"))
    
    FILTER(?curso != "{aluno['curso']}")
  FILTER(?idAluno != "{aluno['idAluno']}")
  FILTER(?nomeAluno != "{aluno['nome']}")
        FILTER (?curso = xsd:string(?curso))
}
ORDER BY ?nomeAluno


    """

    # Enviar a consulta SPARQL para o GraphDB
    response = requests.get(graphDB_endpoint, params={'query': query}, headers={'Accept': 'application/sparql-results+json'})

    # Verificar se a resposta é bem-sucedida
    if response.status_code == 200:
        data = response.json()
        # Extrair os dados dos alunos que realizaram o exame de recurso da resposta SPARQL
        alunos_recurso = [{
            'idAluno': aluno['idAluno']['value'],
            'nomeAluno': aluno['nomeAluno']['value'],
            'curso': aluno['curso']['value'],
            'recurso': aluno['recurso']['value']
        } for aluno in data['results']['bindings']]
        return jsonify(alunos_recurso)
    else:
        return jsonify({"error": "Falha ao buscar os alunos que realizaram o exame de recurso"}), 500




if __name__ == '__main__':
    app.run(debug=True)