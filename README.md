# Implementação do Código de Huffman para Compressão de Texto

Este projeto apresenta uma implementação prática do **Algoritmo de Huffman** para compressão de dados sem perdas (lossless). O software foi desenvolvido em **Python** como parte da disciplina de Algoritmos e Estruturas de Dados do CEFET-MG.

O programa lê textos de entrada, calcula a frequência das palavras, constrói a árvore de Huffman, gera os códigos binários e produz um arquivo de saída contendo os dados comprimidos (em bytes reais) juntamente com os metadados necessários para a descompressão.

##  Funcionalidades

* **Leitura de Blocos:** Processa múltiplos textos separados por linhas em branco em um único arquivo de entrada.
* **Compressão Real:** Converte as strings de "0s" e "1s" em *bytes* reais para economizar espaço em disco.
* **Tratamento de Padding:** Calcula e armazena os bits de preenchimento (padding) para garantir a integridade dos dados binários.
* **Persistência de Metadados:** Salva a tabela de códigos (em formato JSON) e a informação de padding no cabeçalho do arquivo de saída.

##  Como Executar

Este projeto não possui dependências externas complexas e utiliza apenas bibliotecas padrão do Python (`heapq`, `json`).

### Pré-requisitos
* Python 3 instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/deivyrossi/HuffmanCompression
    ```

2.  **Verifique o arquivo de entrada:**
    Certifique-se de que o arquivo `input.dat` esteja na pasta `data/`. Você pode editar este arquivo para adicionar seus próprios textos de teste.
    * *Nota: Separe os diferentes textos com uma linha em branco.*

3.  **Execute o programa:**
    A partir da raiz do projeto, execute o script principal:
    ```bash
    python3 src/main.py
    ```

4.  **Verifique o resultado:**
    O arquivo comprimido será gerado em `data/output.dat`.

##  Estrutura do Projeto

A organização de pastas segue o padrão solicitado na especificação do trabalho:

```text
.
├── data/
│   ├── input.dat       # Arquivo de texto original (entrada)
│   └── output.dat      # Arquivo comprimido gerado (saída)
├── src/
│   └── main.py         # Código-fonte principal
└── README.md           # Documentação do projeto
```


## Formato do Arquivo de Saída (`output.dat`)

O arquivo gerado é um híbrido de texto e dados binários. Para cada bloco de texto processado, o formato segue a seguinte estrutura:

1.  **Cabeçalho de Identificação:** `--- BLOCO X ---`
2.  **Metadado de Padding:** `PADDING:N` (Onde N é o número de bits de preenchimento adicionados ao final).
3.  **Mapa de Códigos (Árvore):** Uma linha contendo a estrutura da árvore/dicionário serializada em JSON. Ex: `{"palavra": "001", ...}`.
4.  **Dados Comprimidos:** O conteúdo binário (bytes reais) correspondente ao texto comprimido.

*Exemplo visual de um bloco no output:*
```text
--- BLOCO 1 ---
PADDING:4
{"computador": "1011", "dados": "1100", ...}
[BYTES BINÁRIOS ILEGÍVEIS AQUI]
```


## Detalhes de Implementação

**O algoritmo segue estas etapas lógicas:**

1. Contagem de Frequência: O texto é dividido em palavras e suas ocorrências são contadas.

2. Fila de Prioridade (Min-Heap): As palavras são inseridas em uma heap baseada na frequência.

3. Construção da Árvore: Os dois nós com menor frequência são removidos e unidos em um novo nó pai repetidamente.

4. Geração de Códigos (DFS): Um percurso em profundidade percorre a árvore (Esquerda=0, Direita=1) para atribuir códigos únicos às folhas (palavras).

5. Conversão Binária: O texto é traduzido para uma sequência de bits.

6. Bit Packing: A sequência de bits é fatiada em grupos de 8, convertida em inteiros e escrita como bytes no arquivo final.


## Autor
- Deivy Rossi Teixeira de Melo ([deivyrossi](https://github.com/deivyrossi)) - Engenharia da computação
