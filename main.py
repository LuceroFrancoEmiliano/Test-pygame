import pygame
import random


pygame.init()

#CONFIGURACIONES DE PANTALLA
ANCHO=800
ALTO=550
ventana=pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Test por mi cuenta")
reloj = pygame.time.Clock()

#Fuente de texto
fuente = pygame.font.SysFont("Arial",25, bold= True)


#TAMAÑO TILE
TAMANO_TILE=50

#mapa
mapa_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#lista de objetos en el mapa para las colisiones
muros = []
for indiceFila, fila in enumerate(mapa_data):
    for indiceColumna, valor in enumerate(fila):
        if valor == 1:
            rectangulo_muro = pygame.Rect(indiceColumna * TAMANO_TILE, indiceFila * TAMANO_TILE, TAMANO_TILE, TAMANO_TILE)
            muros.append(rectangulo_muro)

#JUGADOR
jugador_rect = pygame.Rect(60, 60, 35, 35)
velocidad = 5
puntos=0
meta_puntos = 2  # Cantidad para ganar
ganaste = False


#Monedas
monedas=[]
tiempoDeSpawnDeMonedas=3000
tiempoUltimoSpawnDeMoneda = pygame.time.get_ticks()

#Monedas negativas
monedasNegativas=[]
tiempoDeSpawnDeMonedasNegativa=3500
tiempoUltimoSpawnDeMonedaNegativa = pygame.time.get_ticks()

ejecutando = True
while ejecutando:

    tiempoActualPrograma = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

    #llena el fondo de gris
    ventana.fill((30,30,30))
    
    

    #POSICION DEL JUGADOR para colisiones y no atravesar los bloques
    pos_anterior = jugador_rect.copy()
    #LOGICA DEL MOVIMIENTO
    if not ganaste:
        tecla= pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] : jugador_rect.x -= velocidad 
        if tecla[pygame.K_RIGHT] : jugador_rect.x += velocidad
        if tecla[pygame.K_UP] : jugador_rect.y -= velocidad 
        if tecla[pygame.K_DOWN] : jugador_rect.y += velocidad 



    #COLISION DEL PERSONAJE
    for muro in muros:
        if jugador_rect.colliderect(muro):
            jugador_rect = pos_anterior

    #LOGICA DE SPAWN MONEDAS
    tiempoTranscurridoPrograma = tiempoActualPrograma- tiempoUltimoSpawnDeMoneda

    if(tiempoTranscurridoPrograma >= tiempoDeSpawnDeMonedas):
        moneda_x = random.randint(50,ANCHO-50)
        moneda_y = random.randint(50, 500)
        nuevaMoneda = pygame.Rect(moneda_x,moneda_y,20,20)

        if not any(nuevaMoneda.colliderect(m) for m in muros):
            monedas.append(nuevaMoneda)
            tiempoUltimoSpawnDeMoneda = tiempoActualPrograma

    tiempoTranscurridoNegativa = tiempoActualPrograma - tiempoUltimoSpawnDeMonedaNegativa
    if tiempoTranscurridoNegativa >= tiempoDeSpawnDeMonedasNegativa:
        monedaNegativa_x = random.randint(50, ANCHO - 50)
        monedaNegativa_y = random.randint(50, ALTO - 50)
        nuevaMonedaNegativa = pygame.Rect(monedaNegativa_x, monedaNegativa_y, 20, 20)

        # Corregido el 'for m in muros'
        if not any(nuevaMonedaNegativa.colliderect(m) for m in muros):
            monedasNegativas.append(nuevaMonedaNegativa)
            tiempoUltimoSpawnDeMonedaNegativa = tiempoActualPrograma


    #LOGICA RECOLECCION
    for moneda in monedas:
        if jugador_rect.colliderect(moneda):
            monedas.remove(moneda)
            puntos+=1
            if puntos >= meta_puntos:
                ganaste = True # ¡Activamos el modo victoria!   

    #Logica monedas negativas
    for moneda in monedasNegativas:
        if jugador_rect.colliderect(moneda):
            monedasNegativas.remove(moneda)
            puntos = max(0, puntos - 2)

##LOGICA DE LOS MUROS
    for muro in muros:
        pygame.draw.rect(ventana,(0,100,200),muro)
        pygame.draw.rect(ventana,(0,100,200),muro,1)
    #LOGICA DE MONEDAS
    for moneda in monedas:
        pygame.draw.circle(ventana,(255,215,50), moneda.center,10)
    #LOGICA MONEDAS NEGATIVAS
    for moneda in monedasNegativas:
        pygame.draw.circle(ventana,(255,0,0), moneda.center,16)
    #DIBUJANDO EL PERSONAJE    (donde queremos que se dibuje, (color), que atributos adapta, tamaño )
    pygame.draw.circle(ventana, (255, 50, 50), jugador_rect.center, 16)

    #LOGICA VICTORIA
    if ganaste:
        # Creamos un rectángulo oscuro que tape un poco el juego
        superficie_final = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        superficie_final.fill((0, 0, 0, 150)) # Negro con transparencia
        ventana.blit(superficie_final, (0,0))

        # Renderizamos el texto de victoria
        texto_victoria = fuente.render("¡FELICIDADES! HAS GANADO", True, (0, 255, 0))
        texto_instrucciones = fuente.render("Presiona ESC para salir", True, (255, 255, 255))
        
        # Lo centramos en pantalla
        ventana.blit(texto_victoria, (ANCHO // 2 - 150, ALTO // 2 - 20))
        ventana.blit(texto_instrucciones, (ANCHO // 2 - 130, ALTO // 2 + 30))

        # Si presiona Escape, cerramos el juego
        if tecla[pygame.K_ESCAPE]:
            ejecutando = False

    #INTERFAZ
    texto_puntos = fuente.render(f"PUNTOS: {puntos}", True, (255, 255, 255))
    ms_restantes = tiempoDeSpawnDeMonedas - (tiempoActualPrograma - tiempoUltimoSpawnDeMoneda)
    segundos_display = max(0, ms_restantes // 1000)
    textoTimer = fuente.render(f"Moneda en: {segundos_display}s", True, (200, 200, 0))

    # 2. LOS PEGAS en la ventana (Blit) ANTES del flip
    ventana.blit(texto_puntos, (20, 20))
    ventana.blit(textoTimer, (ANCHO - 350, 20))

    # 3. AHORA SÍ, muestras todo el conjunto al usuario
    pygame.display.flip()

    # 4. Controlas los FPS
    reloj.tick(60)

pygame.quit()