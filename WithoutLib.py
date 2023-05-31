import os
import argparse
import shutil
import sys
import time


def ao_criar(evento, pastas):
    if evento.is_directory:
        return

    caminho_arquivo = evento.src_path
    extensao = os.path.splitext(caminho_arquivo)[1].lower()

    if extensao:
        pasta_destino = encontrar_pasta_destino(extensao[1:], pastas)
    else:
        pasta_destino = encontrar_pasta_destino("sem_extensao", pastas)

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    arquivo_destino = os.path.join(pasta_destino, os.path.basename(caminho_arquivo))

    try:
        shutil.move(caminho_arquivo, arquivo_destino)
        print(f"Arquivo movido com sucesso: {caminho_arquivo} -> {arquivo_destino}")
    except Exception as e:
        print(f"Erro ao mover o arquivo: {caminho_arquivo} -> {arquivo_destino}")
        print(f"Detalhes do erro: {str(e)}")


def encontrar_pasta_destino(extensao, pastas):
    for pasta in pastas:
        pasta_destino = os.path.join(pasta, extensao)
        if os.path.exists(pasta_destino):
            return pasta_destino
    return os.path.join(pastas[0], extensao)


def criar_pastas_para_extensoes(pastas):
    extensoes = set()

    for pasta in pastas:
        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                extensao = os.path.splitext(arquivo)[1].lower()
                extensoes.add(extensao)

    for pasta in pastas:
        for extensao in extensoes:
            pasta_destino = os.path.join(pasta, extensao[1:])
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)

    for pasta in pastas:
        pasta_destino = os.path.join(pasta, "sem_extensao")
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)


def organizar_arquivos(pastas):
    criar_pastas_para_extensoes(pastas)

    for pasta in pastas:
        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                extensao = os.path.splitext(arquivo)[1].lower()
                if extensao:
                    pasta_destino = os.path.join(pasta, extensao[1:])
                else:
                    pasta_destino = os.path.join(pasta, "sem_extensao")
                arquivo_destino = os.path.join(pasta_destino, arquivo)
                shutil.move(caminho_arquivo, arquivo_destino)


def monitorar_pastas(pastas):
    tempos_ultima_modificacao = {}

    while True:
        for pasta in pastas:
            for arquivo in os.listdir(pasta):
                caminho_arquivo = os.path.join(pasta, arquivo)
                tempo_modificacao = os.path.getmtime(caminho_arquivo)

                if tempo_modificacao > tempos_ultima_modificacao.get(
                    caminho_arquivo, 0
                ):
                    tempos_ultima_modificacao[caminho_arquivo] = tempo_modificacao
                    ao_criar(caminho_arquivo, pastas)

        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monitora e organiza arquivos em uma pasta baseando-se em suas extensões."
    )
    parser.add_argument(
        "--pastas",
        nargs="*",
        default=[os.getcwd()],
        help="Pastas para monitorar",
    )

    args = parser.parse_args()

    pastas = args.pastas

    organizar_arquivos(pastas)
    monitorar_pastas(pastas)
