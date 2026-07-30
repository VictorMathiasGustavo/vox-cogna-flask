from flask import Flask, render_template, request, jsonify
import pandas as pd
import unicodedata
import re
from pathlib import Path
from typing import List

app = Flask(__name__)

# ════════════════════════════════════════════════════════════════════════════
# LÓGICA DE BUSCA FUZZY
# ════════════════════════════════════════════════════════════════════════════

def normalizar(texto: str) -> str:
    """Remove acentos e converte para minúsculas"""
    if not texto:
        return ""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.lower().strip()

def levenshtein(a: str, b: str) -> int:
    """Calcula distância de Levenshtein entre duas strings"""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    
    if len(a) < len(b):
        a, b = b, a
    
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        curr = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            curr[j] = min(curr[j-1] + 1, prev[j] + 1, prev[j-1] + cost)
        prev = curr
    return prev[len(b)]

def similaridade(a: str, b: str) -> float:
    """Calcula similaridade 0-1 entre duas strings"""
    if not a or not b:
        return 0.0
    dist = levenshtein(a, b)
    max_len = max(len(a), len(b))
    return 1 - (dist / max_len) if max_len > 0 else 0.0

def busca_fuzzy(query: str, registros: List[dict], threshold: float = 0.65) -> List[dict]:
    """Filtra registros usando busca fuzzy"""
    if not query:
        return registros
    
    q_norm = normalizar(query)
    resultados = []
    
    for reg in registros:
        blob = normalizar(reg['tema'] + ' ' + reg['assunto'] + ' ' + reg['produto'])
        frase = normalizar(reg['fraseologia'])
        
        if q_norm in blob or q_norm in frase:
            resultados.append(reg)
            continue
        
        tokens = [t for t in blob.split() if len(t) >= 3]
        q_tokens = [t for t in q_norm.split() if len(t) >= 3]
        
        match = True
        for qt in q_tokens:
            encontrou = False
            for t in tokens:
                if qt in t or t in qt:
                    encontrou = True
                    break
                if abs(len(t) - len(qt)) <= max(2, int(len(qt) * 0.4)):
                    if similaridade(t, qt) >= threshold:
                        encontrou = True
                        break
            if not encontrou:
                match = False
                break
        
        if match:
            resultados.append(reg)
    
    return resultados

# ════════════════════════════════════════════════════════════════════════════
# CARREGAMENTO DE DADOS
# ════════════════════════════════════════════════════════════════════════════

def carregar_fraseologias() -> List[dict]:
    """Carrega fraseologias do Excel"""
    try:
        excel_path = Path(__file__).parent / "base_fraseologias.xlsx"
        if not excel_path.exists():
            excel_path = Path("/mnt/project/base_fraseologias.xlsx")
        
        if excel_path.exists():
            xl = pd.read_excel(excel_path, sheet_name=None)
            registros = []
            
            aba_map = {
                'EAD Legado': {'produto': 'EAD Legado'},
                'Presencial': {'produto': 'Presencial'},
                'N3 - PTC': {'produto': 'PTC'},
                'GERAIS': {'produto': 'Geral'},
                'MODERAÇÃO SIM OU NÃO': {'produto': 'Moderação'},
            }
            
            for nome_aba, df in xl.items():
                if nome_aba == "CAPA" or df.empty:
                    continue
                
                meta = aba_map.get(nome_aba, {'produto': nome_aba})
                
                for _, row in df.iterrows():
                    assunto = str(row.get('Assunto', '')).strip()
                    tema = str(row.get('Tema', '')).strip()
                    fraseologia = str(row.get('Fraseologia', '')).lstrip()
                    status = str(row.get('STATUS', '')).strip() if 'STATUS' in df.columns else ''
                    artigo = str(row.get('Artigo', '')).strip() if 'Artigo' in df.columns else ''
                    
                    # Validar artigo - só aceitar URLs válidas (http:// ou https://)
                    if artigo and not (artigo.lower().startswith('http://') or artigo.lower().startswith('https://')):
                        artigo = ''  # Se não for URL válida, deixar vazio
                    
                    if not fraseologia or fraseologia.lower() in ('nan', ''):
                        continue
                    
                    # Agrupa Moderação
                    if 'Moderação' in nome_aba or 'MODERAÇÃO' in nome_aba:
                        assunto_final = 'Moderação'
                    else:
                        assunto_final = assunto if assunto.lower() not in ('nan', '') else 'Geral'
                    
                    registros.append({
                        'produto': meta['produto'],
                        'assunto': assunto_final,
                        'tema': tema if tema.lower() not in ('nan', '') else 'Sem tema',
                        'fraseologia': fraseologia,
                        'status': status if status.lower() not in ('nan', '') else '',
                        'artigo': artigo,  # Já validado acima
                    })
            
            return registros if registros else []
    except Exception as e:
        print(f"Erro ao carregar Excel: {e}")
    
    return []

# Cache global
FRASEOLOGIAS = carregar_fraseologias()

# ════════════════════════════════════════════════════════════════════════════
# ROTAS FLASK
# ════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """Página principal"""
    if not FRASEOLOGIAS:
        return render_template('error.html', 
            erro="Nenhuma fraseologia encontrada. Verifique se 'base_fraseologias.xlsx' está no diretório.")
    
    # Métricas
    stats = {
        'total': len(FRASEOLOGIAS),
        'temas': len(set(f['tema'] for f in FRASEOLOGIAS)),
        'assuntos': len(set(f['assunto'] for f in FRASEOLOGIAS)),
    }
    
    # Opções de filtro
    produtos = sorted(set(f['produto'] for f in FRASEOLOGIAS))
    assuntos = sorted(set(f['assunto'] for f in FRASEOLOGIAS))
    
    return render_template('index.html', 
        fraseologias=FRASEOLOGIAS,
        stats=stats,
        produtos=produtos,
        assuntos=assuntos)

@app.route('/api/filtro', methods=['POST'])
def api_filtro():
    """API para filtrar fraseologias"""
    data = request.json
    produto = data.get('produto', 'Todos')
    assunto = data.get('assunto', 'Todos')
    busca = data.get('busca', '')
    
    # Aplica filtros
    resultado = FRASEOLOGIAS.copy()
    
    if produto != 'Todos':
        resultado = [f for f in resultado if f['produto'] == produto]
    
    if assunto != 'Todos':
        resultado = [f for f in resultado if f['assunto'] == assunto]
    
    if busca.strip():
        resultado = busca_fuzzy(busca.strip(), resultado, threshold=0.65)
    
    # Agrupa por assunto
    grupos = {}
    for r in resultado:
        assunto_grupo = r['assunto']
        if assunto_grupo not in grupos:
            grupos[assunto_grupo] = []
        grupos[assunto_grupo].append(r)
    
    return jsonify({
        'total': len(resultado),
        'grupos': grupos
    })

@app.route('/api/copy', methods=['POST'])
def api_copy():
    """API para copiar fraseologia"""
    data = request.json
    idx = data.get('idx')
    
    # Encontra a fraseologia
    for frase in FRASEOLOGIAS:
        if hash(frase['fraseologia']) == idx:
            return jsonify({
                'sucesso': True,
                'conteudo': frase['fraseologia']
            })
    
    return jsonify({'sucesso': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
