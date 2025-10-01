import serial
import time
import re

ser = serial.Serial('COM5', 9600)  # ajusta a porta
time.sleep(2)  # espera o Arduino iniciar
directions = {
    'up': (0, -1),
    'right': (1, 0),
    'down': (0, 1),
    'left': (-1, 0),
}
direcoes = ['up', 'right', 'down', 'left']
dir_atual = "up"
idx_dir= 0

# def parse_sensor_data(line):
#     try:
#         parts = line.strip().split(',')
#         dist = int(parts[0].split(':')[1])
#         line_val = int(parts[1].split(':')[1])
#         return dist, line_val
#     except:
#         return None, None

# try:
#     while True:
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8')
#             dist, line_val = parse_sensor_data(line)
#             if dist is not None:
#                 print(f"Distância: {dist} cm, Linha: {line_val}")

#                 # Decidir comando
#                 if dist < 15 or line_val == 0:
#                     print("Obstáculo ou linha detectados - Parar")
#                     ser.write(b's')
#                 else:
#                     print("Caminho livre - Avançar")
#                     ser.write(b'f')
#         time.sleep(0.1)

# except KeyboardInterrupt:
#     print("Programa terminado")
#     ser.write(b's')
#     ser.close()


def frente():
    ser.write(b'f')
    print("➡️  Frente")
    

def tras():
    ser.write(b'b')
    print("⬅️  Trás")


def esquerda():
    global idx_dir, dir_atual
    ser.write(b'l')
    print("⬅️  Esquerda")
    idx_dir = (idx_dir - 1) % 4
    dir_atual = direcoes[idx_dir]

def direita():
    global idx_dir, dir_atual
    ser.write(b'r')
    print("➡️  Direita")
    idx_dir = (idx_dir+1) % 4
    dir_atual = direcoes[idx_dir]


print("Controlo manual do mBot via teclado")
print("Comandos:")
print("  w -> frente")
print("  s -> trás")
print("  a -> esquerda")
print("  d -> direita")
print("  espaço -> parar")
print("  q -> sair")

try:
    while True:
        key = input("Comando: ").lower()
        
        #verifica se nao tem nenhum obstáculo ou linha
        if key == 'w':
           frente()
        elif key == 's':
            tras()
        elif key == 'a':
            esquerda()
        elif key == 'd':
            direita()
        elif key == ' ':
            ser.write(b's')
            print("⏹️ Parar")
        elif key == 'q':
            ser.write(b's')  # parar antes de sair
            print("A sair...")
            break
        elif key == 'v':
            ser.write(b'v')
            print("🔍 Verificando obstáculos e linha (rotação 360°)")
            
            #-------------------------
            # Lê a resposta do Arduino
            #-------------------------

            resposta_raw = ser.readline()
            resposta = resposta_raw.decode(errors='ignore').strip()
            print("📡 Leituras brutas:", resposta)
            # Regex para extrair todos os números da string
            valores = list(map(int, re.findall(r'\d+', resposta)))
            print("📡 Leituras convertidas:", valores)
            
            #-------------------------
            #Coloca barreiras
            #-------------------------
            LIMIAR_CM = 15

            bloqueios = set()
            posicao_atual = (0, 0)
            pos = posicao_atual  # posição (x, y) atual do robô
            
            # Função para mapear leitura do sensor para direção absoluta
            def obter_direcao_absoluta(indice_leitura, orientacao_inicial_idx):
                """
                Mapeia uma leitura do sensor para direção absoluta
                
                Args:
                    indice_leitura: 0=frente, 1=direita, 2=trás, 3=esquerda (relativo ao robô)
                    orientacao_inicial_idx: índice da direção inicial do robô (0=up, 1=right, 2=down, 3=left)
                
                Returns:
                    tuple: (direção_absoluta_string, direção_absoluta_idx)
                """
                direcao_absoluta_idx = (orientacao_inicial_idx + indice_leitura) % 4
                direcao_absoluta = direcoes[direcao_absoluta_idx]
                return direcao_absoluta, direcao_absoluta_idx
            
            # Direções relativas ao robô durante a rotação 360°
            direcoes_relativas = ['frente', 'direita', 'tras', 'esquerda']
            
            print(f"🧭 Orientação inicial do robô: {dir_atual} (idx_dir = {idx_dir})")
            print(f"📏 Análise das leituras:")
            
            for i, dist in enumerate(valores):
                direcao_abs, direcao_abs_idx = obter_direcao_absoluta(i, idx_dir)
                print(f"  Leitura {i} ({direcoes_relativas[i]}): {dist} cm → Direção absoluta: {direcao_abs}")
                
                if dist < LIMIAR_CM:
                    print(f"    🚧 Obstáculo detectado!")
                    dx, dy = directions[direcao_abs]
                    vizinho = (pos[0] + dx, pos[1] + dy)
                    bloqueios.add((pos, vizinho))
            
            print("🚧 Bloqueios detectados:", bloqueios)
        
        else:
            print("❌ Comando inválido. Usa W, A, S, D, Z, X, espaço ou Q.")
        print(idx_dir)
        print(dir_atual)
except KeyboardInterrupt:
    print("Programa terminado")
    ser.write(b's')