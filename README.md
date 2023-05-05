## Ferramenta baseada em python que realiza web-scrap no [site do IOERJ](www.ioerj.rj.gov.br) para baixar arquivos de Diários automaticamente.

### Opções suportadas:
- Baixar período de datas selecionadas
- Baixar diário do dia (ideal para scripts rotineiros)
- Selecionar cadernos

### Módulos

Requer módulos: **bs4** (BeaufitulSoup4), **requests**. Módulos opcionais para linha de comando interativa CLI: **prompt-toolkit** e **tqdm**. Todos estão listados *requirements.txt*.

### Problemas conhecidos:
- Edições suplementares não são suportadas. 
- Sem fallback ao escolher "cancelar" no CLI