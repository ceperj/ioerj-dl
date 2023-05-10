import datetime as dt
from pathlib import Path

################################# VARIAVEIS GLOBAIS ###################################
class Globals:
  # nome de meses e respectivos números para serem parseados. Modulo Datetime não suporta português
  meses = {'Janeiro': 1,
          'Fevereiro': 2,
          'Março': 3,
          'Abril': 4,
          'Maio': 5,
          'Junho': 6,
          'Julho': 7,
          'Agosto': 8,
          'Setembro': 9,
          'Outubro': 10,
          'Novembro': 11,
          'Dezembro': 12
          }
  urlAnos = 'http://www.ioerj.com.br/portal/modules/conteudoonline/do_seleciona_data.php'
  urlDiaBase = 'http://www.ioerj.com.br/portal/modules/conteudoonline/'
  urlUltima = 'http://www.ioerj.com.br/portal/modules/conteudoonline/do_ultima_edicao.php'
  headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0' }
  cadernosDisponiveis = ['Parte I (Poder Executivo)', 'Parte IB - (Tribunal de Contas)', 'Parte II (Poder Legislativo)', 'Parte IV (Municipalidades)', 'Parte V (Publicações a Pedido)']
  hoje = dt.date.today()
  defaultDir = Path(Path.home(), 'Documents', 'IOERJ')

class Defaults:
  dir = Path(Path.home(), 'Documents', 'IOERJ')
  inicio = (Globals.hoje - dt.timedelta(days=7))