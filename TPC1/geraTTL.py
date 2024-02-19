import json


with open('plantas.json') as file:
    data = json.load(file)
ttl = ""
objs = set()

for plant in data:
    objs.add(plant['Estado'])
    objs.add(plant['Implantação'])
    objs.add(plant['Gestor'])
    objs.add(plant['Espécie'])
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/Plantas#{plant['Id']}
<http://rpcw.di.uminho.pt/2024/Plantas#{plant['Id']}> rdf:type owl:NamedIndividual ,
                                                            <http://rpcw.di.uminho.pt/2024/TPC1/Planta> ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/temEspécie> <http://rpcw.di.uminho.pt/2024/TPC1/{plant['Espécie'].replace(" ", "_")}> ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/temEstado> <http://rpcw.di.uminho.pt/2024/TPC1/{plant['Estado']}> ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/temGestor> <http://rpcw.di.uminho.pt/2024/TPC1/{plant['Gestor'].replace(" ", "_")}> ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/temImplantação> <http://rpcw.di.uminho.pt/2024/TPC1/{plant['Implantação'].replace(" ", "_")}> ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Caldeira> "{plant['Caldeira']}"^^xsd:boolean ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Código_de_rua> {plant['Código de rua']} ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Data_de_Plantação> "{plant['Data de Plantação']}"^^xsd:dateTime ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Data_de_actualização> "{plant['Data de actualização']}"^^xsd:dateTime ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Freguesia> "{plant['Freguesia'].replace(" ", "_")}" ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Rua> "{plant['Rua'].replace(" ", "_")}" ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Id> {plant['Id']} ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Local> "{plant['Local'].replace(" ", "_")}" ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Nome_Científico> "{plant['Nome Científico'].replace(" ", "_")}" ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Número_de_Registo> {plant['Número de Registo']} ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Número_de_intervenções> "{plant['Número de intervenções']}"^^xsd:int ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Origem> "{plant['Origem']}" ;
                                                    <http://rpcw.di.uminho.pt/2024/TPC1/Tutor> "{plant['Tutor']}"^^xsd:boolean .
    """
    ttl += registo
    
for element in objs:
    filtered_element = element.replace(" ", "_")
    obj = f"""
###  http://rpcw.di.uminho.pt/2024/Plantas#{filtered_element}
:{filtered_element} rdf:type owl:NamedIndividual .
"""
    ttl +=obj

print(ttl)