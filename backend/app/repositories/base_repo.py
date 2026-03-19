from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, Any, Dict

T = TypeVar('T')

class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
        
    def inserir(self, db: Session, obj_in: Dict[str, Any]) -> T:
        #cria um novo registro no banco de dados usando o modelo fornecido
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def buscar_por_id(self, db: Session, id: Any) -> T:
        #recupera um registro do banco de dados com base no ID fornecido
        return db.query(self.model).filter(self.model.id == id).first()
    
    def buscar_todos(self, db: Session, skip: int = 0, limit: int = 100) -> list[T]:
        #recupera todos os registros do banco de dados, com suporte para paginação
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def atualizar(self, db: Session, id: int, obj_in: Dict[str, Any]) -> T:
        #atualiza um registro existente no banco de dados com base no ID fornecido
        db_obj = self.buscar_por_id(db, id)
        if db_obj:
            for field, value in obj_in.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def deletar(self, db: Session, id: int) -> T:
        #deleta um registro do banco de dados com base no ID fornecido
        db_obj = self.buscar_por_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False