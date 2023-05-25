import os
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def on_created(event, pasta_destino):
    if event.is_directory:
        return

    caminho_arquivo = event.src_path
    extensao = Path(caminho_arquivo).suffix.lower()

    if extensao:
        pasta_alvo = pasta_destino / extensao[1:]
    else:
        pasta_alvo = pasta_destino / "sem_extensao"

    if not pasta_alvo.exists():
        pasta_alvo.mkdir()

    arquivo_alvo = pasta_alvo / Path(caminho_arquivo).name
    shutil.move(caminho_arquivo, arquivo_alvo)


def criar_pastas_para_extensoes(pasta):
    extensoes = set()

    for arquivo in pasta.iterdir():
        if arquivo.is_file():
            extensao = arquivo.suffix.lower()
            extensoes.add(extensao)

    for extensao in extensoes:
        pasta_alvo = pasta / extensao[1:]
        if not pasta_alvo.exists():
            pasta_alvo.mkdir()

    pasta_sem_extensao = pasta / "sem_extensao"
    if not pasta_sem_extensao.exists():
        pasta_sem_extensao.mkdir()


def organizar_arquivos(pasta):
    criar_pastas_para_extensoes(pasta)

    for arquivo in pasta.iterdir():
        if arquivo.is_file():
            extensao = arquivo.suffix.lower()
            if extensao:
                pasta_alvo = pasta / extensao[1:]
            else:
                pasta_alvo = pasta / "sem_extensao"
            arquivo_alvo = pasta_alvo / arquivo.name
            shutil.move(str(arquivo), str(arquivo_alvo))


def monitorar_pasta(pasta):
    class ManipuladorArquivo(FileSystemEventHandler):
        def on_created(self, event):
            on_created(event, pasta)

    manipulador_evento = ManipuladorArquivo()
    observador = Observer()
    observador.schedule(manipulador_evento, pasta, recursive=True)
    observador.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observador.stop()

    observador.join()


if __name__ == "__main__":
    pasta = Path(input("Digite o caminho da pasta a ser monitorada: "))

    organizar_arquivos(pasta)
    monitorar_pasta(pasta)
