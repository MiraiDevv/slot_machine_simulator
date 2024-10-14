import random
import time
import sys

def slot_machine():
    print("Bem-vindo ao Cassino Python!")
    saldo = 1000  # Saldo inicial do jogador
    aposta_minima = 10
    total_ganho = 0
    total_perdido = 0
    total_jogos = 0
    vitorias = 0
    derrotas = 0
    chance_de_ganhar = 30  # Chance inicial de ganhar (em porcentagem)
    simbolos = ['A', 'B', 'C', 'D', '7', '@', '#', '$']  # Símbolos das slots

    while True:
        print(f"\nSeu saldo atual é: R${saldo}")
        print(f"Total ganho: R${total_ganho}")
        print(f"Total perdido: R${total_perdido}")
        if total_jogos > 0:
            porcentagem_vitorias = (vitorias / total_jogos) * 100
            porcentagem_derrotas = (derrotas / total_jogos) * 100
        else:
            porcentagem_vitorias = porcentagem_derrotas = 0
        print(f"Vitórias: {vitorias} vezes ({porcentagem_vitorias:.2f}%)")
        print(f"Derrotas: {derrotas} vezes ({porcentagem_derrotas:.2f}%)")
        aposta = input(f"Digite o valor da sua aposta (ou 'sair' para encerrar): ")

        if aposta.lower() == 'sair':
            print("Obrigado por jogar! Até a próxima.")
            break

        if not aposta.isdigit() or int(aposta) < aposta_minima:
            print(f"Aposta inválida! A aposta mínima é R${aposta_minima}.")
            continue

        aposta = int(aposta)

        if aposta > saldo:
            print("Saldo insuficiente para essa aposta.")
            continue

        saldo -= aposta

        # Decidir antecipadamente se o jogador vai ganhar ou perder
        resultado = random.randint(1, 100)
        ganhou = resultado <= chance_de_ganhar

        # Incrementar o contador de jogos
        total_jogos += 1

        # Animação dos slots girando
        print("Girando as slots...")
        slot1, slot2, slot3 = slots_animacao(simbolos, ganhou)

        # Verificar o resultado final
        if ganhou:
            premio = aposta * 5  # O prêmio é 5 vezes a aposta
            saldo += premio
            total_ganho += premio
            vitorias += 1
            print(f"| {slot1} | {slot2} | {slot3} |")
            print(f"Parabéns! Você ganhou R${premio}!")
            # Diminuir a chance de ganhar em 10%, até o mínimo de 0%
            chance_de_ganhar = max(chance_de_ganhar - 10, 0)
        else:
            total_perdido += aposta
            derrotas += 1
            print(f"| {slot1} | {slot2} | {slot3} |")
            print("Você perdeu! Tente novamente.")

        if saldo < aposta_minima:
            print("Seu saldo é insuficiente para continuar jogando.")
            break

    print(f"\nEstatísticas finais:")
    print(f"Total de jogos: {total_jogos}")
    print(f"Vitórias: {vitorias} vezes ({(vitorias / total_jogos) * 100:.2f}%)")
    print(f"Derrotas: {derrotas} vezes ({(derrotas / total_jogos) * 100:.2f}%)")
    print(f"Saldo final: R${saldo}")

def slots_animacao(simbolos, ganhou):
    # Definir tempos de parada para cada slot
    tempos_de_parada = [random.uniform(0.5, 1.5) for _ in range(3)]
    tempos_acumulados = [sum(tempos_de_parada[:i+1]) for i in range(3)]
    max_tempo = tempos_acumulados[-1]

    start_time = time.time()
    slots = [' ', ' ', ' ']  # Slots iniciais vazios
    slot_final = [None, None, None]

    while True:
        current_time = time.time() - start_time

        for i in range(3):
            if slot_final[i] is None:
                if current_time >= tempos_acumulados[i]:
                    if ganhou and i == 0:
                        # Se ganhou, definir o símbolo vencedor no primeiro slot
                        simbolo_vencedor = random.choice(simbolos)
                        slots[i] = simbolo_vencedor
                        slot_final[i] = simbolo_vencedor
                    elif ganhou:
                        # Replicar o símbolo vencedor nos slots subsequentes
                        slots[i] = simbolo_vencedor
                        slot_final[i] = simbolo_vencedor
                    else:
                        # Se perdeu, escolher um símbolo aleatório
                        slots[i] = random.choice(simbolos)
                        slot_final[i] = slots[i]
                else:
                    # Enquanto não parar, continuar girando
                    slots[i] = random.choice(simbolos)

        sys.stdout.write('\r' + f"| {slots[0]} | {slots[1]} | {slots[2]} |")
        sys.stdout.flush()
        time.sleep(0.05)

        if all(slot_final):
            break

    print()  # Pular para a próxima linha após a animação

    # Garantir que, se perdeu, os três símbolos não sejam iguais
    if not ganhou and slot_final[0] == slot_final[1] == slot_final[2]:
        while slot_final[2] == slot_final[0]:
            slot_final[2] = random.choice(simbolos)
        print(f"| {slot_final[0]} | {slot_final[1]} | {slot_final[2]} |")

    return slot_final[0], slot_final[1], slot_final[2]

if __name__ == "__main__":
    slot_machine()
