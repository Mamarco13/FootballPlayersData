def convertir_valor_mercado(valor_texto):
    if valor_texto is None or valor_texto == 'No disponible':
        return 0  # Si el valor no está disponible, devolver 0
    valor_texto = valor_texto.strip().replace('€', '').replace(' ', '')

    if 'm' in valor_texto.lower():  # Para millones
        return float(valor_texto.lower().replace('m', '')) * 1_000_000
    elif 'k' in valor_texto.lower():  # Para miles
        return float(valor_texto.lower().replace('k', '')) * 1_000
    else:
        return float(valor_texto)  # Para valores numéricos directos
