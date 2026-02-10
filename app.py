from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import sqlite3
import socket
from datetime import datetime, date
import json

# Importar seus módulos existentes
import banco
import atividades
import progresso
import usuarios

app = Flask(__name__)
app.secret_key = 'sistema_educacional_secret_key_2024'

# ==================== FUNÇÕES AUXILIARES ====================

def get_ip():
    """Obtém IP local para compartilhamento em rede"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def conectar():
    """Conexão com banco"""
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== DECORADORES ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'cpf' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def aluno_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != '1':
            flash('Acesso restrito a alunos!', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def professor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != '2':
            flash('Acesso restrito a professores!', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def coordenador_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != '3':
            flash('Acesso restrito a coordenadores!', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/')
def index():
    if 'cpf' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']
        tipo = request.form['tipo']
        
        # Usar sua função existente
        if usuarios.cpf_existe(cpf):
            # Verificar senha
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM usuarios WHERE cpf = ? AND senha = ?", (cpf, senha))
            check = cursor.fetchone()
            conn.close()
            
            if check:
                # Pegar nome do usuário
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT nome, tipo FROM usuarios WHERE cpf = ?", (cpf,))
                user = cursor.fetchone()
                conn.close()
                
                if str(user['tipo']) == tipo:
                    session['cpf'] = cpf
                    session['nome'] = user['nome']
                    session['tipo'] = tipo
                    flash(f'Bem-vindo, {user["nome"]}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Tipo de usuário incorreto!', 'danger')
            else:
                flash('Senha incorreta!', 'danger')
        else:
            flash('CPF não cadastrado!', 'danger')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
@login_required
@coordenador_required
def cadastro():
    if request.method == 'POST':
        # Coletar dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        tipo = request.form['tipo']
        
        # Validar CPF
        if not cpf.isdigit() or len(cpf) != 11:
            flash('CPF deve ter 11 dígitos numéricos!', 'danger')
            return redirect(url_for('cadastro'))
        
        if usuarios.cpf_existe(cpf):
            flash('CPF já cadastrado!', 'danger')
            return redirect(url_for('cadastro'))
        
        if usuarios.email_existe(email):
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('cadastro'))
        
        # Gerar senha automática
        senha = (nome[:3]) + "@" + (str(cpf)[-4:])
        
        # Inserir no banco
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, cpf, senha, tipo) VALUES (?, ?, ?, ?, ?)",
            (nome, email, cpf, senha, int(tipo) - 1)
        )
        
        # Se for aluno, matricular em curso
        if tipo == "1":
            cursos = request.form.getlist('cursos')
            for curso_id in cursos:
                cursor.execute(
                    "INSERT INTO usuario_curso (id_usuario, id_curso) VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?), ?)",
                    (cpf, curso_id)
                )
        
        conn.commit()
        conn.close()
        
        flash(f'Usuário cadastrado! Senha: {senha}', 'success')
        return redirect(url_for('cadastro'))
    
    # Listar cursos para seleção
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_curso, nome FROM cursos ORDER BY nome")
    cursos = cursor.fetchall()
    conn.close()
    
    return render_template('cadastro.html', cursos=cursos)

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

# ==================== DASHBOARDS ====================

@app.route('/dashboard')
@login_required
def dashboard():
    tipo = session['tipo']
    if tipo == '1':
        return redirect(url_for('aluno_dashboard'))
    elif tipo == '2':
        return redirect(url_for('professor_dashboard'))
    else:
        return redirect(url_for('coordenador_dashboard'))

# ==================== ROTAS DO ALUNO ====================

@app.route('/aluno')
@login_required
@aluno_required
def aluno_dashboard():
    cpf = session['cpf']
    
    # Estatísticas
    conn = conectar()
    cursor = conn.cursor()
    
    # Total de estrelas
    cursor.execute("""
        SELECT COUNT(CASE WHEN ua.acerto = 1 THEN 1 END) as estrelas
        FROM usuario_atividade ua
        INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
        WHERE u.cpf = ?
    """, (cpf,))
    estrelas = cursor.fetchone()['estrelas'] or 0
    
    # Atividades hoje
    hoje = str(date.today())
    cursor.execute("""
        SELECT COUNT(*) as hoje
        FROM usuario_atividade ua
        INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
        WHERE u.cpf = ? AND ua.data = ?
    """, (cpf, hoje))
    atividades_hoje = cursor.fetchone()['hoje'] or 0
    
    # Total de cursos
    cursor.execute("""
        SELECT COUNT(*) as total FROM usuario_curso uc
        INNER JOIN usuarios u ON uc.id_usuario = u.id_usuario
        WHERE u.cpf = ?
    """, (cpf,))
    total_cursos = cursor.fetchone()['total'] or 0
    
    # Ranking top 3
    cursor.execute("""
        SELECT u.nome, COUNT(CASE WHEN ua.acerto = 1 THEN 1 END) as estrelas
        FROM usuarios u
        LEFT JOIN usuario_atividade ua ON ua.id_usuario = u.id_usuario
        WHERE u.tipo = 0
        GROUP BY u.id_usuario
        ORDER BY estrelas DESC
        LIMIT 3
    """)
    ranking = cursor.fetchall()
    
    conn.close()
    
    return render_template('aluno/dashboard.html',
                         estrelas=estrelas,
                         atividades_hoje=atividades_hoje,
                         total_cursos=total_cursos,
                         ranking=ranking)

@app.route('/aluno/cursos')
@login_required
@aluno_required
def aluno_cursos():
    cpf = session['cpf']
    
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.id_curso, c.nome, c.horario,
               (SELECT COUNT(*) FROM atividades WHERE id_curso = c.id_curso) as total_atividades,
               (SELECT COUNT(*) FROM usuario_atividade ua 
                INNER JOIN atividades a ON ua.id_atividade = a.id_atividade
                INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
                WHERE a.id_curso = c.id_curso AND u.cpf = ?) as feitas
        FROM cursos c
        INNER JOIN usuario_curso uc ON c.id_curso = uc.id_curso
        INNER JOIN usuarios u ON uc.id_usuario = u.id_usuario
        WHERE u.cpf = ?
        ORDER BY c.nome
    """, (cpf, cpf))
    
    cursos = cursor.fetchall()
    conn.close()
    
    return render_template('aluno/cursos.html', cursos=cursos)

