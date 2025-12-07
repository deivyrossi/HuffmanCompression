# Implementação do Código de Huffman para Compressão de Texto

Este projeto apresenta uma implementação prática do **Algoritmo de Huffman** para compressão de dados sem perdas (lossless). O software foi desenvolvido em **Python** como parte da disciplina de Algoritmos e Estruturas de Dados do CEFET-MG.

O programa processa textos de entrada, constrói a Árvore de Huffman baseada na frequência das palavras e gera um arquivo de saída detalhado. Diferente de compactadores comerciais, salvando o "texto comprimido" como uma sequência visível de caracteres '0' e '1', permitindo fácil inspeção visual da lógica de codificação.

##  Funcionalidades

* **Processamento em Blocos:** Capaz de ler múltiplos textos separados por linhas em branco em um único arquivo de entrada.
* **Algoritmo de Huffman Completo:**
    * Contagem de frequência de palavras.
    * Uso de Fila de Prioridade (Min-Heap).
    * Construção da Árvore Binária.
    * Geração de códigos prefixados via percurso em profundidade (DFS).
* **Saída Legível:** O arquivo final contém o dicionário de códigos (formatado em JSON) e a sequência binária resultante em formato de texto.
* **Preservação de Dados:** O algoritmo diferencia maiúsculas/minúsculas e pontuação, garantindo que o processo seja *lossless* (sem perda de informação).

##  Como Executar

Este projeto não possui dependências externas complexas e utiliza apenas bibliotecas padrão do Python (`heapq`, `json`).

### Pré-requisitos
* Python 3 instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/deivyrossi/HuffmanCompression.git
    cd HuffmanCompression
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

Para facilitar a correção e o entendimento, o arquivo de saída é puramente textual e segue esta estrutura para cada bloco processado:

1.  **Cabeçalho:** `--- BLOCO X ---`
2.  **Mapa de Códigos:** A estrutura da árvore serializada em formato JSON (indentado para leitura humana), mostrando qual código binário pertence a qual palavra.
3.  **Texto Comprimido:** A representação do texto original convertida para uma longa string de 0s e 1s.

*Exemplo:*
```text
--- BLOCO 1 ---
MAPA DE CÓDIGOS:
{
    "computador": "1011",
    "dados": "1100",
    "instruções": "000"
}

TEXTO COMPRIMIDO (REPRESENTAÇÃO BINÁRIA):
101111000000...
```


## Detalhes de Implementação

**O algoritmo segue estas etapas lógicas:**

1. Contagem de Frequência: O texto é dividido em palavras e suas ocorrências são contadas.

2. Fila de Prioridade (Min-Heap): As palavras são inseridas em uma heap baseada na frequência.

3. Construção da Árvore: Os dois nós com menor frequência são removidos e unidos em um novo nó pai repetidamente.

4. Geração de Códigos (DFS): Um percurso em profundidade percorre a árvore (Esquerda=0, Direita=1) para atribuir códigos únicos às folhas (palavras).

5. Codificação: O texto original é relido e cada palavra é substituída pelo seu código binário correspondente, gerando uma string contínua de zeros e uns.


## Autor
- Deivy Rossi Teixeira de Melo ([deivyrossi](https://github.com/deivyrossi)) - Engenharia da computação
