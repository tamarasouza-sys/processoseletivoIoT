# Relatório do Candidato

## Identificação do Candidato

- **Nome completo:** Tâmara de Oliveira Souza
- **GitHub:** https://github.com/tamarasouza-sys

---

# Visão Geral da Solução

Este projeto apresenta a implementação de um sistema embarcado para realizar a contagem de peças em uma esteira utilizando um ESP32, um sensor LDR e um botão de reset.

O funcionamento baseia-se na variação da luminosidade detectada pelo sensor. Sempre que uma peça altera a luminosidade sobre o sensor e, em seguida, a condição retorna ao estado normal, o sistema registra uma nova peça produzida.

Também foi implementada a identificação de micro-paradas quando o sensor permanece na condição de detecção de peça por um período igual ou superior a cinco segundos.

O botão de reset permite reiniciar o contador de produção e as variáveis relacionadas ao estado atual do sistema.

---

# Arquitetura do Sistema Embarcado

O firmware foi desenvolvido em MicroPython e utiliza um laço principal (`while True`) para executar continuamente as tarefas do sistema.

Durante a execução são realizadas as seguintes operações:

- leitura constante do sensor LDR;
- identificação do início da passagem de uma peça;
- identificação do fim da passagem da peça;
- atualização do contador de produção;
- monitoramento do tempo de permanência da peça sobre o sensor;
- detecção de micro-paradas;
- leitura do botão de reset;
- reinicialização das variáveis do sistema quando o botão é acionado;
- envio de mensagens de status para o monitor serial.

A lógica foi estruturada em um único laço principal, permitindo que o ESP32 monitore continuamente o sensor e o botão.

---

# Componentes Utilizados na Simulação

Os componentes utilizados na simulação foram:

- ESP32 DevKit V4;
- Sensor fotoresistor (LDR);
- Botão de pressão (Push Button);
- Monitor Serial do Wokwi.

Cada componente possui uma função específica no sistema.

O ESP32 executa o firmware e processa as informações recebidas dos dispositivos de entrada.

O sensor LDR é utilizado para identificar a passagem das peças através da variação da luminosidade.

O botão permite realizar o reset manual do contador de produção.

O monitor serial é utilizado para acompanhar as mensagens geradas pelo sistema durante a execução e também para permitir a validação dos cenários de teste.

---

# Decisões Técnicas Relevantes

Para tornar a implementação organizada e compatível com os requisitos do desafio, foram adotadas algumas estratégias durante o desenvolvimento.

Foram definidos dois limites para a leitura do sensor:

- `LIMIAR_BAIXO = 1200`;
- `LIMIAR_ALTO = 1800`.

A utilização de dois valores de referência permite distinguir os estados utilizados pela lógica de detecção da passagem das peças.

Para controlar o estado da peça sobre o sensor foi utilizada a variável `peca_passando`.

Quando a leitura do sensor ultrapassa o limite estabelecido para o início da detecção, o sistema registra que existe uma peça passando e armazena o instante em que essa condição começou.

Quando a leitura retorna para a condição abaixo do limite inferior, o sistema considera que a passagem foi concluída e incrementa o contador de produção.

Para o controle de tempo foram utilizadas as funções:

- `time.ticks_ms()`;
- `time.ticks_diff()`.

Essas funções permitem calcular durante quanto tempo o sensor permanece na condição de detecção.

O tempo definido para caracterizar uma micro-parada foi:

`TEMPO_MICRO_PARADA = 5000`

Portanto, caso a condição permaneça ativa por cinco segundos, o sistema gera a mensagem de alerta de micro-parada.

Também foi implementada a leitura do botão de reset, permitindo reiniciar o contador e as variáveis relacionadas ao estado atual do sistema.

---

# Funcionamento da Contagem de Peças

O sistema realiza continuamente a leitura analógica do sensor LDR através do ADC do ESP32.

Quando o valor lido ultrapassa o `LIMIAR_ALTO`, o sistema considera que uma peça começou a passar pelo ponto de detecção.

Nesse momento:

- `peca_passando` recebe o valor `True`;
- o instante inicial é armazenado utilizando `time.ticks_ms()`.

Quando o valor do sensor posteriormente fica abaixo do `LIMIAR_BAIXO`, o sistema identifica que a passagem da peça foi concluída.

O contador é então incrementado e uma mensagem é enviada ao monitor serial informando o total de peças detectadas.

Exemplo:

`Peca detectada! Total: 1`

---

# Detecção de Micro-parada

Além da contagem das peças, o sistema monitora durante quanto tempo uma peça permanece na região do sensor.

Quando uma peça é detectada, o instante inicial da detecção é armazenado.

