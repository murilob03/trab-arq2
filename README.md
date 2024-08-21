# Simulador de Banco de Sangue com Protocolo MESI

## Visão Geral

Este projeto é uma simulação de um sistema de banco de sangue utilizando o protocolo de coerência de cache MESI (Modified, Exclusive, Shared, Invalid). O protocolo MESI é normalmente usado em arquitetura de computadores para gerenciar a memória cache, mas aqui foi adaptado para gerenciar bolsas de sangue em caches de diferentes hospitais, garantindo a consistência e sincronização das informações do estoque de sangue.

## Funcionalidades

- **Usar Sangue**: Permite que um hospital utilize sangue de uma bolsa especificada, alterando seu status para "E" (Vazia) após o uso.
- **Solicitar Sangue**: Permite que um hospital consulte o tipo de sangue disponível em uma bolsa específica.
- **Doar Sangue**: Facilita a doação de sangue por um hospital, armazenando-o em uma bolsa vazia no banco de sangue.

## Executando a Simulação

- Para executar a simulação, execute o seguinte comando:
    ```bash
    python main.py
    ```

## Uso

### Usar Sangue

Permite que um hospital use sangue de uma bolsa específica se ele corresponder ao tipo necessário.

- Selecione o Hospital que deseja usar para realizar a ação

- Selecione a linha do banco com o sangue que deseja utilizar (memória principal)

- Clique em `Use Blood`

### Solicitar Sangue

Permite que um hospital verifique o tipo de sangue em uma bolsa específica. Pois ele pode ter sido
utilizado em algum outro hospital e essa informação ainda não foi sincronizada.

- Selecione o Hospital que deseja usar para realizar a ação

- Selecione a linha do banco (memória principal) com o sangue que deseja verificar 

- Clique em `Request Blood`

### Doar Sangue

Permite que um hospital doe sangue para uma bolsa vazia no banco de sangue.

- Selecione o Hospital que deseja usar para realizar a ação

- Selecione o tipo de sangue que deseja doar no menu `Type`

- Clique em `Donate Blood`

## Estrutura do Projeto

```plaintext
blood-bank-mesi-simulator/
│
├── src/
│   ├── mesi_simulator.py      # Junta os componentes em um objeto do tipo SimuladorMESI
│   ├── enums.py               # Define os enums usados para o simulador
│   ├── blood_bank/        
│   │    ├── BloodBank.py      # Classe BloodBank implementando a lógica de negócio
│   │    └── BloodBankGUI.py   # Classe que implementa a interface gráfica
│   └── components/
│       ├── bus.py
│       ├── cache.py
│       └── main_memory.py
├── main.py                # Ponto de entrada para executar a simulação
└── README.md              # Documentação do projeto
```

## Membros

Este trabalho foi desenvolvido pelos alunos de graduação: 
 - Murilo Boccardo: RA 124160
 - Reidner Adnan Maniezo de Melo: RA 110582
