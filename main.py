import cargas as c

# Dados
# w = 5.4 * 9.81  # input('> Peso da aeronave (N): ')
# s = 0.3339  # input('> Area alar(m**2): ')
# clmax = 2.1 # input('> Maximo coeficiente de sustentacao: ')
# vh = 19.45  # input('> Velocidade maxima nivelada(m/s): ')
# c = 0.21  # Corda media aerodinamica
# a = 3.3513  # Angulo de inclinacao medio da curva cl x alfa(radianos)mtow = [5.4 * 9.81,0.3339, 2.1, 19.45, 0.21, 3.513]
mpec = [1.75 * 9.81,0.3339, 2.1, 19.86, 0.21, 3.513]
mtow = [5.4 * 9.81,0.3339, 2.1, 19.86, 0.21, 3.513]
matriz = c.vn(mtow)
print('SUSTENTAÇÕES DA EH')
for cdv in matriz:
	print('\nCONDIÇÃO: '+ str(cdv))
	print('%6.2f N' % c.lt(cdv, 0.0168, 0.7, -0.25))
	
c.tdp(0.032, 0.174, 88.94, 2.67, 0.075, 0.10)
c.boom(0.7, 17, -7, -2, 0.1, 0.04)
