import traceback
import os
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from functools import wraps
import re

app = Flask(__name__)

instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')

os.makedirs(instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "usuarios.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'erlandsonsilvadonascimento')

CORS(app, supports_credentials=True, origins=["http://localhost:5173"]) # Depois que fizer o deploy do front, precisarei mudar o endereço

db = SQLAlchemy(app)

class Usuario(db.Model):
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
    cronograma = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'idade': self.idade,
            'nome_mae': self.nome_mae,
            'data_prevista_parto': self.data_prevista_parto.strftime('%Y-%m-%d'),
            'ultima_menstruacao': self.ultima_menstruacao.strftime('%Y-%m-%d'),
            'endereco': self.endereco,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado': self.estado,
            'telefone': self.telefone,
            'cronograma': self.cronograma,
        }

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Acesso não autorizado'}), 401 
        return f(*args, **kwargs)
    return decorated_function

def parse_date_flexible(date_string):
    formats_to_try = [
        '%Y-%m-%d', 
        '%d/%m/%Y',  
    ]
    for fmt in formats_to_try:
        try:
            
            return datetime.strptime(date_string, fmt)
        except ValueError:           
            continue
    
    raise ValueError(f"Formato de data inválido: '{date_string}'. Use AAAA-MM-DD ou DD/MM/AAAA.")

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() 
    if not data:
        return jsonify({'error': 'Requisição inválida'}), 400

    username = os.getenv('APP_USERNAME', 'usuario')
    password = os.getenv('APP_PASSWORD', '123456')

    if data.get('username') == username and data.get('password') == password:
        session['user_id'] = data.get('username')
        return jsonify({'message': 'Login realizado com sucesso'}), 200
    else:
        return jsonify({'error': 'Usuário ou senha incorretos'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

@app.route('/api/status')
@login_required
def status():
   
    return jsonify({'message': 'Sessão ativa'}), 200


@app.route('/api/gestantes', methods=['POST'])
@login_required
def create_gestante():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    try:
        
        cpf_limpo = re.sub(r'\D', '', data.get('cpf', ''))

        if not cpf_limpo or len(cpf_limpo) != 11:
            return jsonify({'error': 'CPF inválido'}), 400
        
        if Usuario.query.filter_by(cpf=cpf_limpo).first():
            return jsonify({'error': 'CPF já cadastrado'}), 409

        data_nascimento = parse_date_flexible(data.get('data_nascimento'))
        idade = (datetime.now() - data_nascimento).days // 365
        
        novo_usuario = Usuario(
            cpf=cpf_limpo,
            nome=data.get('nome'),
            data_nascimento=data_nascimento,
            idade=idade,
            nome_mae=data.get('nome_mae'),
            data_prevista_parto=parse_date_flexible(data.get('data_prevista_parto')),
            ultima_menstruacao=parse_date_flexible(data.get('ultima_menstruacao')),
            endereco=data.get('endereco'),
            cep=data.get('cep'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            telefone=data.get('telefone'),
            cronograma=data.get('cronograma')
        )
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify(novo_usuario.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno ao cadastrar', 'details': str(e)}), 500


@app.route('/api/gestantes', methods=['GET'])
@login_required
def get_all_gestantes():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200


@app.route('/api/gestantes/<cpf>', methods=['GET'])
@login_required
def get_gestante_by_cpf(cpf):
    cpf_limpo = re.sub(r'\D', '', cpf)

    usuario = Usuario.query.filter_by(cpf=cpf_limpo).first()
    if usuario:
        return jsonify(usuario.to_dict()), 200
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
@app.route('/api/gestantes/<cpf>', methods=['PUT'])
@login_required
def update_gestante(cpf):
    cpf_limpo = re.sub(r'\D', '', cpf)
    usuario = Usuario.query.filter_by(cpf=cpf_limpo).first_or_404()
    
    data = request.get_json()

    if 'cronograma' in data:
        usuario.cronograma = data['cronograma']

    db.session.commit()
    
    return jsonify(usuario.to_dict()), 200


if __name__ == '__main__':
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)
  