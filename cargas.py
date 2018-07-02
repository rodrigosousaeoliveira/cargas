# Finalidade: gerar diagrama VN da aeronave
# Entradas: nmax = FATOR DE CARGA MAXIMO, nmin = FATOR DE CARGA MINIMO
# w = PESO DA AERONAVE, s = AREA ALAR,
#clmax = MAXIMO COEFICIENTE DE SUSTENTACAO DO PERFIL
# vd = VELOCIDADE DE MERGULHO

import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, sin, cos, radians

def vn(entradas, nmin = -1, nmax = 2):
	# Coleta de dados de entradas
	global w, s, clmax, vh, c, a, ro, clmin, vs, vc, vd, va
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
	vc = 0.9 * vh  # Velocidade de cruzeiro nao deve exceder 0.9 Vh
	vd = 1.25 * vc  # Velocidade de mergulho nao deve ser menor que 1.25 Vc
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
	print('\n---- FATORES DE CARGA(JAR-VLA A3) ----\n')
	print('n1(maximo positivo):	      %6.2f ' % nmax)
	print('n2(maximo negativo):	      %6.2f ' % nmin)
	print('n3(maximo positivo - rajada): %6.2f'  % rajada_vc[0])
	print('n4(maximo negativo - rajada): %6.2f' % rajada_vc[1])
	# Condicaoes de voo (JAR-VLA A9(b)1)
	print('\n---- CONDICOES DE VOO(JAR-VLA A9(b)1) ---\n')
	print(' CDV |  A  |  C  |  D  |  E  |  F  |  G  |')
	print('------------------------------------------')
	print('  v  |%5.2f|%5.2f|%5.2f|%5.2f|%5.2f|%5.2f|' % (va, vc, vd, vd, vc, ae_x[-1]))
	print('------------------------------------------')
	print('  n  |%5.2f|%5.2f|%5.2f|%5.2f|%5.2f|%5.2f|\n' % (ab_yc[-1], rajada_vc[0], nmax, nmin, rajada_vc[1], ae_y[-1]))
	
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
	
	# Retorna a lista de condicoes de voos [A, C, D, E, F, G]
	return [[va, ab_yc[-1]], [vc, rajada_vc[0]], [vd, nmax], [vd, nmin], [vc, rajada_vc[1]], [ae_x[-1], ae_y[-1]]]

def lt(cdv, ca_cg, ca_ca, cm):
	# Funcao para calcular sustentacao da empenagem em equilibrio na CDV dada, retorna sustentacao em Newtons
	# Sintaxe: cdv = [v, n], ca_ca = distancia ca-ca, ca_cg = distancia ca da asa-cg 
	# cm = coeficiente de momento da asa
	[v, n] = cdv
	try:
		lt = (((ca_cg * 2 * n * w)/ (ro * (v ** 2) * s)) + cm) * ((ro * (v ** 2) * s * c)/(2 * ca_ca))
		return lt
	except:
		print('ERRO: provavelmente algumas variáveis não foram declaradas. Rode a funcao vn()')

