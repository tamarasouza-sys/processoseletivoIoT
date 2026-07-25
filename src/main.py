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

# Com PULL_UP:
# 1 = botão solto
# 0 = botão pressionado
ultimo_estado_botao = botao.value()

print("Contador de Producao Inicializado")

while True:
    # -------------------------
    # SENSOR LDR
    # -------------------------

    valor = ldr.read()

    # Início da passagem/bloqueio
    if valor > LIMIAR_ALTO:
        if not peca_passando:
            peca_passando = True
            inicio_bloqueio = time.ticks_ms()

    # Fim da passagem
    elif valor < LIMIAR_BAIXO:
        if peca_passando:
            contador += 1

            print("Peca detectada! Total:", contador)

            peca_passando = False
            inicio_bloqueio = None
            micro_parada_detectada = False

    # -------------------------
    # MICRO-PARADA
    # -------------------------

    if peca_passando and not micro_parada_detectada:
        if inicio_bloqueio is not None:
            tempo_bloqueado = time.ticks_diff(
                time.ticks_ms(),
                inicio_bloqueio
            )

            if tempo_bloqueado >= TEMPO_MICRO_PARADA:
                print("Alerta: Micro-parada detectada!")
                micro_parada_detectada = True

    # -------------------------
    # BOTÃO DE RESET
    # -------------------------

    estado_botao = botao.value()

    # Detecta a LIBERAÇÃO do botão:
    # estado anterior = 0 (pressionado)
    # estado atual    = 1 (solto)
    if ultimo_estado_botao == 0 and estado_botao == 1:
        contador = 0
        peca_passando = False
        inicio_bloqueio = None
        micro_parada_detectada = False

        print("Turno resetado com sucesso. Contadores zerados.")

    ultimo_estado_botao = estado_botao

    time.sleep_ms(50)