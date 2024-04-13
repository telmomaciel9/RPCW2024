import json

def main():
    with open('Aval_Alunos.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    ttl = ""

    cursos = set()

    for aluno in db['alunos']:
        cursos.add(aluno['curso'])

        ttl += f"""
###  http://rpcw.di.uminho.pt/2024/AvalAlunos#{aluno['idAluno']}
:{aluno['idAluno']} rdf:type owl:NamedIndividual ,
            :Aluno ;
    """
        
        for tpc in aluno['tpc']:
            ttl += f"""
                :fezTPC :{tpc['tp']}_{aluno['idAluno']} ;
            """

        for tipo_exame, valor_exame in aluno['exames'].items():
            ttl += f"""
                :realizouExame :{tipo_exame}_{aluno['idAluno']} ;
            """
        
        ttl += f"""
    :notaProjeto "{aluno['projeto']}" ;
    :temCurso :{aluno['curso']} ;
    :idAluno "{aluno['idAluno']}" ;
    :nomeAluno "{aluno['nome']}" .
    """


    
        for tpc in aluno['tpc']:
            ttl += f"""
###  http://rpcw.di.uminho.pt/2024/AvalAlunos#{tpc['tp']}_{aluno['idAluno']}
:{tpc['tp']}_{aluno['idAluno']} rdf:type owl:NamedIndividual ,
            :TPC ;
    :notaTPC {tpc['nota']} .
            """

        for tipo_exame, valor_exame in aluno['exames'].items():
            ttl += f"""
###  http://rpcw.di.uminho.pt/2024/AvalAlunos#{tipo_exame}_{aluno['idAluno']}
:{tipo_exame}_{aluno['idAluno']} rdf:type owl:NamedIndividual ,
            :Exame ;
    :notaExame {valor_exame} .
            """


    for curso in cursos:
        ttl += f"""
###  http://rpcw.di.uminho.pt/2024/AvalAlunos#{curso}
:{curso} rdf:type owl:NamedIndividual ,
            :Curso ;
    :curso "{curso}" .
        """


    #with open('output.ttl', 'w', encoding='utf-8') as output_file:
    #    output_file.write(ttl)

    with open('AvalAlunos.ttl', 'a', encoding='utf-8') as output_file:
        output_file.write(ttl)


if __name__ == "__main__":
    main()