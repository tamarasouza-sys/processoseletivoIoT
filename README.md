# Relatório do Candidato

## Identificação do Candidato

- **Nome completo:** Tâmara de Oliveira Souza
- **GitHub:** https://github.com/tamarasouza-sys

---

# Visão Geral da Solução

Este projeto apresenta a implementação de um sistema embarcado para realizar a **contagem de peças em uma esteira**, utilizando um ESP32, um sensor LDR e um botão de reset.

O funcionamento baseia-se na variação da luminosidade detectada pelo sensor. A passagem de uma peça provoca uma alteração no valor lido pelo LDR. O firmware identifica o início da passagem e, quando o sensor retorna ao estado correspondente à linha livre, registra uma nova peça produzida.

Além da contagem de produção, foi implementada a **detecção de micro-paradas**. Caso o sensor permaneça no estado de bloqueio por cinco segundos, o sistema gera um alerta indicando uma possível parada da esteira.

O sistema também possui um botão físico responsável pelo **reset do turno**, permitindo zerar o contador e os estados internos relacionados à passagem das peças e à detecção de micro-paradas.

---

# Arquitetura do Sistema Embarcado

O firmware foi desenvolvido em **MicroPython** para execução em um **ESP32 DevKit C V4**.

A lógica principal é executada continuamente através de um laço:

```python
while True:
```

Durante cada iteração, o sistema realiza:

- leitura do sensor LDR;
- identificação do início e do fim da passagem de uma peça;
- atualização do contador de produção;
- monitoramento do tempo de bloqueio do sensor;
- identificação de micro-paradas;
- leitura do estado do botão de reset;
- detecção da transição de liberação do botão;
- atualização das variáveis de estado;
- envio das mensagens necessárias pela interface serial.

A implementação utiliza variáveis de estado para evitar múltiplas contagens durante a passagem de uma única peça.

---

# Componentes Utilizados na Simulação

A simulação foi desenvolvida no ambiente **Wokwi**, utilizando os seguintes componentes:

- ESP32 DevKit C V4;
- Sensor fotoresistor (LDR);
- Botão de pressão (Push Button);
- Monitor Serial do Wokwi.

No projeto, o sensor LDR é identificado como `ldr1` e sua saída analógica está conectada ao **GPIO 34** do ESP32.

O botão é identificado como `btn1` e está conectado ao **GPIO 18**, configurado no firmware utilizando `Pin.PULL_UP`.

A interface serial é utilizada para apresentar as mensagens de inicialização, contagem de peças, micro-parada e reset do turno.

---

# Lógica de Detecção de Peças

Para interpretar os valores provenientes do LDR, foram definidos dois limiares:

```python
LIMIAR_BAIXO = 1200
LIMIAR_ALTO = 1800
```

Quando a leitura ultrapassa o `LIMIAR_ALTO`, o firmware considera que ocorreu o início da condição correspondente à passagem ou bloqueio da peça e registra o instante utilizando `time.ticks_ms()`.

Quando posteriormente a leitura fica abaixo do `LIMIAR_BAIXO`, o sistema considera que a passagem foi concluída e incrementa o contador.

A mensagem enviada pela serial é:

```text
Peca detectada! Total: X
```

onde `X` representa o número acumulado de peças.

A utilização de dois limiares distintos também cria uma faixa intermediária na qual o estado atual é mantido, evitando que pequenas variações próximas a um único valor de referência provoquem alterações sucessivas de estado.

---

# Detecção de Micro-paradas

O sistema monitora o período durante o qual permanece na condição de passagem ou bloqueio.

O tempo limite utilizado é:

```python
TEMPO_MICRO_PARADA = 5000
```

correspondente a **5 segundos**.

O instante inicial é armazenado utilizando:

```python
time.ticks_ms()
```

e o tempo decorrido é calculado com:

```python
time.ticks_diff()
```

Dessa forma, o controle é realizado sem utilizar uma espera de cinco segundos que interromperia a execução do programa.

Quando o tempo de bloqueio atinge o limite estabelecido, o sistema envia:

```text
Alerta: Micro-parada detectada!
```

A variável `micro_parada_detectada` impede que o mesmo alerta seja emitido continuamente durante uma única ocorrência.

---

# Reset Manual do Turno

