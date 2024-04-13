import xml.etree.ElementTree as ET

# Função para criar triplas RDF com base nas informações extraídas do XML
def create_rdf_triples():
    # Ler o arquivo XML
    tree = ET.parse('royal.xml')
    root = tree.getroot()

    # Iterar sobre os elementos <person>
    for person in root.findall('.//person'):
        person_id = person.find('id').text
        person_name = person.find('name').text

        # Encontrar os pais da pessoa
        parents = person.findall('parent')
        for parent in parents:
            parent_id = parent.attrib['ref']
            # Verificar o sexo do pai/mãe
            parent_sex = 'Pai' if parent.tag == 'father' else 'Mãe'

            # Criar tripla RDF para temPai ou temMae
            rdf_triple = f'<http://rpcw.di.uminho.pt/2024/familia/{person_id}> :tem{parent_sex} <http://rpcw.di.uminho.pt/2024/familia/{parent_id}> .'
            print(rdf_triple)

# Chamar a função para criar as triplas RDF
create_rdf_triples()
