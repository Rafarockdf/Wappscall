from datetime import datetime

def obter_data_hora_atual():

    agora = datetime.now()
    

    data_hora_formatada = agora.strftime("%d-%m-%Y-%H-%M-%S")
    
    return data_hora_formatada

