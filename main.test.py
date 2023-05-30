import os
import random
import string


def generate_random_extension():
    extensions = [".txt", ".doc", ".pdf", ".jpg", ".png", ".mp3", ".mp4", ".exe"]
    return random.choice(extensions)


def generate_random_filename(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_files(num_files, output_folder):
    for i in range(num_files):
        extension = generate_random_extension()
        filename = generate_random_filename(8)
        file_path = os.path.join(output_folder, f"{filename}{extension}")
        with open(file_path, "w") as file:
            file.write("This is a sample file.")


output_folder = "arquivos"
num_files = 1000

# Cria a pasta de saída se não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

generate_files(num_files, output_folder)
print(f'{num_files} arquivos gerados na pasta "{output_folder}".')
