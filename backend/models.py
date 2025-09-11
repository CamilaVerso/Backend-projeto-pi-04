from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Gestante(db.Model):
    __tablename__ = 'gestantes'  
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)  
    nome = db.Column(db.String(100), nullable=False)  
    data_nascimento = db.Column(db.Date, nullable=False)  
    idade = db.Column(db.Integer)  
    nome_mae = db.Column(db.String(100), nullable=False)  
    data_prevista_parto = db.Column(db.Date, nullable=False)  
    ultima_menstruacao = db.Column(db.Date, nullable=False)  
    endereco = db.Column(db.String(200), nullable=False) 
    cep = db.Column(db.String(8), nullable=False)  
    cidade = db.Column(db.String(100), nullable=False)  
    estado = db.Column(db.String(100), nullable=False)  
    telefone = db.Column(db.String(20), nullable=False)  

    
    exames = db.relationship('Exame', back_populates='gestante', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "cpf": self.cpf,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            "idade": self.idade,
            "nome_mae": self.nome_mae,
            "data_prevista_parto": self.data_prevista_parto.strftime('%Y-%m-%d') if self.data_prevista_parto else None,
            "ultima_menstruacao": self.ultima_menstruacao.strftime('%Y-%m-%d') if self.ultima_menstruacao else None,
            "endereco": self.endereco,
            "cep": self.cep,
            "cidade": self.cidade,
            "estado": self.estado,
            "telefone": self.telefone
        }


class Exame(db.Model):
    __tablename__ = 'exames'  
    id = db.Column(db.Integer, primary_key=True)
    gestante_id = db.Column(db.Integer, db.ForeignKey('gestantes.id'))  
    nome = db.Column(db.String(50))  
    data = db.Column(db.Date)  
    status = db.Column(db.String(20))  
    cor_status = db.Column(db.String(7))  

    
    gestante = db.relationship('Gestante', back_populates='exames')

    def to_dict(self):
        return {
            "id": self.id,
            "gestante_id": self.gestante_id,
            "nome": self.nome,
            "data": self.data.strftime('%Y-%m-%d') if self.data else None,
            "status": self.status,
            "cor_status": self.cor_status
        }
