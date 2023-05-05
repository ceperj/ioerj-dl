from bs4 import BeautifulSoup
import requests, re, os
import datetime as dt
from prompt_toolkit.shortcuts import button_dialog, input_dialog, checkboxlist_dialog
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import Application
from tqdm import tqdm

################################# VARIAVEIS GLOBAIS ###################################
class Globals():
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

gl = Globals()


######################################## RECURSOS DE DOWNLOAD DO SITE IOERJ ##############################################


# função para obter página HTML e processar como objeto da biblioteca Beautiful Soup
# o tipo de parser funciona em páginas específicas
def defSoup(url, parser='html.parser'):
  try:
    html = requests.get(url, headers=gl.headers)
    soup = BeautifulSoup(html.content, parser)
    return soup
  except:
    print('Erro ao conectar ao site da IOERJ')

#########################

def savePdf(urlPdf, conf):
  
  fullDir = "%s/%s/%s" %(conf.workDir, conf.dataAtual.year, conf.dataAtual.month)
  os.makedirs(fullDir, exist_ok=True)
  nomeFull = "%s/%s_%s.pdf" %(fullDir, conf.dataAtual.day, conf.caderno)

  # download do pdf completo do caderno
  print('Baixando ', nomeFull)
  res = requests.get(urlPdf, stream=True, headers=gl.headers)
  # cabeçalho da requisição para obter tamanho do arquivo e prever na barra de progresso
  tamanhoArq = int(res.headers.get('Content-Length', 0))
  
  # escreve DO na pasta definida, com barra de progresso
  with open(nomeFull, 'wb') as f:
    for chunk in tqdm(res.iter_content(32*1024), total=tamanhoArq, unit='B', unit_scale=True):
      if chunk:
        f.write(chunk)
    

  # escreve uma cópia extra para DO de hoje
  if conf.tipoDownload == 'hoje':
    nomeFull = "%s/Hoje_%s.pdf" % (conf['workDir'], conf['caderno'])
    with open(nomeFull, 'wb') as f:
      f.write(res.content)

#########################

# classe vai receber o elemento HTML(do beautiful soup) para processar nome e se é edição extra
class CadernoDL():
  def __init__(self, element, data):
    self.element = element
    self.url = gl.urlDiaBase + element['href']
    self.caderno = element.text
    self.data = data
    # remove o espaço
    self.nome = re.findall('Parte [IVB]', self.caderno)[0].replace(' ', '')
    # procura se é edição extra, navegando no elemento superior e buscando o span com o id
    if element.parent.find(id='EdicaoExtraDO'):
      self.extra = True
      self.caderno = self.caderno + ' Edição Extra'
      self.nome = self.nome + 'Extra'
    else:
      self.extra = False

  def numerarExtra(self, num):
    self.extraNum = num
    if int(num) > 1:
      self.nome = self.nome + str(num)
      self.caderno = self.caderno + ' ' + str(num)
    return self

  def download(self, conf):    
    htmlDO = defSoup(self.url)
    # busca link do pdf completo dentro do visualizador do IOERJ
    scriptLink = htmlDO.find(id='scaleSelectContainer').find('script').text
    # retorna chave base do PDF, buscando o que tem dentro de aspas
    key = re.findall('"(.*?)"',scriptLink)[0]
    # insere o P dentro da segunda parte da chave, que irá apontar para o PDF com todas as páginas do DO
    # ex: C88CBE18-A446-4060-9882-DF929C0468EA >> C88CBE18-A44P6-4060-9882-DF929C0468EA
    keyArr = key.split('-')
    keyMain = keyArr[1]
    keyArr[1] = keyMain[:3] + 'P' + keyMain[3:]
    key = '-'.join(keyArr)

    urlPdf = gl.urlDiaBase + 'mostra_edicao.php?k=' + key

    # nome que o arquivo terá
    conf.caderno = self.nome
    savePdf(urlPdf, conf)


#########################

def downloadDia(url, conf):
  # abre pagina do dia com os cadernos
  htmlDia = defSoup(url)
  htmlDia.find(id='xo-content').find_all('a')

  for tipoCaderno in conf.cadernos:
    # contagem de edição para cada parte do caderno
    extra = 0
    # links no conteudo central da página, que são os cadernos
    for link in htmlDia.find(id='xo-content').find_all('a'):
      # verificar se o link dentro da página é para um dos cadernos configurados
      if link.text == tipoCaderno:
        # indexar dados do elemento do caderno
        caderno = CadernoDL(link, conf.dataAtual)
        # verificação e contagem de edições extra
        if caderno.extra:
          extra += 1
          caderno = caderno.numerarExtra(extra)
        
        caderno.download(conf)

#########################

