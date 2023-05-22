# Organizador de Arquivos por Extensão

Este programa monitora uma pasta especificada e organiza os arquivos presentes nela em subpastas com base em suas extensões. Os arquivos são movidos para as pastas correspondentes de acordo com sua extensão.

## Requisitos

- Python 3.x
- Bibliotecas Python: `watchdog`, `pystray`

## Instalação

1. Clone ou baixe este repositório para o seu computador.

2. Certifique-se de ter o Python 3.x instalado em seu sistema. Caso contrário, faça o download e a instalação a partir do site oficial do Python.

3. Instale as bibliotecas Python necessárias executando o seguinte comando no terminal:

## Uso

Execute o programa usando o seguinte comando:

- `[caminho_da_pasta]` (opcional): Especifique o caminho da pasta que deseja monitorar e organizar. Se nenhum caminho for fornecido, o programa monitorará a pasta em que o arquivo `main.py` está localizado.

O programa ficará em execução, monitorando a pasta especificada. Sempre que um novo arquivo for criado na pasta, ele será movido para a pasta correspondente de acordo com sua extensão. Além disso, o programa verificará se existem arquivos existentes na pasta e os organizará também.

## Notas

- O arquivo `main.py` não será movido para nenhuma pasta durante a organização.
- Se um arquivo não tiver uma extensão, ele será movido para a pasta "sem_extensao".

## Personalização

- Ícone da bandeja do sistema: Se você deseja personalizar o ícone exibido na bandeja do sistema, substitua o arquivo `icone.png` pelo seu próprio ícone com o mesmo nome e extensão PNG.

## Contribuição

Sinta-se à vontade para contribuir para este projeto abrindo problemas (issues) ou enviando solicitações de pull (pull requests).

Se você encontrar algum problema ou tiver alguma sugestão, por favor, abra um problema ou entre em contato.

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).
