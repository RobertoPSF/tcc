# Análise de Comportamento de Digitação

Este projeto é uma ferramenta para analisar padrões de digitação e comportamento do usuário em um computador. Ele processa registros de atividades e gera relatórios detalhados que podem ajudar a identificar comportamentos suspeitos ou incomuns.

## O que o projeto faz?

O projeto consiste em dois componentes principais:

1. **Coletor de Dados**: Um programa que registra as atividades do usuário, como:
   - Teclas pressionadas
   - Tempo entre pressionamentos
   - Aplicativos utilizados
   - Comandos executados

2. **Analisador de Dados**: Um programa que processa esses registros e gera relatórios que incluem:
   - Padrões de digitação
   - Análise de comandos suspeitos
   - Métricas por aplicativo
   - Gráficos de comportamento

## Como usar?

### Requisitos
- Python 3.6 ou superior
- Bibliotecas Python necessárias (instaladas automaticamente)

### Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando o Coletor de Dados

Para começar a coletar dados:
```bash
python keylogger.py
```

O programa irá:
- Iniciar a coleta de dados
- Salvar os registros em arquivos JSON
- Mostrar um resumo das atividades coletadas

### Analisando os Dados

Para analisar os dados coletados, você tem duas opções:

1. Analisar um arquivo específico:
```bash
python analyzer.py caminho/para/arquivo.json
```

2. Analisar todos os arquivos em um diretório:
```bash
python analyzer.py caminho/para/diretorio/
```

O programa irá:
- Processar os dados coletados
- Gerar relatórios em PDF
- Mostrar um resumo da análise
- Salvar os relatórios na pasta `output/`

## Estrutura dos Relatórios

Os relatórios gerados incluem:

1. **Métricas de Digitação**
   - Tempo médio de pressionamento das teclas
   - Padrões de digitação
   - Gráficos de distribuição

2. **Análise de Comandos Suspeitos**
   - Frequência de comandos como copiar/colar
   - Alertas para comportamentos incomuns

3. **Métricas por Aplicativo**
   - Tempo gasto em cada aplicativo
   - Taxa de digitação por aplicativo
   - Padrões de uso

## Observações Importantes

- Os relatórios são gerados em PDF na pasta `output/`
- Cada arquivo de entrada gera um relatório separado
- O programa identifica automaticamente comportamentos suspeitos
- Os dados são processados localmente, garantindo privacidade

## Suporte

Se encontrar algum problema ou tiver dúvidas, por favor abra uma issue no repositório.
