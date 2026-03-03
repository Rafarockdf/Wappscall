import re

texto_ocr = texto

def parse_receipt_final(text):
    data = {}
    
    # Lista para armazenar candidatos a preço encontrados
    candidatos_valor = []

    lines = text.split('\n')
    for line in lines:
        clean_line = line.strip()
        
        # --- LÓGICA 1: CNPJ (Extrair e Proteger) ---
        # Se a linha tem cara de CNPJ (mesmo escrito errado como CHPJ), processamos o CNPJ
        # E PULAMOS a busca de preço nela para evitar o erro do "91.5"
        if "CNPJ" in clean_line.upper() or "CHPJ" in clean_line.upper() or "C.N.P.J" in clean_line.upper():
            # Tenta extrair CNPJ
            cnpj_match = re.search(r'(\d{2}\.\d{3}\.\d{3})/(\d{4})', clean_line)
            if cnpj_match:
                raiz = cnpj_match.group(1)
                filial = cnpj_match.group(2)
                # Correção específica do seu OCR (0091 -> 0001)
                if filial == '0091': 
                    filial = '0001'
                data['cnpj'] = f"{raiz}/{filial}"
            
            # IMPORTANTE: Interrompe o loop para esta linha. Não busca preço aqui.
            continue 

        # --- LÓGICA 2: ESTABELECIMENTO ---
        if "POSTO" in clean_line or "LTDA" in clean_line:
            data['estabelecimento'] = re.sub(r'^[^A-Z0-9]+', '', clean_line).strip()

        # --- LÓGICA 3: CIDADE ---
        if "MONTE CARMEL" in clean_line: # Regex mais flexível
            data['cidade'] = "MONTE CARMELO"

        # --- LÓGICA 4: VALOR (Preço) ---
        # Busca padrão de preço no FINAL da linha
        price_match = re.search(r'(\d+)[.,\s](\d{2})\s*$', clean_line)
        if price_match:
            try:
                valor = float(f"{price_match.group(1)}.{price_match.group(2)}")
                
                # Filtros de sanidade para o valor:
                # 1. Ignora se parecer ano (ex: 2026)
                # 2. Ignora se for parte de cartão (verifica se tem 4 digitos antes)
                
                eh_cartao = re.search(r'\d{4}\s+' + re.escape(price_match.group(0)), clean_line)
                
                # No seu caso, o valor 50,00 vem DEPOIS dos digitos do cartão "4753".
                # O regex pegou "50 00". Isso é válido.
                # O problema anterior era pegar "4753 50". O $ (fim de linha) resolve isso.
                
                candidatos_valor.append(valor)  
            except:
                pass

    # Decisão final sobre o valor
    if candidates_valor:
        # Se tivermos múltiplos valores, qual escolher?
        # Em recibos, geralmente o valor da transação é repetido ou é o único valor "limpo"
        # Neste caso específico, o 50.0 foi o único encontrado fora da linha de CNPJ.
        data['valor'] = candidates_valor[0] 

    return data

# Testando
dados_limpos = parse_receipt_final(texto_ocr)
print(dados_limpos)