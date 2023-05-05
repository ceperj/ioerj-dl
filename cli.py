from prompt_toolkit.shortcuts import button_dialog, input_dialog
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import HTML, PromptSession, Application
import ioerj_conf


def mudarConf(conf):
  result = button_dialog(
    title='Gerenciador IOERJ: Baixar',
    text='Selecione baixar ou pesquisar no diretório local',
    buttons=[
        ('Busca: %s'%conf.tipoDownload, 'tipoDownload'),
        ('Cadernos selecionados: %s'%conf.cadernosDownload, 'cadernosDownload')
      ],
  ).run()

# criar atalhos teclado
def atalhos(conf):
  kb = KeyBindings()
  @kb.add('c-d')
  def _(event):
    mudarConf(conf)

# barra inferior
def barraInf(texto):
  return HTML(texto)


# tela inicial
def main(conf):
  result = button_dialog(
      title='Gerenciador IOERJ: Baixar',
      text='Selecione baixar ou pesquisar no diretório local',
      buttons=[
          ('Baixar', 'baixar'),
          ('Pesquisar', 'pesquisar'),
          ('Mudar configuração', 'conf')
      ],
  ).run()

  if result == 'baixar':
    download(conf)
  if result == 'pesquisar':
    pesquisa(conf)
  if result == 'conf':
    mudarConf(conf)


def download(conf):
  texto = 'Buscando: %s \n\
  Cadernos: %s\n\
  Salvando na pasta: %s'\
  %(conf.tipoBusca, conf.cadernosDownload, conf.workDir)

  data = input_dialog(
    title='Gerenciador IOERJ: Baixar',
    text='Digite as data em formato dia/mês/ano (01/01/2020).\n\
      Mantenha em branco para buscar a data de hoje:').run()
  

def pesquisa(conf):  
  busca = input_dialog(
    title='Gerenciador IOERJ: Pesquisar',
    text='Digite sua pesquisa:').run()



conf = ioerj_conf.Conf()
