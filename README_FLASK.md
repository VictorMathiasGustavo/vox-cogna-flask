# 💜 Vox Cogna - Versão Flask

**Biblioteca de Fraseologias - Cogna Educação**

Versão em **Flask** (alternativa ao Streamlit)

---

## 📋 Diferenças Streamlit vs Flask

| Aspecto | Streamlit | Flask |
|---------|-----------|-------|
| **Tipo** | Framework de dados | Framework web |
| **Performance** | Mais lenta (recalcula) | Mais rápida |
| **Customização** | Limitada | Ilimitada |
| **Estilo** | Predefinido | Total controle |
| **Deploy** | Fácil (Community Cloud) | Mais trabalho |
| **Ideal para** | Prototipagem rápida | Produção |

---

## 🚀 Como Usar

### 1️⃣ Estrutura de Pastas

```
seu-projeto/
├── app_flask.py                    ← Aplicação principal
├── base_fraseologias.xlsx          ← Dados (COPIE DO SEU PROJETO)
├── requirements_flask.txt          ← Dependências
├── templates/
│   ├── base.html
│   ├── index.html
│   └── error.html
└── static/
    └── style.css
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements_flask.txt
```

### 3️⃣ Copiar Dados

**IMPORTANTE:** Copie o arquivo `base_fraseologias.xlsx` para o mesmo diretório que `app_flask.py`

```bash
cp ../seu-projeto/base_fraseologias.xlsx ./base_fraseologias.xlsx
```

### 4️⃣ Rodar Localmente

```bash
python app_flask.py
```

**Acesse:** `http://localhost:5000`

---

## ✅ Funcionalidades

- ✅ Filtros (Produto, Assunto, Busca Fuzzy)
- ✅ Busca tolerante a acentos e erros de digitação
- ✅ Badges coloridos (STATUS e PRODUTO)
- ✅ Copiar fraseologia automaticamente
- ✅ Expandir/Recolher todos
- ✅ Design responsivo (desktop + mobile)
- ✅ Paleta de cores Cogna (roxo)

---

## 🔧 Configuração

### Porta Padrão: 5000

Para usar outra porta:

```python
# No final de app_flask.py
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Mudar para 8080
```

### Debug Mode

Desabilitar em produção:

```python
app.run(debug=False)  # False para produção
```

---

## 📊 Estrutura do Código

### `app_flask.py`

```python
# Carrega fraseologias do Excel
FRASEOLOGIAS = carregar_fraseologias()

# Rotas principais
@app.route('/')                    # Página principal
@app.route('/api/filtro')          # API de filtros
@app.route('/api/copy')            # API de copiar
```

### `templates/`

- `base.html` - Template base (herança)
- `index.html` - Página principal com JavaScript
- `error.html` - Página de erro

### `static/`

- `style.css` - Estilo completo (cores Cogna)

---

## 🔍 Busca Fuzzy

A busca funciona com:

```
✅ Acentuação variada
✅ Pequenos erros de digitação
✅ Prefixos e sufixos
✅ Busca por tema, assunto ou conteúdo

Exemplos:
- "reembolso" encontra "Reembolso"
- "débto" encontra "Débito"
- "prova" encontra "Avaliação da Prova"
```

---

## 🐛 Troubleshooting

### Erro: "base_fraseologias.xlsx not found"

**Solução:**
1. Verifique se o arquivo está no mesmo diretório que `app_flask.py`
2. Feche o Excel se estiver aberto
3. Recarregue a página

### Erro: "ModuleNotFoundError"

**Solução:**
```bash
pip install -r requirements_flask.txt
```

### Fraseologias não aparecem

**Solução:**
1. Verifique se as abas do Excel estão nomeadas corretamente
2. Verifique se há dados na coluna "Fraseologia"
3. Feche o Excel e recarregue

---

## 📝 Atualizando Dados

**Fluxo mensal:**

```bash
# 1. Editar Excel
# 2. Fechar Excel
# 3. Recarregar página (F5)

# Sem need de código!
```

---

## 🚀 Deploy em Produção

### Opção 1: Heroku

```bash
# 1. Criar arquivo Procfile
echo "web: gunicorn app_flask:app" > Procfile

# 2. Instalar gunicorn
pip install gunicorn

# 3. Push
heroku create vox-cogna
git push heroku main
```

### Opção 2: PythonAnywhere

1. Upload arquivos
2. Configurar app
3. Iniciar

### Opção 3: VPS (AWS/DigitalOcean)

```bash
# Usar Nginx + Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_flask:app
```

---

## 📱 Responsivo

Funciona em:

- ✅ Desktop (1920px+)
- ✅ Tablet (768px)
- ✅ Mobile (375px)

---

## 📚 Tecnologias

- **Python** 3.8+
- **Flask** 2.3+
- **Pandas** 2.0+ (carregar Excel)
- **HTML5** (templates)
- **CSS3** (estilo)
- **JavaScript** (interatividade)

---

## 📄 Licença

Desenvolvido para **Cogna Educação** - Time de Qualidade de Atendimento

---

## 👥 Autores

- Victor Mathias Gustavo
- Natalice Gomes Lima

---

**Versão:** 1.0 | **Data:** Julho 2026
