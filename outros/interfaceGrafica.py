import os
import argparse
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog


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


def criar_pastas_para_extensoes(pastas):
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


def organizar_arquivos(pastas):
    criar_pastas_para_extensoes(pastas)

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


def monitorar_pastas(pastas):
    manipulador_eventos = FileSystemEventHandler()
    manipulador_eventos.on_created = lambda evento: ao_criar(evento, pastas)

    observador = Observer()
    for pasta in pastas:
        observador.schedule(manipulador_eventos, pasta, recursive=True)
    observador.start()


def iniciar_monitoramento():
    global pastas, observador
    pastas = [Path(pasta) for pasta in pasta_entry.get().split(";")]
    organizar_arquivos(pastas)
    monitorar_pastas(pastas)
    start_button.config(state=tk.DISABLED)
    pause_button.config(state=tk.NORMAL)


def pausar_monitoramento():
    global observador
    observador.stop()
    start_button.config(state=tk.NORMAL)
    pause_button.config(state=tk.DISABLED)


def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_entry.delete(0, tk.END)
        pasta_entry.insert(tk.END, pasta)


if __name__ == "__main__":
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

    observador = Observer()

    root = tk.Tk()
    root.title("Organizador de Arquivos")
    root.geometry("400x150")

    folder_label = tk.Label(root, text="Pasta:")
    folder_label.pack()

    pasta_entry = tk.Entry(root, width=50)
    pasta_entry.pack()

    select_button = tk.Button(root, text="Selecionar", command=selecionar_pasta)
    select_button.pack()

    start_button = tk.Button(root, text="Iniciar", command=iniciar_monitoramento)
    start_button.pack()

    pause_button = tk.Button(root, text="Pausar", command=pausar_monitoramento, state=tk.DISABLED)
    pause_button.pack()

    root.mainloop()
