# 🚀 Iniciar Vox Cogna Flask - 5 Minutos

## Passo 1: Preparar Pasta

```bash
mkdir vox-cogna-flask
cd vox-cogna-flask
```

## Passo 2: Copiar Arquivos

Copie estes arquivos para a pasta:

```
app_flask.py
base_fraseologias.xlsx         ← DO SEU PROJETO
requirements_flask.txt
templates/
  ├── base.html
  ├── index.html
  └── error.html
static/
  ├── style.css
  └── script.js
```

## Passo 3: Instalar Python (se não tiver)

Baixe em: https://www.python.org/downloads/

## Passo 4: Instalar Dependências

```bash
pip install -r requirements_flask.txt
```

## Passo 5: Rodar

```bash
python app_flask.py
```

## Passo 6: Acessar

**Abra no navegador:**
```
http://localhost:5000
```

---

## ✅ Pronto!

- ✅ App rodando
- ✅ Filtros funcionando
- ✅ Badges coloridas
- ✅ Copiar funcionando

---

## 🛑 Parar

```bash
Ctrl+C (no terminal)
```

---

## 📝 Dúvidas Comuns

### "Erro: base_fraseologias.xlsx not found"

→ Verifique se o arquivo está no mesmo diretório que `app_flask.py`

### "Erro: ModuleNotFoundError"

→ Execute: `pip install -r requirements_flask.txt`

### "Porta 5000 já está em uso"

→ Abra `app_flask.py` e mude `port=5000` para `port=8080`

---

**Pronto pra usar! 💜**
