from machine import Pin, ADC
import time

# Configuração
LIMIAR_BAIXO = 100
LIMIAR_ALTO = 500
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
ultimo_tempo_botao = 0
print("Contador de Producao Inicializado")
while True:
    valor = ldr.read()

    if valor < LIMIAR_BAIXO:
        if not peca_passando:
            peca_passando = True
            inicio_bloqueio = time.ticks_ms()

    elif valor > LIMIAR_ALTO:
        if peca_passando:
            contador += 1
            print("Peca detectada! Total:", contador)
            peca_passando = False
            inicio_bloqueio = None
            micro_parada_detectada = False

    if peca_passando and not micro_parada_detectada:
        if time.ticks_diff(time.ticks_ms(), inicio_bloqueio) >= TEMPO_MICRO_PARADA:
            print("Alerta: Micro-parada detectada!")
            micro_parada_detectada = True

    estado_botao = botao.value()
    agora = time.ticks_ms()

    if (
        ultimo_estado_botao == 1
        and estado_botao == 0
        and time.ticks_diff(agora, ultimo_tempo_botao) > 200
    ):
        contador = 0
        peca_passando = False
        inicio_bloqueio = None
        micro_parada_detectada = False
        print("Turno resetado com sucesso. Contadores zerados.")
        ultimo_tempo_botao = agora

    ultimo_estado_botao = estado_botao

    time.sleep_ms(50)