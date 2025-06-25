class LivreInexistantError(Exception):
    def __init__(self, message="Le livre n'existe pas."):
        super().__init__(message)

class MembreInexistantError(Exception):
    def __init__(self, message="Le membre n'existe pas."):
        super().__init__(message)

class LivreIndisponibleError(Exception):
    def __init__(self, message="Le livre est déjà emprunté."):
        super().__init__(message)

class QuotaEmpruntDepasseError(Exception):
    def __init__(self, message="Le quota d'emprunt est dépassé."):
        super().__init__(message)
