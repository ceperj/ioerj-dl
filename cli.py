import ioerj_dl as id, datetime as dt, conf
from prompt_toolkit.shortcuts import button_dialog, input_dialog, checkboxlist_dialog

gl = conf.Globals()

def main():

  tipoDownload = button_dialog(
    title= 'Selecione o periodo a ser baixado',
    text = 'Último DO ou multiplos DOs',
    buttons=[
        ('Hoje', 'hoje'),
        ('Período', 'periodo'),
    ]).run()
  
  diretorio = input_dialog(
    title = 'Diretório de destino dos arquivos de DO',
    text =  'Navegar com setas e enter (padrão: pasta Documentos)',
    cancel_text = 'Cancelar',
    default = str(gl.defaultDir)).run()
  
  cad = [(c, c) for c in gl.cadernosDisponiveis]
  cadernos = checkboxlist_dialog(
    title = "Cadernos para serem baixados",
    text = "Navegar com setas, selecionar com espaço/Enter, confirmar com Tab",
    cancel_text='Cancelar',
    values = cad).run()
  
  if tipoDownload == 'periodo':
    # função anonima de parsear data para string DD/MM/YYYY
    fData = lambda x: x.strftime('%d/%m/%Y')

    # data inicial padrão
    inicioPadrao = fData( gl.hoje - dt.timedelta(days=7))
    inicio = input_dialog(
      title='Data de início da busca de DOs',
      text='Formato DD/MM/AAAA',
      default = fData(inicioPadrao),
      cancel_text="Cancelar" ).run()
    
    # se data de inicio for modificada, manter a mesma no fim para otimizar buscas de datas únicas
    if inicio != inicioPadrao:
      fimPadrao = inicio
    else:
      fimPadrao = fData(gl.hoje)
    
    fim = input_dialog(
      title = 'Data de fim da busca de DOs',
      text = 'Formato DD/MM/AAAA',
      default = fimPadrao,
      ok_text="Começar",
      cancel_text="Cancelar" ).run()
    
    # formatação de data DD/MM/YYYY de volta para datetime
    fData = lambda x: dt.date(int(x.split('/')[2]), int(x.split('/')[1]), int(x.split('/')[0]))
    inicio = fData(inicio)
    fim = fData(fim)
    
  else:
    fim = None
    inicio = None

    conf = {
            'tipoDownload': tipoDownload,
            'diretorio': diretorio,
            'cadernos': cadernos,
            'dataInicio': inicio,
            'dataFim': fim
    }

    id.executarDO(conf)
  