import json

def main():
    with open('db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    ttl = ""

    ttl += generate_aluno(db['alunos'], ttl)
    ttl += generate_curso(db['cursos'], ttl)
    ttl += generate_instrumento(db['instrumentos'], ttl)

    with open('output.ttl', 'w', encoding='utf-8') as output_file:
        output_file.write(ttl)
    
    concat_ttl_files('inicio.ttl', 'output.ttl', 'final.ttl')

    
def concat_ttl_files(file1_path, file2_path, output_file_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        file1_content = file1.read()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        file2_content = file2.read()

    concatenated_content = file1_content + file2_content

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(concatenated_content)


def generate_aluno(dic, ttl):
    for aluno in dic:
        registo = f"""
###  http://rpcw.di.uminho.pt/2024/escola_de_musica#{aluno['id']}
    :{aluno['id']} rdf:type owl:NamedIndividual ,
                :Aluno ;
        :temCurso :{aluno['curso']} ;
        :temInstrumentoAluno :{aluno['instrumento'].replace(" ", "_")} ;
        :anocurso_aluno {aluno['anoCurso']} ;
        :datanasc_aluno "{aluno['dataNasc']}" ;
        :id_aluno "{aluno['id']}" ;
        :nome_aluno "{aluno['nome'].replace(" ", "_")}" .
"""
        ttl += registo
    return ttl

def generate_curso(dic, ttl):
    for curso in dic:
        registo = f"""
###  http://rpcw.di.uminho.pt/2024/escola_de_musica#{curso['id']}
    :{curso['id']} rdf:type owl:NamedIndividual ,
                    :Curso ;
        :temInstrumentoCurso :{curso['instrumento']['#text'].replace(" ", "_")} ;
        :designacao_curso "{curso['designacao'].replace(" ", "_")}" ;
        :duracao_curso {curso['duracao']} ;
        :id_curso "{curso['id']}" .
"""
        ttl += registo
    return ttl

def generate_instrumento(dic, ttl):
    for instrumento in dic:
        registo = f"""
###  http://rpcw.di.uminho.pt/2024/escola_de_musica#{instrumento['#text'].replace(" ", "_")}
    :{instrumento['#text'].replace(" ", "_")} rdf:type owl:NamedIndividual ,
                :Instrumento ;
        :designacao_instrumento "{instrumento['#text'].replace(" ", "_")}" ;
        :id_instrumento "{instrumento['id']}" .
"""
        ttl += registo
    return ttl



if __name__ == "__main__":
    main()