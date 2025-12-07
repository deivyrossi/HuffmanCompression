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
                # Se a linha for vazia (só enter/espaço), o bloco acabou
                if not linha.strip():
                    if bloco_atual.strip():
                        textos.append(bloco_atual.strip())
                    bloco_atual = "" # Reseta para começar o próximo
                else:
                    # Se tem texto, acumula na variável
                    bloco_atual += linha
                    
        # Não esquece de adicionar o último bloco se o arquivo acabar sem linha vazia
        if bloco_atual.strip():
            textos.append(bloco_atual.strip())
            
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{filepath}' não existe.")
        return []
        
    return textos



# ETAPA 2: CONTAGEM DE FREQUÊNCIA

def contador_palavras(texto_bloco):
    """
    Conta quantas vezes cada palavra aparece.
    Huffman precisa disso para dar códigos curtos às palavras frequentes.
    """
    palavras_sujas = texto_bloco.split(" ")
    frequencias = {}

    for palavra in palavras_sujas:
        # Ignora espaços vazios que aparecem se tiver dois espaços seguidos
        if not palavra:
            continue
            
        if palavra in frequencias:
            frequencias[palavra] += 1
        else:
            frequencias[palavra] = 1
            
    return frequencias



# ETAPA 3: CONSTRUÇÃO DA ÁRVORE

def construir_arvore(frequencias):
    """
    Cria a Árvore de Huffman usando uma Fila de Prioridade (Heap).
    """
    lista_para_fila = []
    
  
    # O Python dá erro se tentar comparar um Nó (Lista) com uma Palavra (String)
    # quando as frequências são iguais.
    # Solução: Um número sequencial (contador) na tupla.
    # Se as frequências forem iguais, ele desempata pelo número
    contador_desempate = 0 
    
    # Formato da Tupla: (Frequencia, ID_UNICO, Conteudo)
    for palavra, freq in frequencias.items():
        lista_para_fila.append((freq, contador_desempate, palavra))
        contador_desempate += 1

    # Transforma a lista em uma Heap (ordena pelo primeiro item: Frequência)
    heapq.heapify(lista_para_fila)
    fila = lista_para_fila

    # Loop Principal: Enquanto tiver mais de 1 item, agrupa eles.
    while len(fila) > 1:
        
        # Remove os dois nós com as MENORES frequências
        # Como usamos heap, eles sempre saem ordenados.
        item_1 = heapq.heappop(fila) # Filho Esquerdo
        item_2 = heapq.heappop(fila) # Filho Direito

        # Cria o Pai somando as frequências
        frequencia_pai = item_1[0] + item_2[0]
        
        # O conteúdo do pai é uma lista com os dois filhos
        filhos = [item_1, item_2]
        
        # Cria a tupla do pai (com um novo ID de desempate)
        novo_nodo = (frequencia_pai, contador_desempate, filhos)
        contador_desempate += 1

        # Devolve o pai para a fila
        heapq.heappush(fila, novo_nodo)

    # Retorna a raiz da árvore (o único item que sobrou)
    return fila[0] 


# ETAPA 4: GERAÇÃO DOS CÓDIGOS (RECURSÃO)

def gerar_codigos_recursivo(nodo, mapa_de_codigos, codigo_atual=""):
    """
    Percorre a árvore (DFS) para descobrir o binário de cada palavra.
    Esquerda = 0, Direita = 1.
    """
    
    # ATENÇÃO: Agora o conteúdo está no índice [2] por causa do contador de desempate
    # Tupla: (freq, id, CONTEUDO)
    conteudo = nodo[2]

    # Se o conteúdo for uma LISTA, significa que é um nó de bifurcação (Pai)
    if isinstance(conteudo, list):
        filho_esquerdo = conteudo[0]
        filho_direito = conteudo[1]

        # Mergulha na esquerda (adiciona 0)
        gerar_codigos_recursivo(filho_esquerdo, mapa_de_codigos, codigo_atual + "0")
        # Mergulha na direita (adiciona 1)
        gerar_codigos_recursivo(filho_direito, mapa_de_codigos, codigo_atual + "1")
        
    else:
        # Se NÃO for lista, é uma String (Palavra/Folha). Chegamos no fim.
        palavra = conteudo
        mapa_de_codigos[palavra] = codigo_atual



# ETAPA 5: COMPRESSÃO VISUAL

def compressao_simples(texto_bloco, mapa_de_codigos):
    """
    Substitui cada palavra pelo seu código binário.
    """
    binario_gigante = ""
    palavras = texto_bloco.split(" ")
    
    for palavra in palavras:
        if palavra in mapa_de_codigos:
            codigo = mapa_de_codigos[palavra]
            binario_gigante += codigo
            
    return binario_gigante



# FUNÇÃO PRINCIPAL (MAIN)

def main():
    print(">>> Iniciando Compressor de Huffman<<<\n")
    
    blocos = ler_blocosdetexto("data/input.dat")
    print(f"Foram encontrados {len(blocos)} blocos de texto.\n")
    
    # Limpa o arquivo de saída
    with open("data/output.dat", 'w', encoding='utf-8') as f:
        f.write("")

    for i, bloco in enumerate(blocos):
        print(f"--- Processando Bloco {i+1} ---")
        
        # 1. Contar
        freqs = contador_palavras(bloco)
        print(f"   > Palavras únicas: {len(freqs)}")
        
        if len(freqs) == 0:
            print("   > Bloco vazio. Pulando...")
            continue
            
        # 2. Construir Árvore
        arvore = construir_arvore(freqs)
        
        # 3. Gerar Códigos
        mapa_codigos = {}
        
        # Caso especial: Se o texto só tem 1 palavra repetida ("banana banana")
        # a árvore não tem bifurcações. Atribuímos "0" direto.
        conteudo_raiz = arvore[2]
        if isinstance(conteudo_raiz, str):
            mapa_codigos[conteudo_raiz] = "0"
        else:
            gerar_codigos_recursivo(arvore, mapa_codigos)
        
        # 4. Comprimir
        texto_comprimido = compressao_simples(bloco, mapa_codigos)
        print(f"   > Tamanho do binário gerado: {len(texto_comprimido)} bits")
        
        # 5. Salvar
        with open("data/output.dat", 'a', encoding='utf-8') as f:
            f.write(f"--- BLOCO {i+1} ---\n")
            f.write("MAPA DE CÓDIGOS:\n")
            # json.dumps
            f.write(json.dumps(mapa_codigos, indent=4, ensure_ascii=False))
            f.write("\n\nTEXTO COMPRIMIDO (REPRESENTAÇÃO BINÁRIA):\n")
            f.write(texto_comprimido)
            f.write("\n\n" + "="*40 + "\n\n")
            
    print("\n>>> Sucesso! Verifique o arquivo 'data/output.dat'. <<<")

if __name__ == "__main__":
    main()
