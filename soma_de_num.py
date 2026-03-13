import threading
import time

# -------------------------
# Ler números do arquivo
# -------------------------

def ler_arquivo(nome_arquivo):

    numeros = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:

        for linha in arquivo:

            linha = linha.strip()

            if linha:
                try:
                    numeros.append(int(linha))
                except ValueError:
                    print("Valor inválido encontrado:", linha)

    return numeros


# -------------------------
# Soma Serial
# -------------------------
def soma_serial(numeros):

    inicio = time.time()

    total = 0
    for n in numeros:
        total += n

    fim = time.time()

    print("\n--- Soma Serial ---")
    print("Resultado:", total)
    print("Tempo:", fim - inicio)

    return fim - inicio


# -------------------------
# Worker da Thread
# -------------------------
def worker(numeros, inicio, fim, resultados, index):

    soma = 0

    for i in range(inicio, fim):
        soma += numeros[i]

    resultados[index] = soma


# -------------------------
# Soma Paralela
# -------------------------
def soma_paralela(numeros, num_threads):

    tamanho = len(numeros)
    bloco = tamanho // num_threads

    threads = []
    resultados = [0] * num_threads

    inicio_tempo = time.time()

    for i in range(num_threads):

        inicio = i * bloco

        if i == num_threads - 1:
            fim = tamanho
        else:
            fim = (i + 1) * bloco

        t = threading.Thread(
            target=worker,
            args=(numeros, inicio, fim, resultados, i)
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total = sum(resultados)

    fim_tempo = time.time()

    print(f"\n--- Soma Paralela ({num_threads} threads) ---")
    print("Resultado:", total)
    print("Tempo:", fim_tempo - inicio_tempo)

    return fim_tempo - inicio_tempo


# -------------------------
# Programa principal
# -------------------------
def main():

    arquivo = "paralelo/numero2.txt"

    numeros = ler_arquivo(arquivo)

    print("\nEscolha quantidade de threads")
    print("1 - 2 threads")
    print("2 - 4 threads")
    print("3 - 8 threads")
    print("4 - 12 threads")

    opcao = int(input("Opção: "))

    mapa_threads = {
        1: 2,
        2: 4,
        3: 8,
        4: 12
    }

    num_threads = mapa_threads.get(opcao, 2)

    # executar serial
    soma_serial(numeros)

    # executar paralelo
    soma_paralela(numeros, num_threads)


if __name__ == "__main__":
    main()