import os
import datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import json
import sqlite3

import logging



app = Flask(__name__)
CORS(app)


handler = logging.FileHandler('logs/flask_app.log')  # Log to a file
app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
app.logger.addHandler(handler)


# Crie uma métrica de exemplo (contador de requisições)
REQUEST_COUNT = Counter('http_requests_total', 'Total de requisições HTTP', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Latência das requisições HTTP em segundos', ['method', 'endpoint'])
HTTP_ERRORS = Counter('http_errors_total', 'Total de respostas HTTP com erro', ['method', 'endpoint', 'status_code'])


def log_message(level, message):
    """Loga uma mensagem com o nível especificado."""

    log_methods = {
        'debug': app.logger.debug,
        'info': app.logger.info,
        'warning': app.logger.warning,
        'error': app.logger.error,
        'critical': app.logger.critical
    }
    if level in log_methods:
        log_methods[level](f"{message}")
    else:
        app.logger.error(f"Unrecognized logging level: {level}")


# Middleware para contar requisições
@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

# Rota para o Prometheus coletar as métricas
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Endpoint para devolver todos os imoveis cadastrados
@app.route('/')
def home():
    '''
    log_message('info', 'This is an INFO message')
    log_message('debug', 'This is a DEBUG message')
    log_message('warning', 'This is a WARNING message')
    log_message('error', 'This is an ERROR message')
    log_message('critical', 'This is a CRITICAL message')

    '''
    log_message('info', '/')
    return "API de imoveis"

@app.route('/imoveis', methods=['GET'])
def imoveis():
    log_message('info', 'acessando /imoveis')
    try:
        with sqlite3.connect('imobiliaria_mackenzie.db') as conn:
            conn.row_factory = sqlite3.Row
            log_message('info', 'Conectando no banco de dados: imobiliaria_mackenzie.db...')
            cursor = conn.cursor()
            log_message('info', 'Executando a consulta de SELECT...')
            cursor.execute('''SELECT contrato, nome, endereco, metragem, comodos, garagem FROM imovel''')
            result = cursor.fetchall()
            log_message('info', 'Consulta realizada com sucesso.') 
            return json.dumps([dict(ix) for ix in result]), 200
    except Exception as e:
        log_message('error', 'Erro ao listar todos os imoveis em /imoveis')
        return jsonify(error=str(e)), 500

@app.route('/imovel/<contrato>', methods=['GET', 'DELETE'])
def imovel_por_contrato(contrato):
    log_message('info', '/imovel/' + str(contrato))
    try:
        with sqlite3.connect('imobiliaria_mackenzie.db') as conn:
            conn.row_factory = sqlite3.Row
            log_message('info', 'Conectando no banco de dados: imobiliaria_mackenzie.db...')
            cursor = conn.cursor()
            if request.method == 'GET':
                log_message('info', 'Executando a consulta de SELECT...')
                cursor.execute('''SELECT contrato, nome, endereco, metragem, comodos, garagem FROM imovel WHERE nome=?''', [contrato])
                result = cursor.fetchall()
                log_message('info', 'Consulta realizada com sucesso.') 
                if result:
                    return json.dumps([dict(ix) for ix in result]), 200
                return jsonify(error="Imovel não encontrado"), 404
            elif request.method == 'DELETE':
                log_message('info', 'Executando a consulta de DELETE...')
                cursor.execute('DELETE FROM imovel WHERE contrato = ?', (contrato,))
                if cursor.rowcount == 0:
                    return jsonify(error="Contrato não encontrado"), 404
                conn.commit()
                return jsonify(success="Imovel deletado com sucesso"), 200
    except Exception as e:
        log_message('error', '/imovel/' + str(contrato))
        return jsonify(error=str(e)), 500

@app.route('/imovel', methods=['POST'])
def insere_atualiza_imovel():

    log_message('info', '/imovel POST')

    data = request.get_json(force=True)
    contrato = data.get('contrato')
    nome = data.get('nome')
    endereco = data.get('endereco')
    metragem = data.get('metragem')
    comodos = data.get('comodos')
    garagem = data.get('garagem')

    try:
        with sqlite3.connect('imobiliaria_mackenzie.db') as conn:
            log_message('info', 'Conectando no banco de dados: imobiliaria_mackenzie.db...')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            log_message('info', 'Verificando se o imovel existe...')
            cursor.execute('SELECT 1 FROM imovel WHERE contrato = ?', (contrato,))
            exists = cursor.fetchone()
            if exists:
                log_message('info', 'Executando UPDATE...')
                cursor.execute('UPDATE imovel SET contrato=?, nome=?, endereco=?, metragem=?, comodos=?, garagem=? WHERE contrato=?', (contrato, nome, endereco, metragem, comodos, garagem, contrato))
                conn.commit()
                return jsonify(success="Imovel atualizado com sucesso"), 200
            log_message('info', 'Executando INSERT do imovel...' + str(contrato))
            cursor.execute('INSERT INTO imovel (contrato, nome, endereco, metragem, comodos, garagem) VALUES (?, ?, ?, ?, ?, ?)', (contrato, nome, endereco, metragem, comodos, garagem))
            conn.commit()
            return jsonify(success="Imovel inserido com sucesso"), 201
    except Exception as e:
        log_message('error', '/imovel/POST')
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)