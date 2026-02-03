from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

from backend.database.config.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    salario = Column(Float, nullable=False)
    data_contratacao = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    owner = relationship("User", back_populates="items")

class gastos(Base):
    __tablename__ = 'gastos'
    
    id = Column(Integer, primary_key=True, index=True)
    motivo = Column(String, nullable=False) # Ex: Alimentação, Transporte, etc.
    descricao = Column(String, nullable=False) # Detalhes do gasto
    valor = Column(Float, nullable=False)
    data = Column(DateTime, nullable=False)
    # Local = Definir se será coordenada ou string
    empresa = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    razao_social = Column(String, nullable=False)
    ramo_atividade = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    tipo_gasto = Column(String, nullable=False)  # Ex: Dinheiro Empresa, Dinheiro Funcionário, etc.

    arquivo_extracao = Column(String, nullable=True) # Caminho para o arquivo scrape

    boolean_aprovado = Column(Boolean, default=False)
    data_aprovacao = Column(DateTime, nullable=True)

    boolean_extornado = Column(Boolean, default=False)
    data_extorno = Column(DateTime, nullable=True)

    usuario_id = Column(Integer, ForeignKey('users.id'))
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'))


    Funcionario = relationship("Funcionario", back_populates="gastos")
    User = relationship("User", back_populates="gastos")
    


class ErrosScraping(Base):
    __tablename__ = 'erros_scraping'
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_erro = Column(String, nullable=False)
    descricao_erro = Column(String, nullable=False)
    data_ocorrencia = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    arquivo_log = Column(String, nullable=True)  # Caminho para o arquivo de log, se aplicável
    arquivo_extracao = Column(String, nullable=True)  # Caminho para o arquivo scrape
    