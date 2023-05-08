import os, ioerj_dl as id, datetime as dt
from prompt_toolkit.shortcuts import button_dialog, input_dialog, checkboxlist_dialog
from prompt_toolkit.key_binding import KeyBindings

gl = id.Globals()

def main():
  
  #kb = KeyBindings()
  #@kb.add('escape')
  #def exit_(event):
    #event.app.exit()
  
  #app = Application(key_bindings=kb, full_screen=True)
  #app.run()

  # usa diretório Documentos padrão no Windows ou Linux
  defaultDocs = "%s\\%s"%((os.environ['USERPROFILE'] or os.environ['HOME']), 'Documents\\IOERJ')

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
      ok_text="Começar",
      cancel_text="Cancelar" ).run()

  conf = id.Conf(tipoDownload, diretorio, cadernos)

  fData = lambda x: dt.date(int(x.split('/')[2]), int(x.split('/')[1]), int(x.split('/')[0])) or None
  id.executarDO(conf, dataInicio = fData(inicio), dataFim = fData(fim))