## Ferramenta baseada em python que realiza web-scrap no [site](http://www.ioerj.rj.gov.br) da Imprensa Oficial do Estado do Rio de Janeiro para baixar arquivos PDF de Diários Oficiais automaticamente.

Documentos são baixados por padrão na pasta `<Usuário>/Documents/IOERJ` e organizados na estrutura `YYYY/MM/DD_ParteX.pdf`. Sendo `YYYY/MM/DD` os números da data do Diário e `ParteX` o identificador do caderno, podendo ser reconhecido como caderno Extra (ex: `ParteII`, `ParteIExtra`).

---
### Opções suportadas:
- Baixar período de datas selecionadas
- Baixar diário do dia (ideal para scripts rotineiros)
- Selecionar cadernos

---
### Módulos

**Requer** módulos: **bs4** (BeaufitulSoup4), **requests**. Módulos opcionais para linha de comando interativa CLI: **prompt-toolkit** e **tqdm**. Todos estão listados *requirements.txt*.

---
### Problemas conhecidos:
- Edições suplementares não são suportadas (exemplo: [05 jan 2023](http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_edicao.php?data=MjAyMzAxMDU=), Parte I)
- Sem fallback ao escolher "cancelar" no CLI