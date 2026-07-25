from machine import Pin, ADC
import time

# Configuração
LIMIAR_BAIXO = 1200
LIMIAR_ALTO = 1800
TEMPO_MICRO_PARADA = 5000

# Sensor LDR
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)

# Botão
botao = Pin(18, Pin.IN, Pin.PULL_UP)

# Variáveis
contador = 0
peca_passando = False
inicio_bloqueio = None
micro_parada_detectada = False

ultimo_estado_botao = 1

print("Contador de Producao Inicializado")

while True:
    # Leitura do sensor
    valor = ldr.read()

    # Detecta início da passagem da peça
    if valor > LIMIAR_ALTO:
        if not peca_passando:
            peca_passando = True
            inicio_bloqueio = time.ticks_ms()

    # Detecta fim da passagem da peça
    elif valor < LIMIAR_BAIXO:
        if peca_passando:
            contador += 1
            print("Peca detectada! Total:", contador)
            peca_passando = False
            inicio_bloqueio = None
            micro_parada_detectada = False

    # Detecta micro-parada
    if peca_passando and not micro_parada_detectada:
        if time.ticks_diff(time.ticks_ms(), inicio_bloqueio) >= TEMPO_MICRO_PARADA:
            print("Alerta: Micro-parada detectada!")
            micro_parada_detectada = True

    # Leitura do botão
    estado_botao = botao.value()

    # Detecta o pressionamento do botão
    if estado_botao == 0 and ultimo_estado_botao == 1:
        contador = 0
        peca_passando = False
        inicio_bloqueio = None
        micro_parada_detectada = False
        print("Turno resetado com sucesso. Contadores zerados.")

    ultimo_estado_botao = estado_botao

    time.sleep_ms(50)