def tdp(cg_principal, cg_triquilha, w, na, mi, h):
	# Calcula as cargas críticas no trem de pouso de acordo com os parametros:
	# -cg_principal = distancia horizontal em metros do CG ao TDP principal
	# -cg_triquilha = distancia horizontal em metros do CG a triquilha
	# -w = peso em newtons
	# -na = fator de carga inercial de aterragem
	# -mi = coeficiente de atrito entre pista e conjunto TDP
	# -h = altura do cg em relacao ao TDP
	sustentacao = (2/3) * w # Segundo a JAR VLA 473(b)
	
	# 1 - ATERRAGEM NIVELADA EM 3 RODAS
	
	# Forca vertical atuante em cada roda do TDP principal
	fv_principal_1 = ((mi * na * w * h) - (cg_triquilha * (na * w - sustentacao)))/(-2 *(cg_principal + cg_triquilha))
	# Forca vertical atuante na triquilha
	fv_triquilha_1 = na * w - sustentacao - (2 * fv_principal_1)
	# Forca horizontal atuante em cada roda do TDP principal
	fh_principal_1 = (mi * na * w)/(1 + (fv_principal_1/ fv_triquilha_1))
	# Forca horizontal atuante na triquilha
	fh_triquilha_1 = fh_principal_1 * (fv_principal_1/ fv_triquilha_1)
	
	print('\nATERRAGEM NIVELADA EM 3 RODAS\n')
	print('Forca vertical em cada roda do TDP principal: %6.2f' % fv_principal_1)
	print('Forca horizontal em cada roda do TDP principal: %6.2f' % fh_principal_1)
	print('Forca vertical na triquilha: %6.2f' % fv_triquilha_1)
	print('Forca horizontal na triquilha: %6.2f' % fh_triquilha_1)
	# 2 - ATERRAGEM NIVELADA NO TDP PRINCIPAL
	
	# Forca vertical atuante em cada roda do tdp principal
	fv_principal_2 = (na * w) / 2
	# Forca horizontal atuante em cada roda do TDP principal
	fh_principal_2 = (mi * na * w) / 2
	
	print('\nATERRAGEM NIVELADA EM 2 RODAS\n')
	print('Forca vertical em cada roda do TDP principal: %6.2f' % fv_principal_2)
	print('Forca horizontal em cada roda do TDP principal: %6.2f' % fh_principal_2)
	
	# 3 - ATERRAGEM NIVELADA EM UMA RODA
	
	# Forca vertical atuante em cada roda do tdp principal
	fv_principal_3 = (na * w) 
	# Forca horizontal atuante em cada roda do TDP principal
	fh_principal_3 = (mi * na * w)
	
	print('\nATERRAGEM NIVELADA EM 1 RODAS\n')
	print('Forca vertical em cada roda: %6.2f' % fv_principal_3)
	print('Forca horizontal em cada roda: %6.2f' % fh_principal_3)
	
	# 4 - CONDICAO DE CARGAS LATERAIS
	# De acordo com a JAR VLA 485:
	nv = 1.33 # (b) Fator de carga vertical deve ser igual a 1.33 dividido igualmente entre as rodas
	nh = 0.83 # (c) Fator de carga lateral deve ser igual a 0.83 dividido em:
		  #  0.5 em uma roda e 0.33 em outra roda
	# Forca vertical atuante em cada roda do tdp
	fv_4 = (nv * w)/3 
	# Forca horizontal atuante em cada roda do TDP principal
	fh_roda1 = 0.5 * w
	fh_roda2 = 0.33 * w
	
	print('\nATERRAGEM COM CARGAS LATERAIS\n')
	print('Forca vertical em cada roda: %6.2f' % fv_4)
	print('Forca horizontal na roda exterior: %6.2f' % fh_roda1)
	print('Forca horizontal na roda interior: %6.2f' % fh_roda2)
	
	return [fv_principal_1, fv_triquilha_1, fh_principal_1, fh_triquilha_1,
	fv_principal_2, fh_principal_2, fv_principal_3, fh_principal_3, fv_4,
	fh_roda1, fh_roda2]

def boom(comprimento, angulo, fz, fx, d1, d2):
	# Calculo e plota o diagrama de esforcos solicitantes no boom
	# DESCONSIDERANDO PESO DA EMPENAGEM E BOOM
	# comprimento = comprimento do boom em metros
	# angulo = inclinacao do boom em relacao a horizontal
	# fz = sustentacao da eh (sentido positivo para cima) - peso empenagem
	# fx = carga critica da ev
	# d1 = distancia perpendicular ao boom de onde fx e aplicada
	# d2 = distancia do ponto de articulacao da eh ate a extremidade do boom
	
	coordenada = np.arange(0, comprimento + 0.001, 0.001) # coordenada s no boom
	# Listas com esforcos em determinados pontos
	cortante_z = []
	normal = []
	momento_z = []
	cortante_x = []
	momento_x = []
	torcao = []
	for s in coordenada:
		if s > d2: # Esforcos apos a fixacao da eh sao nulos
			cortante_z.append(-fz * cos(radians(angulo)))
			normal.append(-fz * sin(radians(angulo)))
			momento_z.append(-fz * cos(radians(angulo)) * (s-d2))
			cortante_x.append(-fx)
			momento_x.append(-fx * (s - d2))
			torcao.append(-fx * d1)
		else:
			cortante_z.append(0)
			normal.append(0)
			momento_z.append(0)
			cortante_x.append(0)
			momento_x.append(0)
			torcao.append(0)
	# Cortante ZY
	plt.subplot(321)
	plt.plot(coordenada, cortante_z)
	plt.title('Cortante ZY')
	plt.grid(True)


	# Normal ZY
	plt.subplot(322)
	plt.plot(coordenada, normal)
	plt.title('Normal ZY')
	plt.grid(True)


	# Momento ZY
	plt.subplot(323)
	plt.plot(coordenada, momento_z)
	plt.title('Momento ZY')
	plt.grid(True)
	
	# Cortante XY
	plt.subplot(324)
	plt.plot(coordenada, cortante_x)
	plt.title('Cortante XY')
	plt.grid(True)
	
	# Momento XY
	plt.subplot(325)
	plt.plot(coordenada, momento_x)
	plt.title('Momento XY')
	plt.grid(True)
	
	# Torcao
	plt.subplot(326)
	plt.plot(coordenada, torcao)
	plt.title('Torcao XY')
	plt.grid(True)
	
	plt.show()
