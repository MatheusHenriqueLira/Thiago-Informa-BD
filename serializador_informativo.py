from informativo import Informativo

def desserializar_informativo(linha_banco):
    #vê se a coluna idImagem existe, senão coloca como None
    id_img = linha_banco['idImagem'] if 'idImagem' in linha_banco.keys() else None
    
    return Informativo(
        id_info=linha_banco['Idinfo'],
        titulo=linha_banco['Titulo'],
        conteudo=linha_banco['Conteudo'],
        data_criacao=linha_banco['datacriacao'],
        id_admin=linha_banco['NomeAdmin'], 
        esta_fixado=linha_banco['estafixado'],
        id_imagem=id_img
    )
    
