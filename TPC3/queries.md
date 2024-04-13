
1. Quais as cidades de um determinado distrito?
Testado com Distrito de Braga.
```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa#>

SELECT ?nomesDasCidades
WHERE {
  ?cidade rdf:type :Cidade .
  ?cidade :nome_cidade ?nomesDasCidades .
  ?cidade :emDistrito :Braga .
}
```

2. Distribuição de cidades por distrito?
```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa#>

SELECT ?nomdeDoDistrito (COUNT(?cidade) AS ?numeroDeCidades)
WHERE {PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa#>

SELECT ?cityName
WHERE {
  :Porto :origem ?connection .
  ?connection :destino ?city .
  ?city :nome_cidade ?cityName .
}
  ?cidade rdf:type :Cidade .
  ?cidade :emDistrito ?distrito .
  ?distrito rdf:type :Distrito .
  ?distrito :nome_distrito ?nomdeDoDistrito .
}
GROUP BY ?nomdeDoDistrito
```

3. Quantas cidades se podem atingir a partir do Porto?
```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa#>

PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT DISTINCT ?nomes
WHERE {
    ?cidadesi rdf:type :Cidade .
  	?cidadesi :emDistrito :Porto .
    ?destinos (^:destino/:origem)* ?cidadesi .
  	?destinos :nome_cidade ?nomes .
}
```

4. Quais as cidades com população acima de um determinado valor?
Testado com 10000 pessoas
```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?nomdeDaCidade ?população
WHERE {
  ?cidade rdf:type :Cidade .
  ?cidade :nome_cidade ?nomdeDaCidade .
  ?cidade :populacao_cidade ?população .
  FILTER (xsd:integer(?população) > 10000)
}
```