@app.route('/aluno/atividade/<int:curso_id>')
@login_required
@aluno_required
def aluno_atividade(curso_id):
    cpf = session['cpf']
    
    # Verificar se está matriculado
    if not usuarios.checar_uc(cpf, curso_id):
        flash('Você não está matriculado neste curso!', 'danger')
        return redirect(url_for('aluno_cursos'))
    
    conn = conectar()
    cursor = conn.cursor()
    
    # Buscar atividade não feita
    cursor.execute("""
        SELECT a.*, c.nome as curso_nome
        FROM atividades a
        INNER JOIN cursos c ON a.id_curso = c.id_curso
        WHERE a.id_curso = ?
        AND a.id_atividade NOT IN (
            SELECT ua.id_atividade 
            FROM usuario_atividade ua
            INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
            WHERE u.cpf = ?
        )
        ORDER BY RANDOM()
        LIMIT 1
    """, (curso_id, cpf))
    
    atividade = cursor.fetchone()
    
    # Se não houver atividades, buscar todas para permitir refazer
    if not atividade:
        cursor.execute("""
            SELECT a.*, c.nome as curso_nome
            FROM atividades a
            INNER JOIN cursos c ON a.id_curso = c.id_curso
            WHERE a.id_curso = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (curso_id,))
        atividade = cursor.fetchone()
        ja_feita = True
    else:
        ja_feita = False
    
    conn.close()
    
    if not atividade:
        flash('Nenhuma atividade disponível neste curso!', 'info')
        return redirect(url_for('aluno_cursos'))
    
    return render_template('aluno/atividade.html', 
                         atividade=atividade, 
                         curso_id=curso_id,
                         ja_feita=ja_feita)

@app.route('/aluno/responder', methods=['POST'])
@login_required
@aluno_required
def aluno_responder():
    cpf = session['cpf']
    atividade_id = request.form['atividade_id']
    resposta = request.form['resposta'].lower().strip()
    
    # Verificar se já foi feita
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM usuario_atividade ua
        INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
        WHERE u.cpf = ? AND ua.id_atividade = ?
    """, (cpf, atividade_id))
    ja_feita = cursor.fetchone()
    conn.close()
    
    if ja_feita:
        # Atualizar
        atividades.repetir_atividade(cpf, atividade_id, resposta)
    else:
        # Inserir nova
        atividades.realizar_atividade(cpf, atividade_id, resposta)
    
    # Verificar se acertou
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT gabarito FROM atividades WHERE id_atividade = ?", (atividade_id,))
    gabarito = cursor.fetchone()['gabarito']
    conn.close()
    
    acertou = resposta == gabarito
    
    return jsonify({
        'acertou': acertou,
        'gabarito': gabarito,
        'mensagem': 'Parabéns! +1 ⭐' if acertou else 'Resposta incorreta!'
    })

