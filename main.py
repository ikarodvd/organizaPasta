import os
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def onCreated(event, pastaDestino):
    if event.is_directory:
        return

    caminhoArquivo = event.src_path
    extensao = Path(caminhoArquivo).suffix.lower()

    if extensao:
        pastaAlvo = pastaDestino / extensao[1:]
    else:
        pastaAlvo = pastaDestino / "sem_extensao"

    if not pastaAlvo.exists():
        pastaAlvo.mkdir()

    arquivoAlvo = pastaAlvo / Path(caminhoArquivo).name
    shutil.move(caminhoArquivo, arquivoAlvo)


def criarPastasParaExtensao(pasta):
    extensoes = set()

    for arquivo in pasta.iterdir():
        if arquivo.is_file():
            extensao = arquivo.suffix.lower()
            extensoes.add(extensao)

    for extensao in extensoes:
        pastaAlvo = pasta / extensao[1:]
        if not pastaAlvo.exists():
            pastaAlvo.mkdir()

    pastaSemExtensao = pasta / "sem_extensao"
    if not pastaSemExtensao.exists():
        pastaSemExtensao.mkdir()


def organizarArquivos(pasta):
    criarPastasParaExtensao(pasta)

    for arquivo in pasta.iterdir():
        if arquivo.is_file():
            extensao = arquivo.suffix.lower()
            if extensao:
                pastaAlvo = pasta / extensao[1:]
            else:
                pastaAlvo = pasta / "sem_extensao"
            arquivoAlvo = pastaAlvo / arquivo.name
            shutil.move(str(arquivo), str(arquivoAlvo))


def monitorarPasta(pasta):
    class ManipuladorArquivo(FileSystemEventHandler):
        def onCreated(self, event):
            onCreated(event, pasta)

    manipuladorEvento = ManipuladorArquivo()
    observador = Observer()
    observador.schedule(manipuladorEvento, pasta, recursive=True)
    observador.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observador.stop()

    observador.join()


if __name__ == "__main__":
    pasta = Path(input("Digite o caminho da pasta a ser monitorada: "))

    organizarArquivos(pasta)
    monitorarPasta(pasta)
