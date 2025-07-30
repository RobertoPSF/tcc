stateDiagram-v2
    [*] --> IniciarAtividade
    IniciarAtividade --> ColetandoDados
    ColetandoDados --> JsonGerado
    JsonGerado --> AnalisandoDados
    AnalisandoDados --> RelatorioGerado
    RelatorioGerado --> [*]
