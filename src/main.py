import heapq
import json 

# --- ETAPA 1: LEITURA DO ARQUIVO ---
def ler_blocosdetexto(filepath="data/input.dat"):
    textos = []
    bloco_atual = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for linha in f:
                if not linha.strip():
                    if bloco_atual.strip():
                        textos.append(bloco_atual.strip())
                    bloco_atual = ""
                else:
                    bloco_atual += linha
        if bloco_atual.strip():
            textos.append(bloco_atual.strip())
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {filepath}")
    return textos

# --- ETAPA 2: CONTAGEM DE FREQUÊNCIA ---
def contador_palavras(bloco_de_texto):
    palavras_sujas = bloco_de_texto.split(" ")
    frequencias = {}
    for palavra_original in palavras_sujas:
        if not palavra_original:
            continue
        if palavra_original in frequencias:
            frequencias[palavra_original] += 1
        else:
            frequencias[palavra_original] = 1
    return frequencias

# --- ETAPA 3: CONSTRUÇÃO DA ÁRVORE ---
def construir_arvore(frequencias):
    
    # 3a. Inverter (Frequencia, Palavra)
    lista_para_fila = []
    for palavra, freq in frequencias.items():
        lista_para_fila.append( (freq, palavra) )
        
    # 3b. Converter em Fila de Prioridade (Heap)
    heapq.heapify(lista_para_fila)
    
    # 3c. Algoritmo de Huffman
    fila = lista_para_fila
    while len(fila) > 1:
        item_1 = heapq.heappop(fila)
        item_2 = heapq.heappop(fila)
        frequencia_pai = item_1[0] + item_2[0]
        novo_nodo = (frequencia_pai, [item_1, item_2])
        heapq.heappush(fila, novo_nodo) 

    return fila[0] # Retorna a árvore completa

# --- ETAPA 4: GERAÇÃO DOS CÓDIGOS ---
def gerar_codigos_recursivo(nodo, mapa_de_codigos, codigo_atual=""):
    item = nodo[1]
    if isinstance(item, list): # É um nó-pai
        filho_esquerdo = item[0]
        filho_direito = item[1]
        gerar_codigos_recursivo(filho_esquerdo, mapa_de_codigos, codigo_atual + "0")
        gerar_codigos_recursivo(filho_direito, mapa_de_codigos, codigo_atual + "1")
    else: # É um nó-folha (palavra)
        palavra = item
        mapa_de_codigos[palavra] = codigo_atual

# --- ETAPA 5 & 6: COMPRESSÃO E PADDING ---
def comprimir_e_gerar_bytes(bloco_de_texto, mapa_de_codigos):
    
    # 5. Criar "binário gigante"
    codigao = ""
    palavras = bloco_de_texto.split(" ")
    for palavra in palavras:
        if palavra in mapa_de_codigos:
            codigao += mapa_de_codigos[palavra]
            
    # 6. Aplicar padding
    padding_amount = 0
    tamanho_total = len(codigao)
    remainder = tamanho_total % 8

    if remainder != 0:
        padding_amount = 8 - remainder
    
    codigao_com_padding = codigao + ("0" * padding_amount)
    
    # 7. Converter para bytes reais
    byte_array_final = bytearray()
    for i in range(0, len(codigao_com_padding), 8):
        fatia = codigao_com_padding[i : i+8]
        valor_em_byte = int(fatia, 2)
        byte_array_final.append(valor_em_byte)
        
    return byte_array_final, padding_amount


def main():
    
    print("Iniciando compressão...")
    
    # ETAPA 1: Ler todos os blocos do input
    blocos_de_texto = ler_blocosdetexto("data/input.dat")
    
    # Limpa o arquivo de saída 
    with open("data/output.dat", 'w', encoding='utf-8') as f:
        f.write("") # Arquivo limpo
        
    print(f"Encontrados {len(blocos_de_texto)} blocos de texto para comprimir.")
    
    # Processa um bloco de cada vez
    for i, bloco in enumerate(blocos_de_texto):
        print(f"\n--- Processando Bloco {i+1} ---")
        
        # ETAPA 2: Contar frequências
        mapa_frequencias = contador_palavras(bloco)
        
        # ETAPA 3: Construir a árvore
        arvore = construir_arvore(mapa_frequencias)
        
        # ETAPA 4: Gerar os códigos
        mapa_de_codigos_bloco = {} # Mapa vazio para este bloco
        gerar_codigos_recursivo(arvore, mapa_de_codigos_bloco)
        
        # ETAPA 5 & 6: Comprimir e converter para bytes
        dados_comprimidos, padding = comprimir_e_gerar_bytes(bloco, mapa_de_codigos_bloco)
        
        # ETAPA 7: Salvar no output.dat
        
        # Salva o padding e o mapa (como texto)
        with open("data/output.dat", 'a', encoding='utf-8') as f:
            f.write(f"--- BLOCO {i+1} ---\n")
            f.write(f"PADDING:{padding}\n")
            # Salva o mapa de códigos como uma string JSON
            f.write(json.dumps(mapa_de_codigos_bloco) + "\n")
            
        # Salva os dados binários
        with open("data/output.dat", 'ab') as f:
            f.write(dados_comprimidos)
            # Adiciona uma quebra de linha binária para separar
            f.write(b"\n") 
            
        print(f"Bloco {i+1} comprimido e salvo.")

# --- Executa o programa 
if __name__ == "__main__":
    main()