@app.route('/aluno/dica/<int:atividade_id>')
@login_required
@aluno_required
def aluno_dica(atividade_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT dica FROM atividades WHERE id_atividade = ?", (atividade_id,))
    dica = cursor.fetchone()['dica']
    conn.close()
    return jsonify({'dica': dica})

@app.route('/aluno/progresso')
@login_required
@aluno_required
def aluno_progresso():
    cpf = session['cpf']
    
    # Estatísticas gerais
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN ua.acerto = 1 THEN 1 END) as estrelas,
            COUNT(*) as total,
            SUM(CASE WHEN ua.acerto = 1 THEN 1 ELSE 0 END) as acertos
        FROM usuario_atividade ua
        INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
        WHERE u.cpf = ?
    """, (cpf,))
    stats = cursor.fetchone()
    
    # Por curso
    cursor.execute("""
        SELECT c.nome,
               COUNT(CASE WHEN ua.acerto = 1 THEN 1 END) as estrelas,
               COUNT(*) as total
        FROM cursos c
        LEFT JOIN atividades a ON c.id_curso = a.id_curso
        LEFT JOIN usuario_atividade ua ON a.id_atividade = ua.id_atividade
        LEFT JOIN usuarios u ON ua.id_usuario = u.id_usuario AND u.cpf = ?
        GROUP BY c.id_curso
        HAVING total > 0
    """, (cpf,))
    por_curso = cursor.fetchall()
    
    conn.close()
    
    return render_template('aluno/progresso.html', stats=stats, por_curso=por_curso)

@app.route('/aluno/ranking')
@login_required
@aluno_required
def aluno_ranking():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.nome,
               COUNT(CASE WHEN ua.acerto = 1 THEN 1 END) as estrelas,
               COUNT(*) as atividades
        FROM usuarios u
        LEFT JOIN usuario_atividade ua ON ua.id_usuario = u.id_usuario
        WHERE u.tipo = 0
        GROUP BY u.id_usuario
        ORDER BY estrelas DESC
    """)
    
    ranking = cursor.fetchall()
    conn.close()
    
    return render_template('aluno/ranking.html', ranking=ranking)

@app.route('/aluno/resetar/<int:curso_id>', methods=['POST'])
@login_required
@aluno_required
def aluno_resetar(curso_id):
    cpf = session['cpf']
    progresso.resetar_progresso(cpf, curso_id)
    flash('Progresso resetado com sucesso!', 'success')
    return redirect(url_for('aluno_progresso'))

# ==================== ROTAS DO PROFESSOR ====================

@app.route('/professor')
@login_required
@professor_required
def professor_dashboard():
    cpf = session['cpf']
    
    conn = conectar()
    cursor = conn.cursor()
    
    # Estatísticas
    cursor.execute("""
        SELECT COUNT(*) as meus FROM cursos c
        INNER JOIN usuario_curso uc ON c.id_curso = uc.id_curso
        INNER JOIN usuarios u ON uc.id_usuario = u.id_usuario
        WHERE u.cpf = ?
    """, (cpf,))
    meus_cursos = cursor.fetchone()['meus']
    
    cursor.execute("SELECT COUNT(*) as total FROM atividades")
    total_atividades = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM cursos")
    total_cursos = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('professor/dashboard.html',
                         meus_cursos=meus_cursos,
                         total_atividades=total_atividades,
                         total_cursos=total_cursos)

@app.route('/professor/curso/<int:curso_id>', methods=['GET', 'POST'])
@login_required
@professor_required
def professor_curso(curso_id):
    cpf = session['cpf']
    
    # Verificar se leciona no curso
    if not usuarios.checar_uc(cpf, curso_id):
        flash('Você não leciona neste curso!', 'danger')
        return redirect(url_for('professor_dashboard'))
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        
        if acao == 'adicionar':
            # Adicionar atividade via seu módulo
            questao = request.form['questao']
            a = request.form['a']
            b = request.form['b']
            c = request.form['c']
            d = request.form['d']
            dica = request.form['dica']
            gabarito = request.form['gabarito']
            
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO atividades (questao, A, B, C, D, dica, gabarito, id_curso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (questao, a, b, c, d, dica, gabarito, curso_id))
            conn.commit()
            conn.close()
            
            flash('Atividade adicionada com sucesso!', 'success')
            
        elif acao == 'deletar':
            atividade_id = request.form['atividade_id']
            atividades.deletar_atividade(atividade_id)
            flash('Atividade deletada!', 'success')
    
    # Listar atividades do curso
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome FROM cursos WHERE id_curso = ?", (curso_id,))
    curso_nome = cursor.fetchone()['nome']
    
    cursor.execute("""
        SELECT * FROM atividades WHERE id_curso = ? ORDER BY id_atividade DESC
    """, (curso_id,))
    atividades_lista = cursor.fetchall()
    
    conn.close()
    
    return render_template('professor/curso.html',
                         curso_id=curso_id,
                         curso_nome=curso_nome,
                         atividades=atividades_lista)

