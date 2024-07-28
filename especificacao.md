**Resumo da Especificação do Trabalho**

**Objetivo:**
Implementar um simulador de memória cache utilizando o protocolo MESI (Modify, Exclusive, Shared, Invalid) em uma aplicação real.

**Descrição:**
- Simular pelo menos três processadores, cada um com memória cache dedicada e memória RAM compartilhada.
- O programa deve ter dois espaços de endereçamento: memória principal (50 posições) e memória cache (5 posições por processador).
- Solicitações de acesso à memória podem ser feitas por qualquer processador, podendo ser leitura ou escrita.
- A memória cache deve utilizar o algoritmo FIFO para substituição e a política de escrita write-back.
- Implementar o protocolo MESI para gerenciar o estado das linhas de cache.

**Transações Definidas:**
- RH (Read Hit): Leitura com acerto, mantém o estado da linha.
- RM (Read Miss): Leitura com falha, pode marcar a linha como compartilhada ou exclusiva.
- WM (Write Miss): Escrita com falha, marca a linha como modificada e invalida nas outras caches.
- WH (Write Hit): Escrita com acerto, modifica o estado da linha conforme necessário.

**Aplicação:**
- Inserir o simulador em uma aplicação real, como um jogo ou sistema de reserva.
- O usuário deve poder selecionar um processador e realizar operações de leitura ou escrita, visualizando as informações do protocolo MESI.

**Requisitos de Entrega:**
- Três arquivos: relatório técnico, arquivos fonte, e executável.
- Relatório técnico deve incluir introdução, objetivos, funcionamento da memória cache e protocolo MESI, funcionamento da aplicação, decisões de projeto, conclusão e referências.
- Código fonte deve estar comentado e bem estruturado.

**Avaliação:**
- Código fonte: até 6 pontos.
- Relatório: até 2 pontos.
- Apresentação: até 2 pontos.
- Trabalhos copiados ou que não atendam às especificações serão zerados.

**Data de Entrega:**
- Envio via formulário online até 22/08/2024.
- Apresentação prevista para 29/08/2024.

**Referências Bibliográficas:**
- Vários livros e materiais relacionados à arquitetura e organização de computadores.