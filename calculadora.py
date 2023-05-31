import math


def calcular_equacao_segundo_grau(a, b, c):
    if a == 0:
        raise ValueError(
            "O coeficiente 'a' não pode ser zero. Não é uma equação de segundo grau válida."
        )

    delta = b**2 - 4 * a * c

    if delta < 0:
        print("A equação não possui raízes reais.")
    elif delta == 0:
        raiz = -b / (2 * a)
        print("A equação possui uma raiz real:", raiz)
    else:
        raiz1 = (-b + math.sqrt(delta)) / (2 * a)
        raiz2 = (-b - math.sqrt(delta)) / (2 * a)
        print("A equação possui duas raízes reais:")
        print("Raiz 1:", raiz1)
        print("Raiz 2:", raiz2)


# Exemplo de uso com tratamento de erros
try:
    a = float(input("Digite o coeficiente 'a': "))
    b = float(input("Digite o coeficiente 'b': "))
    c = float(input("Digite o coeficiente 'c': "))

    calcular_equacao_segundo_grau(a, b, c)

except ValueError as e:
    print("Erro:", str(e))
except Exception as e:
    print("Ocorreu um erro inesperado:", str(e))
