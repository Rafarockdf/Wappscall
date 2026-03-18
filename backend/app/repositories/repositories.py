from backend.app.repositories.base_repo import BaseRepo
from backend.database.models.models import User, Funcionario, gastos, ErrosScraping
from sqlalchemy.orm import Session

class UserRepo(BaseRepo[User]):
    def __init__(self):
        super().__init__(User)
        
    def buscar_por_email(self, db: Session, email: str) -> User:
        return db.query(self.model).filter(self.model.email == email).first()
    
class FuncionarioRepo(BaseRepo[Funcionario]):
    def __init__(self):
        super().__init__(Funcionario)
        
class GastosRepo(BaseRepo[gastos]):
    def __init__(self):
        super().__init__(gastos)
        
class ErrosScrapingRepo(BaseRepo[ErrosScraping]):
    def __init__(self):
        super().__init__(ErrosScraping)
        
user_repo = UserRepo()
funcionario_repo = FuncionarioRepo()
gastos_repo = GastosRepo()
erros_scraping_repo = ErrosScrapingRepo()