Durante as próximas execuções do laço principal, o programa compara o tempo atual com o instante inicial utilizando `time.ticks_diff()`.

Se o tempo atingir cinco segundos sem que a condição de passagem seja finalizada, o sistema considera que ocorreu uma micro-parada.

Nesse caso, a seguinte mensagem é enviada ao monitor serial:

`Alerta: Micro-parada detectada!`

A variável `micro_parada_detectada` impede que a mesma micro-parada gere repetidamente a mensagem de alerta.

---

# Reset Manual do Turno

O sistema também possui um botão conectado ao ESP32 para realizar o reset manual do turno.

Quando o acionamento do botão é detectado, o sistema reinicia as principais variáveis utilizadas durante o funcionamento:

- contador de peças;
- estado de passagem da peça;
- instante inicial do bloqueio;
- estado de detecção de micro-parada.

Após o reset, o sistema pode continuar normalmente a contagem das próximas peças.

O funcionamento do botão também foi validado através de um cenário automatizado no Wokwi.

---

# Testes Automatizados

A validação da solução foi realizada através do GitHub Actions utilizando a integração com o Wokwi.

Foram utilizados três cenários automatizados para verificar as principais funcionalidades implementadas.

## Teste 1 — Contagem Normal de Peças

O primeiro cenário verifica o funcionamento da contagem de produção.

O teste simula uma alteração no sensor correspondente à passagem de uma peça e verifica se o sistema registra corretamente a contagem.

A mensagem utilizada para validar o funcionamento é:

`Peca detectada! Total: 1`

O cenário foi executado com sucesso.

## Teste 2 — Detecção de Micro-parada na Esteira

O segundo cenário verifica a identificação de uma micro-parada.

O sensor permanece na condição de detecção por tempo suficiente para atingir o limite de cinco segundos definido no firmware.

Após esse período, o sistema deve gerar a mensagem:

`Alerta: Micro-parada detectada!`

O cenário foi executado com sucesso.

## Teste 3 — Reset Manual de Turno

O terceiro cenário verifica o funcionamento do botão de reset.

Durante o teste, o botão é acionado através do cenário de simulação do Wokwi.

O sistema detecta o acionamento e reinicia os dados relacionados ao turno.

O cenário foi executado com sucesso.

---

# Resultados Obtidos

Ao final do desenvolvimento, o sistema apresentou o comportamento esperado para o cenário LIGHT.

Foram implementadas e validadas as seguintes funcionalidades:

- inicialização correta do sistema;
- contagem automática das peças detectadas pelo sensor LDR;
- identificação de micro-paradas quando a condição de detecção permanece ativa por cinco segundos;
- reinicialização do contador e das variáveis de estado através do botão de reset;
- comunicação das informações através do monitor serial;
- compatibilidade com os cenários automatizados de validação.

A validação foi realizada através do GitHub Actions utilizando a integração com o Wokwi.

Foram executados três cenários de teste:

- `test_1` — Contagem normal de peças;
- `test_2` — Detecção de micro-parada na esteira;
- `test_3` — Reset manual de turno.

Após a execução final do workflow, os três cenários foram concluídos com sucesso, validando o funcionamento da solução implementada.

---

# Integração Contínua

O projeto utiliza GitHub Actions para realizar automaticamente a construção e os testes da solução.

Após o envio das alterações para o repositório remoto, o workflow executa as etapas necessárias para preparar o projeto e iniciar os testes utilizando o Wokwi CLI.

Essa abordagem permite verificar automaticamente se as funcionalidades implementadas continuam compatíveis com os cenários definidos para o desafio.

Durante o desenvolvimento ocorreram algumas execuções que não foram concluídas devido a problemas temporários de comunicação com a API de simulação.

Após a reexecução do workflow, os três cenários foram executados corretamente e a execução final foi concluída com sucesso.

---

# Comentários Adicionais

Este desafio contribuiu para reforçar conhecimentos em sistemas embarcados, programação em MicroPython e utilização da plataforma Wokwi para simulação de hardware.

Além do desenvolvimento do firmware, também foi possível praticar o uso de Git, GitHub e GitHub Actions para versionamento de código, integração contínua e execução automatizada dos testes.

Durante o desenvolvimento, foram realizados ajustes na leitura do sensor LDR, na detecção de micro-paradas e no tratamento do botão de reset. A execução dos cenários automatizados permitiu verificar o comportamento do sistema e realizar os ajustes necessários.

Ao final, os três cenários de teste disponibilizados para o desafio LIGHT foram executados com sucesso no GitHub Actions.

A solução final foi mantida organizada, legível e compatível com os requisitos apresentados no desafio técnico.