# Relatório do Candidato

## Identificação do Candidato

- **Nome completo:** Tâmara de Oliveira Souza
- **GitHub:** https://github.com/tamarasouza-sys

---

# Visão Geral da Solução

Este projeto apresenta a implementação de um sistema embarcado para realizar a contagem de peças em uma esteira utilizando um ESP32, um sensor LDR e um botão de reset.

O funcionamento baseia-se na variação da luminosidade detectada pelo sensor. Sempre que uma peça interrompe a luz e, em seguida, libera novamente o sensor, o sistema registra uma nova peça produzida. Também foi implementada a identificação de micro-paradas quando o sensor permanece bloqueado por um período superior ao tempo estabelecido. O botão permite reiniciar o contador de produção sempre que necessário.

---

# Arquitetura do Sistema Embarcado

O firmware foi desenvolvido em MicroPython e utiliza um laço principal (`while True`) para executar continuamente as tarefas do sistema.

Durante a execução são realizadas as seguintes operações:

- leitura constante do sensor LDR;
- identificação da passagem das peças;
- atualização do contador de produção;
- monitoramento do tempo de bloqueio do sensor para detectar micro-paradas;
- leitura do botão de reset utilizando debounce por software;
- envio das mensagens de status para o monitor serial.

Toda a lógica foi organizada de forma simples para facilitar a manutenção e a compreensão do código.

---

# Componentes Utilizados na Simulação

Os componentes utilizados na simulação foram:

- ESP32 DevKit V4;
- Sensor fotoresistor (LDR);
- Botão de pressão (Push Button);
- Monitor Serial do Wokwi.

Cada componente possui uma função específica: o ESP32 executa o firmware, o LDR identifica a passagem das peças, o botão reinicia o contador e o monitor serial exibe as mensagens geradas pelo sistema.

---

# Decisões Técnicas Relevantes

Para tornar a implementação mais organizada e confiável, foram adotadas algumas estratégias durante o desenvolvimento:

- definição de constantes para os limites de luminosidade e tempo de micro-parada;
- utilização de variáveis para controlar o estado da peça sobre o sensor;
- uso das funções `time.ticks_ms()` e `time.ticks_diff()` para controle do tempo;
- implementação de debounce por software para evitar múltiplos acionamentos do botão;
- estruturação da lógica em um único laço principal, reduzindo a complexidade do programa.

---

# Resultados Obtidos

Ao final do desenvolvimento, o sistema apresentou o comportamento esperado para o cenário LIGHT.

Foram implementadas as seguintes funcionalidades:

- inicialização correta do sistema;
- contagem automática das peças detectadas;
- identificação de micro-paradas após cinco segundos de bloqueio do sensor;
- reinicialização do contador através do botão de reset;
- exibição das mensagens exigidas pelo processo de validação automática.

---

# Comentários Adicionais

Este desafio contribuiu para reforçar conhecimentos em sistemas embarcados, programação em MicroPython e utilização da plataforma Wokwi para simulação de hardware.

Além do desenvolvimento do firmware, também foi possível praticar o uso de Git, GitHub e GitHub Actions, ferramentas importantes para o versionamento de código e integração contínua.

Durante o projeto procurei desenvolver uma solução organizada, legível e compatível com os requisitos apresentados no desafio técnico.
