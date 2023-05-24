import pyforms
import conf
import ioerj_dl
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlCheckBox, ControlButton, ControlDir, ControlLabel, ControlProgress
import datetime as dt

gl = conf.Globals
df = conf.Defaults


class GUI(BaseWidget):
  def __init__(self):
    super(GUI, self).__init__('IOERJ-DL')

    # seleção de diretorio para salvar
    self._diretorio = ControlDir('Pasta destino')
    # definir valor padrão do diretorio; por algum motivo o arg default=... da classe não funciona
    self._diretorio.value = str(df.workDir)

    # Seleção de cadernos
    n = 1
    # criar atributos comuns de cadernos numerados, para que possam ser exibidos
    for cad in gl.cadernosDisponiveis:
      # nome de atributo mais destacavel para ser pesquisado em outra função
      self.__setattr__('_cadernoCheck%i' % n, ControlCheckBox(cad, value=True, changed_event=self.__marcarCaderno))
      n += 1
    # iniciar primeiro caderno já marcado
    self._cadernoCheck1.value = True

    # modo de baixar
    self.operacao = 'periodo'
    self._modo = ControlCheckBox('Baixar apenas de hoje', changed_event=self.__trocarModo)

    # conversão de datetime para string DD/MM/YYYY
    def fData(x): return x.strftime('%d/%m/%Y')
    inicioPadrao = fData(df.inicio)
    fimPadrao = fData(gl.hoje)
    self._inicio = ControlText(
        'Data início', helptext='Primeira data a ser baixada. Deve ser digitada no formato DD/MM/YYYY.',
        default=inicioPadrao)
    self._fim = ControlText(
        'Data fim', helptext='Última data a ser baixada. Deve ser digitada no formato DD/MM/YYYY.', default=fimPadrao)

    self._label = ControlLabel()
    self._progress = ControlProgress('Progresso total')

    self._button = ControlButton('Baixar')
    self._button.value = self.__download

  # troca de modo de download
  def __trocarModo(self):
    if self._modo.value == False:
      self.operacao = 'periodo'
      self._inicio.enabled = True
      self._fim.enabled = True
    elif self._modo.value == True:
      self.operacao = 'hoje'
      self._inicio.enabled = False
      self._fim.enabled = False

  # listar selecionados quando um caderno é (des)marcado
  def __marcarCaderno(self):
    cadernos = [key for key in self.__dict__.keys() if key.startswith('_cadernoCheck')]
    self._cadernosSelecionados = [self.__getattribute__(
        cad).label for cad in cadernos if self.__getattribute__(cad).value == True]

  # Iniciar download quando botão é clicado
  def __download(self):
    self._button.enabled = False

    # função anonima para parsear string de volta para datetime
    def parseDate(x): return dt.date(int(x.split('/')[2]), int(x.split('/')[1]), int(x.split('/')[0]))
    conf = {
        'tipoDownload': self.operacao,
        'diretorio': self._diretorio.value,
        'cadernos': self._cadernosSelecionados,
        'dataInicio': parseDate(self._inicio.value),
        'dataFim': parseDate(self._fim.value),
        'barraProgresso': self._progress,
        'labelGUI': self._label
    }

    ioerj_dl.executarDO(conf)

    self._progress.value = 0
    self._label.value = 'Concluído!'
    self._button.enabled = True


def main():
  pyforms.start_app(GUI)

if __name__ == "__main__":
  main()
