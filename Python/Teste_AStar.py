import serial
import time
import heapq

# Inicializar comunicação serial
ser = serial.Serial('COM5', 9600)
time.sleep(2)

# Direções e seus vetores
directions = {
    'up': (0, -1),
    'right': (1, 0),
    'down': (0, 1),
    'left': (-1, 0),
}

ord_direcoes = ['up', 'right', 'down', 'left']

# Lista de transições bloqueadas (arestas)
arestas_bloqueadas = set()

# Funções de movimento
def frente():
    ser.write(b'f')
    print("➡️  Frente")

def tras():
    ser.write(b'b')
    print("⬅️  Trás")

def esquerda():
    ser.write(b'l')
    print("⬅️  Esquerda")

def direita():
    ser.write(b'r')
    print("➡️  Direita")

def parar():
    ser.write(b's')
    print("⏹️ Parar")

def rodar_horario():
    ser.write(b'z')
    print("↻ Rodar sentido horário")

def rodar_antihorario():
    ser.write(b'x')
    print("↺ Rodar sentido anti-horário")

# Função heurística para A* (distância de Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* com verificação de arestas bloqueadas
def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        x, y = current
        for dir_nome, (dx, dy) in directions.items():
            neighbor = (x + dx, y + dy)
            nx, ny = neighbor
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if ((current, neighbor) in arestas_bloqueadas or
                    (neighbor, current) in arestas_bloqueadas):
                    continue
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
    return None

# Rodar o robô para a direção desejada
def ajustar_direcao(direcao_atual, direcao_desejada):
    idx_atual = ord_direcoes.index(direcao_atual)
    idx_desejado = ord_direcoes.index(direcao_desejada)
    diff = (idx_desejado - idx_atual) % 4

    if diff == 1:
        direita()
    elif diff == 2:
        direita()
        time.sleep(0.5)
        direita()
    elif diff == 3:
        esquerda()

    time.sleep(0.5)
    return direcao_desejada

# Verificar barreiras nas 4 direções a partir da posição atual
def verificar_barreiras(pos):
    ser.write(b'v')  # comando para o Arduino fazer varredura
    print("🔄 Verificando barreiras em 360°...")

    try:
        resposta = ser.readline().decode().strip()
        #print("📡 Leituras:", resposta)
        valores = list(map(int, resposta.split(',')))
        

        if len(valores) != 4:
            print("❌ Dados incompletos do sensor.")
            return

        LIMIAR_CM = 15
        for i, dist in enumerate(valores):
            if dist < LIMIAR_CM:
                dir_nome = ord_direcoes[i]
                dx, dy = directions[dir_nome]
                vizinho = (pos[0] + dx, pos[1] + dy)
                arestas_bloqueadas.add((pos, vizinho))
                print(f"🚧 Barreira detetada entre {pos} -> {vizinho}")

    except Exception as e:
        print("Erro ao ler sensores:", e)

# Imprimir estado do tabuleiro com o agente
def imprimir_tabuleiro(grid, pos):
    for y in range(len(grid)):
        linha = ""
        for x in range(len(grid[0])):
            if (x, y) == pos:
                linha += "🤖 "
            else:
                linha += "⬜️ "
        print(linha)
    print()

# Executar caminho com inputs e varredura de barreiras
def executar_caminho_com_input(path):
    if not path or len(path) < 2:
        print("Nenhum caminho para executar.")
        return

    direcao_atual = 'up'
    pos_atual = path[0]

    for i in range(1, len(path)):
        imprimir_tabuleiro(grid, pos_atual)

        verificar_barreiras(pos_atual)

        proximo = path[i]
        dx = proximo[0] - pos_atual[0]
        dy = proximo[1] - pos_atual[1]

        if dx == 1 and dy == 0:
            dir_esperada = 'right'
        elif dx == -1 and dy == 0:
            dir_esperada = 'left'
        elif dx == 0 and dy == 1:
            dir_esperada = 'down'
        elif dx == 0 and dy == -1:
            dir_esperada = 'up'
        else:
            print("Movimento inválido entre", pos_atual, proximo)
            return

        input(f"➡️  Pressione Enter para mover de {pos_atual} para {proximo}...")

        direcao_atual = ajustar_direcao(direcao_atual, dir_esperada)
        frente()
        time.sleep(1)
        parar()

        pos_atual = proximo

    imprimir_tabuleiro(grid, pos_atual)
    print("✅ Chegou ao objetivo!")

# Tabuleiro de teste
grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)
goal = (4, 4)

caminho = astar(grid, start, goal)

if caminho:
    print("📍 Caminho encontrado:")
    print(caminho)
    executar_caminho_com_input(caminho)
else:
    print("❌ Nenhum caminho encontrado.")
