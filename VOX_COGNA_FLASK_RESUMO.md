# 💜 Vox Cogna - Versão Flask (Completa)

## 📦 Arquivos Criados

### Backend
- **app_flask.py** - Aplicação Flask com todas as rotas

### Frontend
- **templates/base.html** - Template base (herança)
- **templates/index.html** - Página principal com filtros e fraseologias
- **templates/error.html** - Página de erro
- **static/style.css** - Estilo completo (cores Cogna)
- **static/script.js** - Script auxiliar (extensível)

### Configuração
- **requirements_flask.txt** - Dependências Python
- **README_FLASK.md** - Documentação completa
- **INICIO_FLASK.md** - Guia rápido (5 minutos)

---

## 🚀 Como Usar (5 Minutos)

### 1. Preparar Pasta

```bash
mkdir vox-cogna-flask
cd vox-cogna-flask
```

### 2. Copiar Arquivos

Copie todos os arquivos para a pasta (estrutura preserve)

### 3. Copiar Base de Dados

```bash
cp ../seu-projeto/base_fraseologias.xlsx ./base_fraseologias.xlsx
```

### 4. Instalar Dependências

```bash
pip install -r requirements_flask.txt
```

### 5. Rodar

```bash
python app_flask.py
```

### 6. Acessar

```
http://localhost:5000
```

---

## ✅ Funcionalidades Implementadas

- ✅ Carregar dados do Excel (base_fraseologias.xlsx)
- ✅ Filtro por Produto (EAD Legado, Presencial, PTC, Geral, Moderação)
- ✅ Filtro por Assunto
- ✅ Busca Fuzzy (tolera acentos e erros)
- ✅ Badges coloridos
  - STATUS: DEFERIDO (verde), INDEFERIDO (vermelho), SANAR DÚVIDAS (amarelo)
  - PRODUTO: cores diferentes para cada tipo
- ✅ Botão Copiar (copia para clipboard automaticamente)
- ✅ Botões Expandir/Recolher Todos
- ✅ Limpar Filtros (volta tudo ao padrão)
- ✅ Design responsivo (mobile/tablet/desktop)
- ✅ Paleta de cores Cogna (roxo escuro)
- ✅ Header com métricas
- ✅ Link para Artigos Beedoo

---

## 🔧 Estrutura Flask

```python
# Backend (app_flask.py)
@app.route('/')                    # GET - Página principal
@app.route('/api/filtro')          # POST - Filtrar fraseologias
@app.route('/api/copy')            # POST - Copiar fraseologia

# Funções utilitárias
carregar_fraseologias()            # Carrega Excel
busca_fuzzy()                      # Busca tolerante
normalizar()                       # Remove acentos
levenshtein()                      # Distância entre strings
similaridade()                     # Calcula similaridade %
```

---

## 📊 Estrutura de Pastas

```
vox-cogna-flask/
├── app_flask.py                    (Backend)
├── base_fraseologias.xlsx          (Dados - IMPORTANTE!)
├── requirements_flask.txt
├── README_FLASK.md
├── INICIO_FLASK.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── error.html
└── static/
    ├── style.css
    └── script.js
```

---

## 🎨 Design

### Cores (Paleta Cogna)

```css
--roxo-principal: #4A1464
--roxo-escuro: #2E0D42
--roxo-claro: #DFC4EB
--bg-light: #E8E2F0
--border-color: #D4C6E0
```

### Badges

