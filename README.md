# 📌 Suapy

## 📖 Descrição
Sistema para processamento extração de dados do SUAP.
 

## 🔧 Tecnologias Utilizadas

✅ **Linguagem:** Python  
✅ **Bibliotecas:**  
- `selenium` → Para coleta automática de dados no SUAP  
- `pandas` → Para manipulação de planilhas  
- `openpyxl` → Para trabalhar com XLSX  
- `PyQt6` → Para uma interface mínima e configurações rápidas  

📌 **Formato de entrada/saída:**  
- **Entrada:** CSV ou XLSX (cabeçalhos fixos)  
- **Saída:** XLSX (mais organizado) ou CSV (se precisar de compatibilidade)  

## 🎯 Decisões Técnicas

✅ **Automação com Selenium** → O sistema acessará o SUAP automaticamente para coletar as informações necessárias (Autenticação do usuário necessária).  

✅ **Manipulação de planilhas com Pandas e OpenPyXL** → Facilidade para tratar, filtrar e exportar os dados.  

✅ **Interface mínima com PyQt6** → Para permitir seleção de arquivos e configurações rápidas.  

## 🏗️ Execução (Em breve: execução por módulo)
```bash
python run.py
```