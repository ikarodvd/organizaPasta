import os  # Importa o módulo 'os' para interagir com o sistema operacional
import argparse  # Importa o módulo 'argparse' para lidar com argumentos de linha de comando
import shutil  # Importa o módulo 'shutil' para manipular arquivos e diretórios
from pathlib import (
    Path,
)  # Importa a classe 'Path' do módulo 'pathlib' para lidar com caminhos de arquivos
from watchdog.observers import (
    Observer,
)  # Importa a classe 'Observer' do módulo 'watchdog.observers' para monitorar eventos de sistema de arquivos
from watchdog.events import (
    FileSystemEventHandler,
)  # Importa a classe 'FileSystemEventHandler' do módulo 'watchdog.events' para manipular eventos de sistema de arquivos


class FileHandler(
    FileSystemEventHandler
):  # Define a classe 'FileHandler' que herda da classe 'FileSystemEventHandler'
    def __init__(self, folders):  # Define o método de inicialização da classe
        super(
            FileHandler, self
        ).__init__()  # Chama o método de inicialização da classe pai
        self.folders = (
            folders  # Armazena as pastas a serem monitoradas em um atributo da classe
        )

    def on_created(
        self, event
    ):  # Define o método 'on_created' que será chamado quando um arquivo for criado
        if (
            event.is_directory
        ):  # Verifica se o evento é um diretório (ignora diretórios)
            return

        file_path = event.src_path  # Obtém o caminho do arquivo criado
        extension = Path(
            file_path
        ).suffix.lower()  # Obtém a extensão do arquivo em letras minúsculas

        if extension:  # Se houver uma extensão
            target_folder = self.find_target_folder(
                extension[1:]
            )  # Encontra a pasta de destino com base na extensão (ignora o ponto inicial)
        else:
            target_folder = self.find_target_folder(
                "sem_extensao"
            )  # Se não houver uma extensão, define a pasta de destino como "sem_extensao"

        if not target_folder.exists():  # Se a pasta de destino não existir
            target_folder.mkdir()  # Cria a pasta de destino

        target_file = (
            target_folder / Path(file_path).name
        )  # Define o caminho do arquivo de destino

        try:
            shutil.move(
                file_path, target_file
            )  # Move o arquivo para a pasta de destino
            print(
                f"Arquivo movido com sucesso: {file_path} -> {target_file}"
            )  # Exibe uma mensagem de sucesso
        except Exception as e:
            print(
                f"Erro ao mover o arquivo: {file_path} -> {target_file}"
            )  # Exibe uma mensagem de erro
            print(f"Detalhes do erro: {str(e)}")  # Exibe os detalhes do erro

    def find_target_folder(
        self, extension
    ):  # Define o método 'find_target_folder' para encontrar a pasta de destino
        for folder in self.folders:  # Percorre as pastas a serem monitoradas
            target_folder = (
                folder / extension
            )  # Define a pasta de destino com base na extensão
            if target_folder.exists():  # Se a pasta de destino existir
                return target_folder  # Retorna a pasta de destino
        return (
            self.folders[0] / extension
        )  # Se a pasta de destino não existir, retorna a primeira pasta com a extensão


def create_folders_for_extensions(
    folders,
):  # Define a função 'create_folders_for_extensions' para criar as pastas de destino para cada extensão
    extensions = set()  # Cria um conjunto vazio para armazenar as extensões únicas

    for folder in folders:  # Percorre as pastas a serem monitoradas
        for file in folder.iterdir():  # Percorre os arquivos em cada pasta
            if file.is_file():  # Verifica se é um arquivo
                extension = (
                    file.suffix.lower()
                )  # Obtém a extensão do arquivo em letras minúsculas
                extensions.add(
                    extension
                )  # Adiciona a extensão ao conjunto de extensões

    for folder in folders:  # Percorre as pastas a serem monitoradas novamente
        for extension in extensions:  # Percorre as extensões
            target_folder = (
                folder / extension[1:]
            )  # Define a pasta de destino com base na extensão (ignora o ponto inicial)
            if not target_folder.exists():  # Se a pasta de destino não existir
                target_folder.mkdir()  # Cria a pasta de destino

    for folder in folders:  # Percorre as pastas a serem monitoradas novamente
        target_folder = (
            folder / "sem_extensao"
        )  # Define a pasta de destino para arquivos sem extensão
        if not target_folder.exists():  # Se a pasta de destino não existir
            target_folder.mkdir()  # Cria a pasta de destino


def organize_files(
    folders,
):  # Define a função 'organize_files' para organizar os arquivos nas pastas de destino
    create_folders_for_extensions(
        folders
    )  # Cria as pastas de destino para as extensões

    for folder in folders:  # Percorre as pastas a serem monitoradas
        for file in folder.iterdir():  # Percorre os arquivos em cada pasta
            if file.is_file():  # Verifica se é um arquivo
                extension = (
                    file.suffix.lower()
                )  # Obtém a extensão do arquivo em letras minúsculas
                if extension:  # Se houver uma extensão
                    target_folder = (
                        folder / extension[1:]
                    )  # Define a pasta de destino com base na extensão (ignora o ponto inicial)
                else:
                    target_folder = (
                        folder / "sem_extensao"
                    )  # Se não houver uma extensão, define a pasta de destino como "sem_extensao"
                target_file = (
                    target_folder / file.name
                )  # Define o caminho do arquivo de destino
                shutil.move(
                    str(file), str(target_file)
                )  # Move o arquivo para a pasta de destino


def watch_folders(folders):  # Define a função 'watch_folders' para monitorar as pastas
    event_handler = FileHandler(
        folders
    )  # Cria uma instância da classe 'FileHandler' passando as pastas a serem monitoradas
    observer = Observer()  # Cria uma instância do observador
    for folder in folders:  # Percorre as pastas a serem monitoradas
        observer.schedule(
            event_handler, folder, recursive=True
        )  # Adiciona a pasta ao observador, habilitando a recursividade
    observer.start()  # Inicia a observação das pastas

    try:
        while True:
            pass  # Permanece em loop infinito (ou até ser interrompido manualmente)
    except KeyboardInterrupt:
        observer.stop()  # Se for interrompido manualmente, para a observação

    observer.join()  # Aguarda até que a observação seja completamente encerrada


if (
    __name__ == "__main__"
):  # Executa o código somente se este arquivo for o arquivo principal
    parser = argparse.ArgumentParser(
        description="Monitora e organiza arquivos em uma pasta baseando-se em suas extensões."
    )
    parser.add_argument(
        "--folders",
        nargs="*",
        default=[Path(os.getcwd())],
        help="Pastas para monitorar",
    )

    args = parser.parse_args()  # Analisa os argumentos de linha de comando
    folders = [
        Path(folder) for folder in args.folders
    ]  # Converte as pastas fornecidas em objetos 'Path'

    organize_files(folders)  # Organiza os arquivos nas pastas de destino
    watch_folders(folders)  # Inicia a monitoração das pastas
