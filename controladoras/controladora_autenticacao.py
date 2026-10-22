from banco import buscar_admin, buscar_responsavel
from modelos.admin import Admin
from modelos.responsavel import Responsavel
from serializadores.serializador_admin import SerializadorAdmin
from serializadores.serializador_responsavel import SerializadorResponsavel


class ControladoraAutenticacao:
    _instancia = None

    def __init__(self):
        self.conta_logada = False
        self.tipo_usuario = None
        self.usuario_logado = None

    @classmethod
    def obter_instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def executar_login(self, login=None, senha=None):
        """Realiza o login como Admin ou Responsavel usando banco.py e as classes serializadoras."""
        if login is None:
            login = input("Login: ").strip()
        if senha is None:
            senha = input("Senha: ").strip()

        dados_admin = buscar_admin(login, senha)
        if dados_admin:
            admin = SerializadorAdmin.desserializar(dados_admin)
            self.conta_logada = True
            self.tipo_usuario = "admin"
            self.usuario_logado = admin
            return "admin", admin

        dados_resp = buscar_responsavel(login, senha)
        if dados_resp:
            responsavel = SerializadorResponsavel.desserializar(dados_resp)
            self.conta_logada = True
            self.tipo_usuario = "responsavel"
            self.usuario_logado = responsavel
            return "responsavel", responsavel

        self.conta_logada = False
        self.tipo_usuario = None
        self.usuario_logado = None
        print("Login ou senha incorretos.")
        return None

    def verifica_login(self):
        return self.conta_logada and self.usuario_logado is not None

    def verificar_adm(self):
        return self.conta_logada and self.tipo_usuario == "admin"

    def logout(self):
        self.conta_logada = False
        self.tipo_usuario = None
        self.usuario_logado = None
