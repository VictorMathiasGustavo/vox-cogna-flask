from flask import Flask, render_template, request, jsonify
import pandas as pd
import unicodedata
from pathlib import Path
from typing import List

app = Flask(__name__, template_folder='templates', static_folder='static')

def normalizar(texto: str) -> str:
    """Remove acentos e converte para minúsculas"""
    if not texto or texto.lower() in ('nan', ''):
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn').lower()

def carregar_fraseologias() -> List[dict]:
    """Carrega fraseologias do Excel"""
    try:
        # Tentar vários caminhos possíveis
        caminhos_possiveis = [
            Path(__file__).parent / "base_fraseologias.xlsx",
            Path(__file__).parent / "base_de_frases.xlsx",
            Path("/mnt/project/base_fraseologias.xlsx"),
            Path("/mnt/project/base_de_frases.xlsx"),
            Path("/app/base_fraseologias.xlsx"),
            Path("/app/base_de_frases.xlsx"),
        ]
        
        excel_path = None
        for caminho in caminhos_possiveis:
            if caminho.exists():
                excel_path = caminho
                print(f"✅ Arquivo encontrado: {caminho}")
                break
        
        if not excel_path:
            print(f"❌ Nenhum arquivo Excel encontrado nos caminhos:")
            for c in caminhos_possiveis:
                print(f"   - {c}")
            return []
        
        xl = pd.read_excel(excel_path, sheet_name=None)
        registros = []
        
        # MAPEAMENTO COMPLETO DAS ABAS
        aba_map = {
            'EAD Legado': {'produto': 'EAD Legado'},
            'Presencial': {'produto': 'Presencial'},
            'PTC': {'produto': 'PTC'},
            'PÓS Graduação': {'produto': 'Pós-Graduação'},
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
                
                # Validar artigo - só aceitar URLs válidas
                if artigo and not (artigo.lower().startswith('http://') or artigo.lower().startswith('https://')):
                    artigo = ''
                
                if not fraseologia or fraseologia.lower() in ('nan', ''):
                    continue
                
                # Limpar tema - remover espaços extras e converter vazio para padrão
                if tema.lower() in ('nan', '') or not tema:
                    tema_final = 'Sem tema'
                else:
                    tema_final = tema
                
                # Agrupa Moderação
                if 'Moderação' in nome_aba or 'MODERAÇÃO' in nome_aba:
                    assunto_final = 'Moderação'
                else:
                    assunto_final = assunto if assunto.lower() not in ('nan', '') else 'Geral'
                
                registros.append({
                    'produto': meta['produto'],
                    'assunto': assunto_final,
                    'tema': tema_final,
                    'fraseologia': fraseologia,
                    'status': status if status.lower() not in ('nan', '') else '',
                    'artigo': artigo,
                })
        
        print(f"✅ Carregadas {len(registros)} fraseologias")
        return registros if registros else []
        
    except Exception as e:
        print(f"❌ Erro ao carregar Excel: {e}")
        import traceback
        traceback.print_exc()
    
    return []

# Cache de fraseologias
fraseologias_cache = carregar_fraseologias()

@app.route('/')
def index():
    """Página principal"""
    produtos = sorted(set(f['produto'] for f in fraseologias_cache))
    assuntos = sorted(set(f['assunto'] for f in fraseologias_cache))
    
    # ✅ CONTAR TEMAS CORRETAMENTE - excluindo duplicatas
    temas_unicos = set()
    for f in fraseologias_cache:
        tema = f['tema'].strip()
        if tema:
            temas_unicos.add(tema)
    
    stats = {
        'total': len(fraseologias_cache),
        'temas': len(temas_unicos),
        'assuntos': len(assuntos),
    }
    
    return render_template('index.html', 
                         fraseologias=fraseologias_cache,
                         produtos=produtos,
                         assuntos=assuntos,
                         stats=stats)

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """Tratamento para páginas não encontradas"""
    return render_template('error.html', mensagem='Página não encontrada'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
