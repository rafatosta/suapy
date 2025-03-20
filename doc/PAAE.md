# 📌 SuapExtract: PAAE

## 📖 Descrição
Sistema para processamento automatizado de listas de alunos inscritos no PAAE (Plano de Atendimento Educacional Especializado ou Programa de Avaliação da Aprendizagem Escolar). Ele busca os dados bancários dos alunos, aplica a remoção de alunos conforme uma planilha fornecida e gera um relatório final pronto para uso.

## 🚀 Fluxo de Funcionamento

1️⃣ **Usuário seleciona os arquivos:**  
   - Planilha de inscritos do SUAP (CSV/XLSX):
      - https://suap.ifba.edu.br/ae/relatorio_alunos_inscritos/  
   - Planilha de remoção (CSV/XLSX)  

2️⃣ **O sistema processa os dados:**  
   - Verifica se todos os alunos na planilha de remoção existem na lista principal.  
   - Remove os alunos da lista principal.  
   - Destaca alunos sem dados bancários (opcional).  

3️⃣ **Gera e abre o arquivo final** no editor padrão (Excel, LibreOffice, etc.).  

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

## ✅ Checklist de Desenvolvimento

### 🔹 Planejamento
- [ ] Definir requisitos detalhados.
- [x] Estruturar o projeto e definir pastas e arquivos.
- [x] Escolher bibliotecas e dependências necessárias.

### 🔹 Implementação
- [x] Criar estrutura inicial do projeto.
- [ ] Implementar automação com Selenium para coleta de dados no SUAP.
- [ ] Implementar leitura das planilhas de entrada (inscritos e remoção).
- [ ] Implementar validação dos alunos na lista de remoção.
- [ ] Implementar remoção de alunos.
- [ ] Destacar alunos sem dados bancários (opcional).
- [ ] Implementar geração e salvamento do relatório final.
- [ ] Implementar abertura automática do relatório no editor padrão.
- [ ] Criar interface mínima com PyQt6.

### 🔹 Testes e Ajustes
- [ ] Testar o fluxo completo com arquivos reais.
- [ ] Corrigir bugs e otimizar o código.

### 🔹 Documentação e Finalização
- [ ] Criar documentação do sistema.
- [ ] Criar guia de uso para o usuário.
- [ ] Preparar versão final para distribuição.

## 🏗️ Execução
```bash
python run.py
```