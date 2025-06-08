def contar_prescricoes(texto: str):
        prescricoes = {}
        for char in texto:
            # .get(char, 0) retorna o valor contido na chave "char" se a encontrar
            # no dicionário, caso contrário, retorna o valor definido como padrão
            # nesse caso, 0.
            prescricoes[char] = prescricoes.get(char, 0) + 1
        return prescricoes