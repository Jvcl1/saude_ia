# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Banco de dados simples (em produção, use um banco de dados real)
users = {
    "user@example.com": {
        "password": "senha123",
        "name": "Usuário Teste"
    }
}

symptoms_db = {
    "headache": {
        "description": "Dor de cabeça",
        "possible_causes": ["Tensão", "Enxaqueca", "Sinusite", "Problemas de visão"],
        "recommendations": ["Repousar", "Beber água", "Consultar médico se persistir"]
    },
    "nausea": {
        "description": "Enjoo",
        "possible_causes": ["Labirintite", "Gravidez", "Intoxicação alimentar", "Enxaqueca"],
        "recommendations": ["Evitar movimentos bruscos", "Ingerir líquidos aos poucos", "Consultar médico"]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email]['password'] == password:
            session['user_email'] = email
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Credenciais inválidas")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form.get('name', '')
        
        if email in users:
            return render_template('register.html', error="E-mail já cadastrado")
        
        users[email] = {"password": password, "name": name}
        session['user_email'] = email
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user_email = session['user_email']
    user_name = users.get(user_email, {}).get('name', 'Usuário')
    
    return render_template('dashboard.html', user_name=user_name)

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_email' not in session:
        return jsonify({"error": "Não autenticado"}), 401
    
    data = request.json
    user_message = data.get('message', '').lower()
    
    response = "Desculpe, não entendi. Poderia descrever melhor seus sintomas?"
    
    for symptom in symptoms_db:
        if symptom in user_message:
            info = symptoms_db[symptom]
            causes = ", ".join(info['possible_causes'])
            recommendations = ", ".join(info['recommendations'])
            response = f"Para {info['description']}, possíveis causas: {causes}. Recomendações: {recommendations}."
            break
    
    return jsonify({"response": response})

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user_email = session['user_email']
    user_data = users.get(user_email, {})
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        password = request.form.get('password', '')
        
        if name:
            user_data['name'] = name
        if password:
            user_data['password'] = password
        
        users[user_email] = user_data
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user_data=user_data)

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)