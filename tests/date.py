# Recebe a idade em dias
dias_total = int(input("Digite a idade em dias: "))

# Cálculo dos anos, meses e dias
anos = dias_total // 365
dias_restantes = dias_total % 365

meses = dias_restantes // 30
dias = dias_restantes % 30

# Exibe o resultado
print(f"{anos} ano(s)")
print(f"{meses} mes(es)")
print(f"{dias} dia(s)")