@app.route('/professor/adicionar_curso', methods=['POST'])
@login_required
@professor_required
def professor_adicionar_curso():
    cpf = session['cpf']
    nome = request.form['nome']
    horario = request.form['horario']
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cursos (nome, horario) VALUES (?, ?)", (nome, horario))
    cursor.execute("""
        INSERT INTO usuario_curso (id_usuario, id_curso) 
        VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?), last_insert_rowid())
    """, (cpf,))
    conn.commit()
    conn.close()
    
    flash('Curso adicionado com sucesso!', 'success')
    return redirect(url_for('professor_dashboard'))

# ==================== ROTAS DO COORDENADOR ====================

@app.route('/coordenador')
@login_required
@coordenador_required
def coordenador_dashboard():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM usuarios WHERE tipo = 0")
    total_alunos = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM atividades")
    total_atividades = cursor.fetchone()['total']
    
    hoje = str(date.today())
    cursor.execute("""
        SELECT COUNT(*) as total FROM usuario_atividade WHERE data = ?
    """, (hoje,))
    atividades_hoje = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT COUNT(CASE WHEN acerto = 1 THEN 1 END) as total FROM usuario_atividade
    """)
    total_estrelas = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('coordenador/dashboard.html',
                         total_alunos=total_alunos,
                         total_atividades=total_atividades,
                         atividades_hoje=atividades_hoje,
                         total_estrelas=total_estrelas)

@app.route('/coordenador/ranking')
@login_required
@coordenador_required
def coordenador_ranking():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.nome,
               COUNT(CASE WHEN ua.acerto = 1 THEN 1 END) as estrelas,
               COUNT(*) as feitas,
               SUM(CASE WHEN ua.acerto = 1 THEN 1 ELSE 0 END) as acertos
        FROM usuarios u
        LEFT JOIN usuario_atividade ua ON ua.id_usuario = u.id_usuario
        WHERE u.tipo = 0
        GROUP BY u.id_usuario
        ORDER BY estrelas DESC
    """)
    
    ranking = cursor.fetchall()
    conn.close()
    
    return render_template('coordenador/ranking.html', ranking=ranking)

@app.route('/coordenador/relatorios')
@login_required
@coordenador_required
def coordenador_relatorios():
    # Desempenho por curso
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.nome,
               COUNT(DISTINCT ua.id_usuario) as alunos,
               COUNT(*) as tentativas,
               SUM(CASE WHEN ua.acerto = 1 THEN 1 ELSE 0 END) as acertos
        FROM cursos c
        LEFT JOIN atividades a ON c.id_curso = a.id_curso
        LEFT JOIN usuario_atividade ua ON a.id_atividade = ua.id_atividade
        GROUP BY c.id_curso
    """)
    por_curso = cursor.fetchall()
    
    # Atividades de hoje
    hoje = str(date.today())
    cursor.execute("""
        SELECT u.nome, COUNT(*) as quantidade
        FROM usuario_atividade ua
        INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
        WHERE ua.data = ?
        GROUP BY u.id_usuario
        ORDER BY quantidade DESC
    """, (hoje,))
    atividades_hoje = cursor.fetchall()
    
    conn.close()
    
    return render_template('coordenador/relatorios.html',
                         por_curso=por_curso,
                         atividades_hoje=atividades_hoje)

# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    banco.criar_tabela()
    
    ip = get_ip()
    porta = 5000
    
    print("\n" + "="*60)
    print("  🎓 SISTEMA EDUCACIONAL - MODO REDE LOCAL")
    print("="*60)
    print(f"\n  💻 Neste computador: http://localhost:{porta}")
    print(f"  🌐 Outros dispositivos: http://{ip}:{porta}")
    print(f"\n  📱 Compartilhe este endereço: {ip}:{porta}")
    print("="*60)
    print("  ⚠️  Requisitos:")
    print("     • Mesma rede WiFi/cabo")
    print("     • Firewall liberado (porta 5000)")
    print("     • Manter este programa aberto")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=porta, debug=False, threaded=True)