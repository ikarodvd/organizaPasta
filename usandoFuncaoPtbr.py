import os
import argparse
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def ao_criar(evento, pastas):
    if evento.is_directory:
        return

    caminho_arquivo = evento.src_path
    extensao = Path(caminho_arquivo).suffix.lower()

    if extensao:
        pasta_destino = encontrar_pasta_destino(extensao[1:], pastas)
    else:
        pasta_destino = encontrar_pasta_destino("sem_extensao", pastas)

    if not pasta_destino.exists():
        pasta_destino.mkdir()

    arquivo_destino = pasta_destino / Path(caminho_arquivo).name

    try:
        shutil.move(caminho_arquivo, arquivo_destino)
        print(f"Arquivo movido com sucesso: {caminho_arquivo} -> {arquivo_destino}")
    except Exception as e:
        print(f"Erro ao mover o arquivo: {caminho_arquivo} -> {arquivo_destino}")
        print(f"Detalhes do erro: {str(e)}")


def encontrar_pasta_destino(extensao, pastas):
    for pasta in pastas:
        pasta_destino = pasta / extensao
        if pasta_destino.exists():
            return pasta_destino
    return pastas[0] / extensao


def criar_pastas_para_extensoes(pastas):  # 2 função a ser criada
    extensoes = set()

    for pasta in pastas:
        for arquivo in pasta.iterdir():
            if arquivo.is_file():
                extensao = arquivo.suffix.lower()
                extensoes.add(extensao)

    for pasta in pastas:
        for extensao in extensoes:
            pasta_destino = pasta / extensao[1:]
            if not pasta_destino.exists():
                pasta_destino.mkdir()

    for pasta in pastas:
        pasta_destino = pasta / "sem_extensao"
        if not pasta_destino.exists():
            pasta_destino.mkdir()


def organizar_arquivos(pastas):  # 1 função criada
    criar_pastas_para_extensoes(
        pastas
    )  # depois que eu fizer toda a função da camada superior

    for pasta in pastas:
        for arquivo in pasta.iterdir():
            if arquivo.is_file():
                extensao = arquivo.suffix.lower()
                if extensao:
                    pasta_destino = pasta / extensao[1:]
                else:
                    pasta_destino = pasta / "sem_extensao"
                arquivo_destino = pasta_destino / arquivo.name
                shutil.move(str(arquivo), str(arquivo_destino))


def monitorar_pastas(pastas):  # 3 função a ser criada
    manipulador_eventos = FileSystemEventHandler()
    manipulador_eventos.on_created = lambda evento: ao_criar(
        evento, pastas
    )  # Criar depois do final dessa função

    observador = Observer()
    for pasta in pastas:
        observador.schedule(manipulador_eventos, pasta, recursive=True)
    observador.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observador.stop()

    observador.join()


if __name__ == "__main__":  # construindo
    parser = argparse.ArgumentParser(
        description="Monitora e organiza arquivos em uma pasta baseando-se em suas extensões."
    )
    parser.add_argument(
        "--pastas",
        nargs="*",
        default=[Path(os.getcwd())],
        help="Pastas para monitorar",
    )

    args = parser.parse_args()

    pastas = [Path(pasta) for pasta in args.pastas]

    organizar_arquivos(pastas)
    monitorar_pastas(pastas)
