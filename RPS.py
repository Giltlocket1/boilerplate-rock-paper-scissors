# RPS.py

def player(prev_play, opponent_history=[]):
    # Guardamos el movimiento del oponente en el historial si no es el primer turno
    if prev_play:
        opponent_history.append(prev_play)
    else:
        # Si es el primer juego de una nueva partida, limpiamos el historial anterior
        opponent_history.clear()

    # Función auxiliar para saber qué jugada vence a otra
    def ideal_response(move):
        if move == "R":
            return "P"
        elif move == "P":
            return "S"
        else: # "S"
            return "R"

    # Turno 1 por defecto
    if len(opponent_history) == 0:
        return "R"

    # --- ESTRATEGIA CONTRA QUINCY ---
    # Quincy repite un patrón de 5 elementos exactos.
    quincy_pattern = ["R", "R", "P", "P", "S"]
    # Si llevamos suficientes jugadas, verificamos si cumple el patrón de Quincy
    if len(opponent_history) <= 10:
        # Mientras tanto, jugamos contraatacando un patrón cíclico simple o una constante
        # Para Quincy, su jugada en el índice i es quincy_pattern[i % 5]
        next_quincy_move = quincy_pattern[len(opponent_history) % len(quincy_pattern)]
        # Pero como estamos en el turno actual, evaluamos el siguiente
        predicted_quincy = quincy_pattern[len(opponent_history) % 5]
        return ideal_response(predicted_quincy)

    # Identificamos si es Quincy comprobando si encaja en su ciclo repetitivo
    is_quincy = True
    for i, move in enumerate(opponent_history):
        if move != quincy_pattern[i % 5]:
            is_quincy = False
            break
    
    if is_quincy:
        next_move = quincy_pattern[len(opponent_history) % 5]
        return ideal_response(next_move)

    # --- ESTRATEGIA GENERAL PARA MRUGESH, KRIS Y ABBEY (Basada en N-gramas / Markov) ---
    # En lugar de usar una sola lógica, rastreamos patrones de secuencias (historial de jugadas del oponente)
    
    # Buscamos patrones de 3 jugadas (sub-historial de los últimos 3 turnos del oponente)
    # Abbey y Mrugesh responden fuertemente a nuestras jugadas o patrones recientes.
    # Una técnica muy efectiva contra Abbey y Mrugesh es rastrear las secuencias de movimientos de NUESTRO propio jugador,
    # o bien predecir basándonos en la frecuencia de los últimos movimientos del oponente.

    # Estrategia de Frecuencia / Predicción de Markov de orden variable:
    # Contamos qué suele jugar el oponente después de ver una secuencia de longitud n.
    n = 3
    if len(opponent_history) > n:
        # Construimos un diccionario de frecuencias de secuencias
        last_n = tuple(opponent_history[-n-1:-1])
        
        # Busquemos todas las apariciones de esta secuencia last_n en el historial para ver qué jugó después
        element_following = {}
        for i in range(len(opponent_history) - n):
            seq = tuple(opponent_history[i:i+n])
            nxt = opponent_history[i+n]
            if seq == last_n:
                element_following[nxt] = element_following.get(nxt, 0) + 1
        
        if element_following:
            # Predecimos el movimiento más probable del oponente basándonos en su historial
            predicted_opponent_move = max(element_following, key=element_following.get)
            return ideal_response(predicted_opponent_move)

    # Fallback si el historial es corto o no hay coincidencia exacta:
    # Analizamos simplemente qué ha jugado más frecuentemente el oponente en total
    from collections import Counter
    counts = Counter(opponent_history)
    most_common = counts.most_common(1)[0][0]
    
    return ideal_response(most_common)