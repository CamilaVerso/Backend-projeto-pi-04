import traceback
import os
import re
import joblib
import pandas as pd
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Configuração de caminhos e banco de dados
instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "usuarios.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'erlandsonsilvadonascimento')

# Segurança de Cookies para o Render
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# Configuração de CORS para o seu Frontend no Render
CORS(app, supports_credentials=True, origins=["https://rede-cegonha-web.onrender.com", "http://localhost:5173", "http://localhost:3000"])

db = SQLAlchemy(app)

# --- MODELOS ---

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
            'id': self.id, 'cpf': self.cpf, 'nome': self.nome,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'idade': self.idade, 'nome_mae': self.nome_mae,
            'data_prevista_parto': self.data_prevista_parto.strftime('%Y-%m-%d'),
            'ultima_menstruacao': self.ultima_menstruacao.strftime('%Y-%m-%d'),
            'endereco': self.endereco, 'cep': self.cep, 'cidade': self.cidade,
            'estado': self.estado, 'telefone': self.telefone, 'cronograma': self.cronograma,
        }

class SinaisVitais(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_cpf = db.Column(db.String(11), db.ForeignKey('usuario.cpf'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    batimentos_cardiacos = db.Column(db.Float)
    oxigenacao_sangue = db.Column(db.Float)
    pressao_sistolica = db.Column(db.Integer)
    pressao_diastolica = db.Column(db.Integer)

with app.app_context():
    db.create_all()

# --- UTILITÁRIOS ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Acesso não autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def parse_date_flexible(date_string):
    formats_to_try = ['%Y-%m-%d', '%d/%m/%Y']
    for fmt in formats_to_try:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"Formato de data inválido: {date_string}")

# --- ROTAS ---

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = os.getenv('APP_USERNAME', 'usuario')
    password = os.getenv('APP_PASSWORD', '123456')
    if data and data.get('username') == username and data.get('password') == password:
        session['user_id'] = data.get('username')
        return jsonify({'message': 'Login realizado com sucesso'}), 200
    return jsonify({'error': 'Usuário ou senha incorretos'}), 401

@app.route('/api/gestantes', methods=['POST', 'GET'])
@login_required
def gerenciar_gestantes():
    if request.method == 'POST':
        data = request.get_json()
        try:
            cpf_limpo = re.sub(r'\D', '', data.get('cpf', ''))
            data_nasc = parse_date_flexible(data.get('data_nascimento'))
            novo = Usuario(
                cpf=cpf_limpo, nome=data.get('nome'), data_nascimento=data_nasc,
                idade=(datetime.now() - data_nasc).days // 365,
                nome_mae=data.get('nome_mae'),
                data_prevista_parto=parse_date_flexible(data.get('data_prevista_parto')),
                ultima_menstruacao=parse_date_flexible(data.get('ultima_menstruacao')),
                endereco=data.get('endereco'), cep=data.get('cep'),
                cidade=data.get('cidade'), estado=data.get('estado'),
                telefone=data.get('telefone'), cronograma=data.get('cronograma')
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify(novo.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios]), 200

@app.route('/api/gestantes/<cpf>', methods=['GET', 'PUT'])
@login_required
def detalhe_gestante(cpf):
    cpf_limpo = re.sub(r'\D', '', cpf)
    usuario = Usuario.query.filter_by(cpf=cpf_limpo).first_or_404()
    if request.method == 'PUT':
        data = request.get_json()
        if 'cronograma' in data:
            usuario.cronograma = data['cronograma']
        db.session.commit()
    return jsonify(usuario.to_dict()), 200

@app.route('/api/sinais-vitais/<cpf>', methods=['POST', 'GET'])
@login_required
def sinais_vitais(cpf):
    cpf_limpo = re.sub(r'\D', '', cpf)
    if request.method == 'POST':
        data = request.get_json()
        novo = SinaisVitais(
            usuario_cpf=cpf_limpo,
            batimentos_cardiacos=data['batimentos'],
            oxigenacao_sangue=data['oxigenacao'],
            pressao_sistolica=data['pressao_sistolica'],
            pressao_diastolica=data['pressao_diastolica']
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'message': 'Dados recebidos'}), 201
    sinais = SinaisVitais.query.filter_by(usuario_cpf=cpf_limpo).all()
    return jsonify([{
        'timestamp': s.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'batimentos': s.batimentos_cardiacos,
        'oxigenacao': s.oxigenacao_sangue,
        'pressao_sistolica': s.pressao_sistolica,
        'pressao_diastolica': s.pressao_diastolica
    } for s in sinais]), 200

@app.route('/api/risco/<cpf>', methods=['GET'])
@login_required
def prever_risco(cpf):
    model_path = os.path.join(instance_path, 'risk_model.joblib')
    if not os.path.exists(model_path):
        return jsonify({'error': 'Modelo de IA não encontrado'}), 500
    
    model = joblib.load(model_path)
    cpf_limpo = re.sub(r'\D', '', cpf)
    usuario = Usuario.query.filter_by(cpf=cpf_limpo).first()
    sinais = SinaisVitais.query.filter_by(usuario_cpf=cpf_limpo).all()

    if not usuario or not sinais:
        return jsonify({'error': 'Dados insuficientes'}), 404
    
    sinais_df = pd.DataFrame([{'bat': s.batimentos_cardiacos, 'oxi': s.oxigenacao_sangue, 'sis': s.pressao_sistolica, 'dia': s.pressao_diastolica} for s in sinais])
    
    dados_para_prever = pd.DataFrame([[
        usuario.idade, sinais_df['bat'].mean(), sinais_df['oxi'].mean(),
        sinais_df['sis'].mean(), sinais_df['dia'].mean()
    ]], columns=['idade', 'batimentos_avg', 'oxigenacao_avg', 'pressao_sistolica_avg', 'pressao_diastolica_avg'])
    
    predicao = model.predict(dados_para_prever)
    return jsonify({'risco': predicao[0]}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
