from verifica_prescricao import verifica_prescricao

if __name__ == "__main__":
    print(verifica_prescricao('a', 'b'))
    print(verifica_prescricao('aa', 'b'))
    print(verifica_prescricao('aa', 'aab')) 
    print(verifica_prescricao('aba', 'cbaa'))