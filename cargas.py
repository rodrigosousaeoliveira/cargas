# Finalidade: gerar diagrama VN da aeronave
# Entradas: nmax = FATOR DE CARGA MAXIMO, nmin = FATOR DE CARGA MINIMO
# w = PESO DA AERONAVE, s = AREA ALAR,
#clmax = MAXIMO COEFICIENTE DE SUSTENTACAO DO PERFIL
# vd = VELOCIDADE DE MERGULHO

import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

def vn(entradas):
	# Coleta de dados de entradas
	# print('Entre com os dados solicitados e pressione enter:')
	nmax = 2  # input("> Fator de carga maximo permitido (g's): ")
	nmin = -1  # input("> Fator de carga negativo maximo permitido (g's): ")
	w = entradas[0]  # input('> Peso da aeronave (N): ')
	s = entradas[1]   # input('> Area alar(m**2): ')
	clmax = entradas[2]  # input('> Maximo coeficiente de sustentacao: ')
	vh = entradas[3]  # input('> Velocidade maxima nivelada(m/s): ')
	c = entradas[4]  # Corda media aerodinamica
	a = entradas[5]   # Angulo de inclinacao medio da curva cl x alfa(radianos)
	
	
	# Variaveis auxiliares
	ro = 1.225  # Densidade do ar
	clmin = -0.6 * clmax
	vs = sqrt((2 * w) / (ro * s * clmax))
	vd = 1.25 * vh  # Velocidade de mergulho nao deve ser menor que 1.25 Vh
	vc = 0.9 * vh  # Velocidade de cruzeiro nao deve exceder 0.9 Vh
	va = vs * sqrt(2)
	mig =  2 * (w / (9.81 * s)) / (ro * c * a)  # Fator de massa da aeronave, usado para rajada
	kg = (0.88 * mig) / (5.3 + mig) # Fator de alivio de rajada



	# Geracao das listas que serao plotadas

	velocidade = np.arange(0.0, vd + 5.0, 0.1)

	#Curva ab
	ab_yp = list()
	ab_xp = list()
	ab_yc = list()
	ab_xc = list()
	for v in velocidade:
	    if (ro * (v ** 2) * s * clmax) / (2 * w) <= nmax and\
	    (ro * (v ** 2) * s * clmax) / (2 * w) > 1:
	        ab_xc.append(v)
	        ab_yc.append((ro * (v ** 2) * s * clmax) / (2 * w))
	    elif (ro * (v ** 2) * s * clmax) / (2 * w) <= nmax and\
	    (ro * (v ** 2) * s * clmax) / (2 * w) <= 1:
	        ab_xp.append(v)
	        ab_yp.append((ro * (v ** 2) * s * clmax) / (2 * w))
	    else:
	        ab_xc.append(sqrt((2 * nmax * w) / (ro * s * clmax)))
	        ab_yc.append(nmax)
	        break
	#Curva ae
	ae_y = list()
	ae_x = list()
	for v in velocidade:
	    if (ro * (v ** 2) * s * clmin) / (2 * w) >= nmin:
	        ae_x.append(v)
	        ae_y.append((ro * (v ** 2) * s * clmin) / (2 * w))
	    else:
	        ae_x.append(sqrt((2 * nmin * w) / (ro * s * clmin)))
	        ae_y.append(nmin)
	        break
	#Curva bc
	bc_x= [ab_xc[-1], vd]
	bc_y = [nmax for i in bc_x]
	
	#Curva cd
	cd_y = [nmin, nmax]
	cd_x = [vd for i in cd_y]
	
	#Curva de
	de_x = [ae_x[-1], vd]
	de_y = [nmin for i in de_x]
	
	#Vs (velocidade de estol)
	vs_y = [0, 1]
	vs_x = [vs for i in vs_y]
		
		# Diagrama de rajada
	# Velocidades de rajada
	rajada_vc = [1 + ((0.5 * ro * vc * a * kg* 5) / ((w) / s)),1 - ((0.5 * ro * vc * a * kg* 5) / ((w) / s)) ]
	rajada_vd = [1 + ((0.5 * ro * vd * a * kg* 2.5) / ((w) / s)),1 - ((0.5 * ro * vc * a * kg* 2.5) / ((w) / s)) ]
		
		# Velocidades estruturais
	print('---- VELOCIDADES ESTRUTURAIS ----\n')
	print('Vs(V-estol):    %6.2f m/s' % vs)
	print('Va(V-manobra):  %6.2f m/s' % va)
	print('Vc(V-cruzeiro): %6.2f m/s' % vc)
	print('Vd(V-mergulho): %6.2f m/s' % vd)
		# Fatores de carga (JAR-VLA A3)
	print('\n---- FATORES DE CARGA ----\n')
	print('n1(maximo positivo):	      %6.2f ' % nmax)
	print('n2(maximo negativo):	      %6.2f ' % nmin)
	print('n3(maximo positivo - rajada): %6.2f'  % rajada_vc[0])
	print('n4(maximo negativo - rajada): %6.2f' % rajada_vc[1])
		
	
	# Plotar listas no grafico
	plt.plot(vs_x, vs_y, 'k-',linewidth = 0.8)  #Estol positivo
	plt.plot([ae_x[-1], ae_x[-1]], [0 , ae_y[-1]], 'k-', linewidth = 0.8) # Estol negativo
	plt.plot([ab_xp[-1], ae_x[-1]], [0,0], 'k-', linewidth = 0.8) # Linha horizontal
	plt.plot(ab_xp, ab_yp, 'k-.', ab_xc, ab_yc, 'k-', ae_x, ae_y, 'k-.',
	bc_x, bc_y, 'k-', cd_x, cd_y, 'k-', de_x, de_y, 'k-',linewidth = 0.8)  # Curvas
	plt.plot([0,vc], [1, rajada_vc[0]], 'r--', [0,vc], [1, rajada_vc[1]], 'r--', linewidth = 0.8 )
	plt.plot([0,vd], [1, rajada_vd[0]], 'r--', [0,vd], [1, rajada_vd[1]], 'r--',linewidth = 0.8)
	plt.plot([vc,vd], [rajada_vc[0], rajada_vd[0]], 'r--', [vc,vd], [rajada_vc[1], rajada_vd[1]], 'r--',linewidth = 0.8)
	
	# Legendas e textos
	plt.text(ab_xc[-1], ab_yc[-1], 'A')
	plt.text(vc, rajada_vc[0], 'C')
	plt.text(vd, nmax, 'D')
	plt.text(vd, nmin, 'E')
	plt.text(vc, rajada_vc[1], 'F')
	plt.text(ae_x[-1], ae_y[-1], 'G')
	plt.title('Diagrama V-n')
	plt.ylabel("n(g's)")
	plt.xlabel("v(m/s)")
	plt.axis('normal')
	plt.grid(True)
	plt.show()
	
#w = 5.4 * 9.81  # input('> Peso da aeronave (N): ')
#s = 0.3339  # input('> Area alar(m**2): ')
#clmax = 2.1 # input('> Maximo coeficiente de sustentacao: ')
#vh = 19.45  # input('> Velocidade maxima nivelada(m/s): ')
#c = 0.21  # Corda media aerodinamica
#a = 3.3513  # Angulo de inclinacao medio da curva cl x alfa(radianos)
	
inputs = [5.4*9.81,0.3339, 2.1, 19.45, 0.21, 3.513]

vn(inputs)
print('Teste')
