class ProjetoTurma:
#esta classe é a ponte de ligação entre um projeto e uma turma. ela vai funcionar como um elo pra guardar apenas os IDs de ambos, servindo para dizer exatamente qual projeto pertence a qual turma no sistema. 
    
    def __init__(self, id_projeto, id_turma):
        self.id_projeto = id_projeto
        self.id_turma = id_turma
