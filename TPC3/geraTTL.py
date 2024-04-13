import json
import random

with open("mapa-virtual.json") as f:
    bd = json.load(f)

cidades = set()
distritos = set()

baseUrl = "http://rpcw.di.uminho.pt/2024/mapavirtual"

# Definição de prefixos RDF
prefixes = """
@prefix : <http://rpcw.di.uminho.pt/2024/mapavirtual#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/mapavirtual> .
"""

# Inicialização da string TTL com os prefixos
ttl = prefixes


ttl+="""
<http://rpcw.di.uminho.pt/2024/mapavirtual> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapavirtual#destino
:destino rdf:type owl:ObjectProperty ;
         rdfs:domain :Ligação ;
         rdfs:range :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#emDistrito
:emDistrito rdf:type owl:ObjectProperty ;
            rdfs:domain :Cidade ;
            rdfs:range :Distrito .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#origem
:origem rdf:type owl:ObjectProperty ;
        rdfs:domain :Ligação ;
        rdfs:range :Cidade .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapavirtual#descricao_cidade
:descricao_cidade rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Cidade ;
                  rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#distancia_ligacao
:distancia_ligacao rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Ligação ;
                   rdfs:range xsd:float .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#id_cidade
:id_cidade rdf:type owl:DatatypeProperty ;
           rdfs:domain :Cidade ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#id_ligacao
:id_ligacao rdf:type owl:DatatypeProperty ;
            rdfs:domain :Ligação ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#nome_cidade
:nome_cidade rdf:type owl:DatatypeProperty ;
             rdfs:domain :Cidade ;
             rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#nome_distrito
:nome_distrito rdf:type owl:DatatypeProperty ;
               rdfs:domain :Distrito ;
               rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#populacao_cidade
:populacao_cidade rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Cidade ;
                  rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapavirtual#Cidade
:Cidade rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#Distrito
:Distrito rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/mapavirtual#Ligação
:Ligação rdf:type owl:Class .


#################################################################
#    General axioms
#################################################################

[ rdf:type owl:AllDisjointClasses ;
  owl:members ( :Cidade
                :Distrito
                :Ligação
              )
] .

"""



# Loop sobre as cidades
for obj in bd["cidades"]:
    cidades.add(obj["id"])
    obj["distrito"] = obj["distrito"].replace(" ", "_")
    distrito_uri = f"{baseUrl}#{obj['distrito']}"

    # Adiciona distrito se ainda não estiver presente
    if obj["distrito"] not in distritos:
        distritos.add(obj["distrito"])
        ttl += f"""
:{obj['distrito']} rdf:type owl:NamedIndividual,
    :Distrito ;
    :nome_distrito "{obj['distrito']}"^^xsd:string .
"""

    # Adiciona cidade
    ttl += f"""
:{obj['id']} rdf:type owl:NamedIndividual,
    :Cidade ;
    :id_cidade "{obj['id']}"^^xsd:string ;
    :nome_cidade "{obj['nome']}"^^xsd:string ;
    :populacao_cidade "{obj['população']}"^^xsd:string ;
    :descricao_cidade "{obj['descrição']}"^^xsd:string ;
    :emDistrito <{baseUrl}#{obj["distrito"]}> . 
"""

# Loop sobre as ligações
for obj in bd["ligacoes"]:
    if obj["destino"] in cidades and obj["origem"] in cidades:
        ttl += f"""
:{obj['id']} rdf:type owl:NamedIndividual,
    :Ligação ;
    :id_ligacao "{obj['id']}"^^xsd:string ;
    :distancia_ligacao "{obj['distância']}"^^xsd:float ;
    :origem <{baseUrl}#{obj["origem"]}> ;
    :destino <{baseUrl}#{obj["destino"]}> .
"""

# Salvar ou imprimir o TTL gerado
print(ttl)



with open("mapavirtual.ttl","w") as f:
    f.write(ttl)