- **DEFERIDO**: Verde (#D4EDDA / #155724)
- **INDEFERIDO**: Vermelho (#F8D7DA / #721C24)
- **SANAR DÚVIDAS**: Amarelo (#FFF3CD / #856404)
- **EAD Legado**: Azul (#CCE5FF / #003399)
- **Presencial**: Ciano (#D1ECF1 / #0C5460)
- **PTC**: Roxo (#E7D4F5 / #4A1464)
- **Geral**: Laranja (#F8CECC / #8B3A15)
- **Moderação**: Roxo (#DFC4EB / #5A1F7D)

---

## 🔍 Busca Fuzzy

Implementação completa com:
- ✅ Normalização de acentos
- ✅ Distância de Levenshtein
- ✅ Similaridade por token
- ✅ Busca em tema, assunto, produto e fraseologia
- ✅ Threshold ajustável (65% por padrão)

**Exemplos que funcionam:**
```
"reembolso" → encontra "Reembolso"
"débto" → encontra "Débito"
"prova" → encontra "Avaliação da Prova"
"escalonamento" → encontra "Escalonamento"
```

---

## 🌐 API Endpoints

### GET /
Retorna página principal com:
- Fraseologias carregadas
- Métricas (total, temas, assuntos)
- Listas de filtros (produtos, assuntos)

**Response:** HTML renderizado

### POST /api/filtro
Filtra fraseologias baseado em critérios

**Request:**
```json
{
  "produto": "Presencial",
  "assunto": "Acadêmico",
  "busca": "prova"
}
```

**Response:**
```json
{
  "total": 3,
  "grupos": {
    "Acadêmico": [
      {
        "produto": "Presencial",
        "assunto": "Acadêmico",
        "tema": "Consulta sobre Nota de Prova",
        "fraseologia": "Olá, XXXX...",
        "status": "DEFERIDO",
        "artigo": "https://..."
      }
    ]
  }
}
```

### POST /api/copy
Retorna conteúdo para copiar

**Request:**
```json
{
  "idx": 12345
}
```

**Response:**
```json
{
  "sucesso": true,
  "conteudo": "Fraseologia aqui..."
}
```

---

## 🚀 Deploy Rápido

### Heroku
```bash
pip install gunicorn
echo "web: gunicorn app_flask:app" > Procfile
heroku create vox-cogna
git push heroku main
```

### PythonAnywhere
1. Upload arquivos
2. Configurar app na web
3. Iniciar web app

### VPS (AWS/DigitalOcean)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_flask:app
```

---

## 📱 Responsivo

- ✅ Desktop (1920px+) - Layout completo
- ✅ Tablet (768px) - Layout adaptado
- ✅ Mobile (375px) - Stack vertical

---

## 🔒 Segurança em Produção

```python
# Mudar antes de fazer deploy
app.run(debug=False)                    # Desabilitar debug
FLASK_ENV=production                    # Variável de ambiente
```

---

## 📚 Diferenças: Streamlit vs Flask

| Aspecto | Streamlit | Flask |
|---------|-----------|-------|
| **Curva de aprendizado** | Fácil | Média |
| **Performance** | Mais lenta | Rápida |
| **Customização** | Limitada | Ilimitada |
| **Deploy** | Muito fácil (Cloud) | Mais trabalho |
| **Ideal para** | Prototipagem | Produção |
| **Interatividade** | Recalcula sempre | Apenas necessário |

---

## 🐛 Troubleshooting

### Erro: "base_fraseologias.xlsx not found"
→ Copiar arquivo para pasta do app

### Erro: "ModuleNotFoundError"
→ `pip install -r requirements_flask.txt`

### Porta 5000 já em uso
→ Mudar em app_flask.py: `port=8080`

### Fraseologias não aparecem
→ Fechar Excel e recarregar página

---

## 💡 Extensões Possíveis

- [ ] Login/autenticação
- [ ] Histórico de buscas
- [ ] Ratings de fraseologias
- [ ] Compartilhar via link
- [ ] Exportar para PDF
- [ ] Integração com Slack
- [ ] Dark mode
- [ ] API pública

---

## 📝 Versionamento

**Versão:** 1.0  
**Data:** Julho 2026  
**Status:** Pronto para produção ✅

---

## 👥 Autores

- Victor Mathias Gustavo
- Natalice Gomes Lima
- Time de Qualidade de Atendimento
- **Cogna Educação**

---

**Pronto para usar! 💜**
