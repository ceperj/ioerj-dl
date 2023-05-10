import cli, conf, argparse, sys, ioerj_dl

parser = argparse.ArgumentParser(description='IOERJ-DL')
df = conf.Defaults

parser.add_argument('--modo', type=str, default='periodo',
                    help="'ultimo', 'periodo' = 'periodo'\nSelecionar o ultimo DO ou datas selecionadas.")
parser.add_argument('--diretorio', type=str, default=df.workDir,
                    help="(Diretorio relativo) = [user]/Documents/IOERJ\nDiretorio de destino.")
parser.add_argument('--inicio', type=str, default=df.inicio,
                    help="DD/MM/YYYY = (hoje)\nData de início ao escolher baixar no modo 'periodo'.")
parser.add_argument('--fim', type=str, default=df.fim,
                    help="DD/MM/YYYY = (7 dias atras)\nData de fim ao escolher baixar no modo 'periodo'.")
# args de Cadernos ainda a ser implementado, padronizado apenas para Parte I por enquanto.

# se nenhum argumento foi passado, usar o CLI(prompt-toolkit) ou GUI
if len(sys.argv) == 1:
  cli.main()

# se agumentos forem passados, 
else:
  args = parser.parse_args()
  config = {
          'tipoDownload': args.modo,
          'diretorio': args.diretorio,
          'cadernos': df.cadernos,
          'dataInicio': args.inicio,
          'dataFim': args.fim
  }
  ioerj_dl.executarDO(config)