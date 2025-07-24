from datacampus_agent import DatacampusAgent

agent = DatacampusAgent()

if agent.autenticar():
    contenido = agent.listar_contenido()
    print("Contenido:", contenido)

    if contenido and contenido['files_count'] > 0:
        primer_archivo = next((i for i in contenido['items'] if i['type'] == 'file'), None)
        if primer_archivo:
            data = agent.obtener_excel_como_json(primer_archivo['id'])
            print("Contenido del archivo:", data)