def executarDO(conf, dataInicio=(gl.hoje - dt.timedelta(days=7)), dataFim=gl.hoje):

  conf.dataAtual = gl.hoje

  if conf.tipoDownload == 'hoje':
    pagUltima = defSoup(gl.urlUltima)
    # ao ir nesse endereço, o IOERJ mostra uma pagina redirecionadora que contém um link para clicar direto
    urlHoje = gl.urlDiaBase + pagUltima.find('a')['href']
    downloadDia(urlHoje, conf)
    
  if conf.tipoDownload == 'periodo':
    print('Buscando dias de DO.')
    # essa página precisa ser parseada com LXML. Recorta pro ID do conteudo principal
    html = defSoup(gl.urlAnos, parser='html.parser').find(id='xo-page')

    class LinkDO():
      def __init__(self, url, dia, mes, ano):
        self.data = dt.date(int(ano), int(mes), int(dia))
        self.url = url

      def download(self, conf):
        conf.dataAtual = self.data
        downloadDia(self.url, conf)

    # busca campos "Ano de 20XX" para indicar anos disponíveis e inclui numa lista
    anosNum = []
    htmlAnos = html.find_all(class_='titulosecao')
    for ano in htmlAnos:
      anoNum = re.findall('([0-9]+)', ano.text)
      anosNum.append(anoNum[0])

    linksDias = []
    # busca os containers table que contém os calendários dos meses de cada ano
    htmlCalAno = html.find_all('table')
    # iterar elementos de ano, mês, e dia. Usando index do ano para encontrar respectivos meses devido à estrutura de elementos paralelos da página
    for indexAno in range(len(anosNum)):
      ano = anosNum[indexAno]
      # busca os elementos de cada mês, dentro do container do ano
      htmlMeses = htmlCalAno[indexAno].find_all(class_='calendario')
      for mes in htmlMeses:
        # encontra o elemento com o nome do mês, e busca número do mês via dicionário
        mesNome = mes.find(class_='mes').text.replace('\n','')
        mesNum = gl.meses[mesNome]
        diasUteis = mes.find_all(class_='dialink')

        for dia in diasUteis:
          # extrair texto puro do número do dia, remove as quebras de linha do HTML
          diaNum = dia.text.replace('\n','')
          urlDia = gl.urlDiaBase + dia.find('a')['href']
          # insere em lista de datas disponíveis 
          #linksDias.append( LinkDO(urlDia, diaNum, mesNum, ano))
          link = LinkDO(urlDia, diaNum, mesNum, ano)
          # verificar se está dentro do período solicitado
          if link.data >= dataInicio and link.data <= dataFim:
            linksDias.append(link)
          
    # após formar lista, iterar e baixar links de DOs
    print('%s dias selecionados para baixar.'%len(linksDias))
    for linkDia in linksDias:
      linkDia.download(conf)


############################################## DEFINIÇÕES ######################################################
#import ioerj_conf
class Conf():
  def __init__(self, tipoDownload, workDir, cadernos, docs = None):

    self.docsDir = docs or os.environ['HOME']
    
    # dataDownload = ['hoje', 'periodo']
    self.tipoDownload = tipoDownload or'periodo'

    # diretório para salvar pastas (padrão: pasta atual do __main__ ./ )
    self.workDir = workDir or './'

    #self.cadernosDisponiveis = ['Parte I (Poder Executivo)', 'Parte IB - (Tribunal de Contas)', 'Parte II (Poder Legislativo)', 'Parte IV (Municipalidades)', 'Parte V (Publicações a Pedido)']
    self.cadernos = cadernos or ['Parte I (Poder Executivo)']

############################################### RODANDO #####################################################

def main():
  
  kb = KeyBindings()
  @kb.add('escape')
  def exit_(event):
    event.app.exit()
  
  #app = Application(key_bindings=kb, full_screen=True)
  #app.run()

  # usa diretório Documentos padrão no Windows ou Linux
  defaultDocs = "%s\\%s"%((os.environ['USERPROFILE'] or os.environ['HOME']), 'Documents')

  tipoDownload = button_dialog(
    title='Selecione o periodo a ser baixado',
    text='Último DO ou multiplos DOs',
    buttons=[
        ('Hoje', 'hoje'),
        ('Período', 'periodo'),
    ]).run()
  
  diretorio = input_dialog(
    title='Diretório de destino dos arquivos de DO',
    text='Navegar com setas e enter (padrão: pasta Documentos)',
    cancel_text='Cancelar',
    default=defaultDocs).run()
  
  cad = []
  for caderno in gl.cadernosDisponiveis:
    cad.append((caderno, caderno))
  cadernos = checkboxlist_dialog(
    title = "Cadernos para serem baixados",
    text = "Navegar com setas, selecionar com espaço/Enter, confirmar com Tab",
    values = cad).run()
  
  if tipoDownload == 'periodo':
    fData = lambda x: x.strftime('%d/%m/%Y')
    inicio = input_dialog(
      title='Data de início da busca de DOs',
      text='Formato DD/MM/AAAA',
      default = fData(gl.hoje - dt.timedelta(days=7)),
      cancel_text="Cancelar" ).run()
    fim = input_dialog(
      title = 'Data de fim da busca de DOs',
      text = 'Formato DD/MM/AAAA',
      default = fData(gl.hoje),
      cancel_text="Cancelar" ).run()

  conf = Conf(tipoDownload, diretorio, cadernos)

  fData = lambda x: dt.date(int(x.split('/')[2]), int(x.split('/')[1]), int(x.split('/')[0])) or None
  executarDO(conf, dataInicio = fData(inicio), dataFim = fData(fim))