O botão de reset está conectado ao GPIO 18 e utiliza o resistor de **pull-up interno** do ESP32:

```python
botao = Pin(18, Pin.IN, Pin.PULL_UP)
```

Nessa configuração, o firmware acompanha o estado atual e o estado anterior do botão.

A rotina de reset utilizada na versão final identifica a **liberação do botão**, correspondente à transição:

```text
0 -> 1
```

Quando essa transição é detectada, são reinicializadas as principais variáveis de controle:

- contador de peças;
- estado de passagem da peça;
- instante inicial do bloqueio;
- estado de detecção da micro-parada.

Em seguida, o sistema envia pela serial:

```text
Turno resetado com sucesso. Contadores zerados.
```

Essa implementação ficou compatível com a sequência de acionamento utilizada pelo cenário automatizado do Wokwi CI.

---

# Decisões Técnicas Relevantes

Para tornar a implementação organizada, confiável e compatível com os requisitos do projeto, foram adotadas algumas estratégias durante o desenvolvimento:

- definição de constantes para os limiares do sensor e o tempo de micro-parada;
- utilização de variáveis de estado para acompanhar a passagem das peças;
- utilização de `time.ticks_ms()` e `time.ticks_diff()` para temporização não bloqueante da micro-parada;
- acompanhamento do estado anterior e atual do botão para detectar sua transição;
- utilização de dois limiares para distinguir os estados associados à passagem da peça;
- manutenção das principais funcionalidades dentro de um único laço de execução;
- utilização da saída serial para integração com os cenários automatizados.

---

# Validação Automatizada

A solução foi validada através do **Wokwi CI integrado ao GitHub Actions**.

Foram executados três cenários automatizados para verificar as principais funcionalidades do sistema.

## Cenário 1 - Contagem Normal de Peças

O cenário altera a condição do LDR simulando a passagem de uma peça pela esteira.

O sistema identifica a passagem e apresenta:

```text
Peca detectada! Total: 1
```

**Resultado: aprovado.**

## Cenário 2 - Detecção de Micro-parada

O sensor permanece na condição de bloqueio por aproximadamente cinco segundos.

O firmware identifica a permanência excessiva nessa condição e apresenta:

```text
Alerta: Micro-parada detectada!
```

**Resultado: aprovado.**

## Cenário 3 - Reset Manual de Turno

O cenário automatizado simula o acionamento e a liberação do botão `btn1`.

Após detectar a transição de liberação, o sistema reinicializa as variáveis correspondentes ao turno e apresenta:

```text
Turno resetado com sucesso. Contadores zerados.
```

**Resultado: aprovado.**

---

# Resultados Obtidos

Ao final do desenvolvimento, o sistema apresentou o comportamento esperado para o cenário LIGHT.

Foram implementadas e validadas as seguintes funcionalidades:

- inicialização correta do sistema;
- leitura do sensor LDR;
- identificação da passagem das peças;
- contagem automática da produção;
- identificação de micro-paradas após cinco segundos de bloqueio;
- reset manual do turno através do botão;
- comunicação através da interface serial;
- integração com os cenários de teste do Wokwi CI;
- execução automatizada dos testes através do GitHub Actions.

Os **três cenários de validação foram concluídos com sucesso** na versão final do projeto.

---

# Comentários Adicionais

O desenvolvimento deste desafio permitiu aplicar conceitos relacionados a **sistemas embarcados, leitura de sensores analógicos, controle de estados e temporização não bloqueante utilizando MicroPython**.

A utilização do Wokwi possibilitou simular o comportamento do hardware e validar diferentes condições de funcionamento do sistema.

O projeto também envolveu o uso de **Git e GitHub para versionamento de código**, além do **GitHub Actions integrado ao Wokwi CI para validação automatizada**, permitindo verificar o comportamento do firmware após as atualizações realizadas no repositório.

Durante o desenvolvimento, os cenários automatizados também foram utilizados como ferramenta de diagnóstico. A análise das leituras do sensor permitiu ajustar os limiares utilizados pelo firmware, enquanto a validação do botão levou ao ajuste da detecção do evento de reset para a transição de liberação.

Ao final, foi obtida uma solução organizada, legível, compatível com os requisitos apresentados e **aprovada nos três cenários automatizados de validação**.