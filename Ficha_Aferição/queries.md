# Queries 

## Quantos alunos estão registados? (inteiro)

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>


SELECT (COUNT(?aluno) AS ?totalAlunos)
WHERE {
  ?aluno rdf:type :Aluno .
}

```

## Quantos alunos frequentam o curso "LCC"? (inteiro)

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>
SELECT (COUNT(?aluno) AS ?totalAlunosLCC)

WHERE {
  ?aluno rdf:type :Aluno .
  ?aluno :temCurso :LCC .
}
```

## Que alunos tiveram nota positiva no exame de época normal? (lista ordenada alfabeticamente por nome com: idAluno, nome, curso, nota do exame);

```
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

  SELECT ?idAluno ?nomeAluno ?curso ?notaExame
  WHERE {
    ?aluno rdf:type :Aluno .
    ?aluno :realizouExame ?exame .
    ?exame rdf:type :Exame .
    ?exame :notaExame ?notaExame .
    ?aluno :nomeAluno ?nomeAluno .
    ?aluno :idAluno ?idAluno .
    ?aluno :temCurso ?curso .
    FILTER (?notaExame >= 10 && CONTAINS(str(?exame), "normal_"))
  }
  ORDER BY ?nomeAluno

```

## Qual a distribuição dos alunos pelas notas do projeto? (lista com: nota e número de alunos que obtiveram essa nota)

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

SELECT ?notaProjeto (COUNT(?aluno) AS ?numAlunos)
WHERE {
  ?aluno rdf:type :Aluno .
  ?aluno :notaProjeto ?notaProjeto .
}
GROUP BY ?notaProjeto
ORDER BY ?notaProjeto
```

## Quais os alunos mais trabalhadores durante o semestre? (lista ordenada por ordem decrescente do total: idAluno, nome, curso, total = somatório dos resultados dos TPC)

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>

SELECT ?idAluno ?nomeAluno ?curso (SUM(?notaTPC) AS ?total)
WHERE {
  ?aluno rdf:type :Aluno .
  ?aluno :fezTPC ?tpc .
  ?tpc :notaTPC ?notaTPC .
  ?aluno :nomeAluno ?nomeAluno .
  ?aluno :idAluno ?idAluno .
  ?aluno :temCurso ?curso .
  FILTER(?curso != "{aluno['curso']}")
  FILTER(?idAluno != "{aluno['idAluno']}")
  FILTER(?nomeAluno != "{aluno['nome']}")
}
GROUP BY ?idAluno ?nomeAluno ?curso
ORDER BY DESC(?total)
```

## Qual a distribuição dos alunos pelos vários cursos? (lista de cursos, ordenada alfabeticamente por curso, com: curso, número de alunos nesse curso)

```
PREFIX : <http://rpcw.di.uminho.pt/2024/AvalAlunos/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?curso (COUNT(?aluno) AS ?numAlunos)
WHERE {
  ?aluno rdf:type :Aluno .
  ?aluno :temCurso ?curso .
  FILTER(?curso != "{aluno['curso']}")
}
GROUP BY ?curso
ORDER BY ?curso
```

