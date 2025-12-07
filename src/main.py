import heapq  
import json   


# ETAPA 1: LEITURA DO ARQUIVO

def ler_blocosdetexto(filepath="data/input.dat"):
    """
    Lê o arquivo de entrada e separa os textos baseados em linhas em branco.
    Retorna uma lista onde cada item é um bloco de texto completo.
    """
    textos = []
    bloco_atual = ""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for linha in f:
                # Se a linha for vazia (só enter/espaço), significa que um bloco acabou
                if not linha.strip():
                    if bloco_atual.strip():
                        textos.append(bloco_atual.strip())
                    bloco_atual = "" # Reinicia para o próximo bloco
                else:
                    # Se tiver texto, acumula na variável do bloco atual
                    bloco_atual += linha
                    
        # Adiciona o último bloco se o arquivo não terminar com linha em branco
        if bloco_atual.strip():
            textos.append(bloco_atual.strip())
            
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{filepath}' não foi encontrado.")
        
    return textos



# ETAPA 2: CONTAGEM DE FREQUÊNCIA

def contador_palavras(texto_bloco):
    """
    Conta quantas vezes cada palavra aparece.
    Isso é crucial porque Huffman dá códigos menores para palavras mais frequentes.
    """
    # Divide o texto em uma lista de palavras usando o espaço como separador
    palavras_sujas = texto_bloco.split(" ")
    frequencias = {}

    for palavra_original in palavras_sujas:
        # Pula strings vazias (causadas por múltiplos espaços no texto original)
        if not palavra_original:
            continue
            
        # Se a palavra já está no dicionário, soma +1
        if palavra_original in frequencias:
            frequencias[palavra_original] += 1
        # Se é a primeira vez que a vemos, começa com 1
        else:
            frequencias[palavra_original] = 1
            
    return frequencias # Retorna: {'casa': 2, 'azul': 1, ...}



# ETAPA 3: CONSTRUÇÃO DA ÁRVORE DE HUFFMAN

def construir_arvore(frequencias):
    """
    Constrói a árvore combinando os nós de menor frequência até sobrar apenas um (a raiz).
    """
    lista_para_fila = []
    
    # 1. Prepara os dados para a fila.
    # O formato TEM que ser (Frequencia, Conteudo) para o heapq ordenar corretamente.
    for palavra, freq in frequencias.items():
        lista_para_fila.append((freq, palavra))

    # 2. Transforma a lista comum em uma Fila de Prioridade (Min-Heap).
    # O Python organiza a lista de modo que o item de menor frequência fique no índice 0.
    heapq.heapify(lista_para_fila)
    fila = lista_para_fila

    # 3. Loop principal do Huffman
    # Enquanto houver mais de 1 item na fila, precisamos continuar agrupando.
    while len(fila) > 1:
        
        # Remove os dois nós com as MENORES frequências
        item_1 = heapq.heappop(fila) # Filho Esquerdo
        item_2 = heapq.heappop(fila) # Filho Direito

        # Soma as frequências deles para criar o nó Pai
        frequencia_pai = item_1[0] + item_2[0]
        
        # Cria a lista de filhos. Isso cria a estrutura da árvore.
        # Nó Pai = (Soma, [Filho1, Filho2])
        filhos = [item_1, item_2]
        novo_nodo = (frequencia_pai, filhos)

        # Coloca o novo nó Pai de volta na fila para ser processado depois
        heapq.heappush(fila, novo_nodo)

    # Quando o loop acaba, sobrou apenas 1 item na fila: a Árvore Completa.
    return fila[0] 



# ETAPA 4: GERAÇÃO DOS CÓDIGOS BINÁRIOS (DFS)

def gerar_codigos_recursivo(nodo, mapa_de_codigos, codigo_atual=""):
    """
    Percorre a árvore criada na etapa anterior para descobrir o código de cada palavra.
    Se for para a esquerda -> adiciona "0".
    Se for para a direita -> adiciona "1".
    """
    # O 'nodo' é uma tupla (Frequencia, Conteudo)
    item = nodo[1]

    # Verifica se 'item' é uma lista. Se for, é um NÓ PAI (tem filhos).
    if isinstance(item, list):
        filho_esquerdo = item[0]
        filho_direito = item[1]

        # Chamada Recursiva: mergulha na árvore
        # Caminho da esquerda ganha "0"
        gerar_codigos_recursivo(filho_esquerdo, mapa_de_codigos, codigo_atual + "0")
        # Caminho da direita ganha "1"
        gerar_codigos_recursivo(filho_direito, mapa_de_codigos, codigo_atual + "1")
        
    else:
        # Se não é lista, é um NÓ FOLHA (uma palavra real).
        # Chegamos ao fim do caminho!
        # Salvamos o código que construímos até aqui no dicionário.
        palavra = item
        mapa_de_codigos[palavra] = codigo_atual



# ETAPA 5: COMPRESSÃO SIMPLES

def compressao_simples(texto_bloco, mapa_de_codigos):
    """
    Lê o texto original palavra por palavra e substitui pelo código correspondente.
    Gera uma string gigante de zeros e uns (ex: "01001110...").
    """
    binario_gigante = ""
    palavras = texto_bloco.split(" ")
    
    for palavra in palavras:
        # Só substitui se a palavra estiver no mapa (ignora espaços vazios extras)
        if palavra in mapa_de_codigos:
            codigo = mapa_de_codigos[palavra]
            binario_gigante += codigo
            
    return binario_gigante



# FUNÇÃO PRINCIPAL (MAIN)

def main():
    print(">>> Iniciando Compressor de Huffman<<<\n")
    
    # 1. Lê o arquivo de entrada
    blocos = ler_blocosdetexto("data/input.dat")
    print(f"Foram encontrados {len(blocos)} blocos de texto para processar.")
    
    # Limpa/Cria o arquivo de saída antes de começar
    with open("data/output.dat", 'w', encoding='utf-8') as f:
        f.write("")

    # Processa cada bloco individualmente
    for i, bloco in enumerate(blocos):
        print(f"\n--- Processando Bloco {i+1} ---")
        
        # A. Conta as palavras
        freqs = contador_palavras(bloco)
        print(f"   > Palavras únicas encontradas: {len(freqs)}")
        
        # B. Cria a árvore
        arvore = construir_arvore(freqs)
        
        # C. Gera o mapa de códigos (Dicionário)
        mapa_codigos = {}
        gerar_codigos_recursivo(arvore, mapa_codigos)
        
        # D. Comprime (Gera a string de 0s e 1s)
        texto_comprimido = compressao_simples(bloco, mapa_codigos)
        print(f"   > Tamanho da string binária gerada: {len(texto_comprimido)} caracteres")
        
        # E. Salva no arquivo output.dat
        with open("data/output.dat", 'a', encoding='utf-8') as f:
            f.write(f"--- BLOCO {i+1} ---\n")
            
            # Salva o Mapa de Códigos (identado para ficar bonito)
            f.write("MAPA DE CÓDIGOS:\n")
            f.write(json.dumps(mapa_codigos, indent=4, ensure_ascii=False))
            
            # Salva o texto comprimido (a sequência de 0 e 1)
            f.write("\n\nTEXTO COMPRIMIDO (REPRESENTAÇÃO BINÁRIA):\n")
            f.write(texto_comprimido)
            
            # Pula linhas para o próximo bloco
            f.write("\n\n" + "="*30 + "\n\n")
            
    print("\n>>> Processo concluído! Verifique o arquivo 'data/output.dat'. <<<")

if __name__ == "__main__":
    main()