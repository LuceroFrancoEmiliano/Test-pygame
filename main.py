import asyncio
import pygame
import random

# 1. INICIALIZACIÓN
pygame.init()

# CONFIGURACIONES DE PANTALLA
ANCHO = 800
ALTO = 550
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Juego en la Web")
reloj = pygame.time.Clock()

# Fuente de texto (Usamos SysFont para compatibilidad)
fuente = pygame.font.SysFont("Arial", 25, bold=True)

# TAMAÑO TILE
TAMANO_TILE = 50

# MAPA
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

# Lista de muros
muros = []
for indiceFila, fila in enumerate(mapa_data):
    for indiceColumna, valor in enumerate(fila):
        if valor == 1:
            rectangulo_muro = pygame.Rect(indiceColumna * TAMANO_TILE, indiceFila * TAMANO_TILE, TAMANO_TILE, TAMANO_TILE)
            muros.append(rectangulo_muro)

# VARIABLES GLOBALES DE ESTADO
EJECUTANDO = True
ganaste = False
puntos = 0
meta_puntos = 10  # Aumentado para que sea más divertido

# JUGADOR
jugador_rect = pygame.Rect(60, 60, 35, 35)
velocidad = 5

# MONEDAS
monedas = []
tiempoDeSpawnDeMonedas = 3000
tiempoUltimoSpawnDeMoneda = pygame.time.get_ticks()

# MONEDAS NEGATIVAS
monedasNegativas = []
tiempoDeSpawnDeMonedasNegativa = 3500
tiempoUltimoSpawnDeMonedaNegativa = pygame.time.get_ticks()

async def main():
    # Referenciamos las variables globales que vamos a modificar
    global EJECUTANDO, ganaste, puntos, tiempoUltimoSpawnDeMoneda, tiempoUltimoSpawnDeMonedaNegativa

    while EJECUTANDO:
        tiempoActualPrograma = pygame.time.get_ticks()

        # 1. EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EJECUTANDO = False

        # 2. LÓGICA DE MOVIMIENTO
        pos_anterior = jugador_rect.copy()
        
        if not ganaste:
            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_LEFT]:  jugador_rect.x -= velocidad 
            if tecla[pygame.K_RIGHT]: jugador_rect.x += velocidad
            if tecla[pygame.K_UP]:    jugador_rect.y -= velocidad 
            if tecla[pygame.K_DOWN]:  jugador_rect.y += velocidad 

            # Colisión con muros
            for muro in muros:
                if jugador_rect.colliderect(muro):
                    jugador_rect = pos_anterior

        # 3. SPAWN DE MONEDAS (DORADAS)
        if (tiempoActualPrograma - tiempoUltimoSpawnDeMoneda) >= tiempoDeSpawnDeMonedas:
            m_x = random.randint(50, ANCHO - 50)
            m_y = random.randint(50, ALTO - 50)
            nuevaM = pygame.Rect(m_x, m_y, 20, 20)
            if not any(nuevaM.colliderect(m) for m in muros):
                monedas.append(nuevaM)
                tiempoUltimoSpawnDeMoneda = tiempoActualPrograma

        # 4. SPAWN DE MONEDAS (ROJAS)
        if (tiempoActualPrograma - tiempoUltimoSpawnDeMonedaNegativa) >= tiempoDeSpawnDeMonedasNegativa:
            mn_x = random.randint(50, ANCHO - 50)
            mn_y = random.randint(50, ALTO - 50)
            nuevaMN = pygame.Rect(mn_x, mn_y, 20, 20)
            if not any(nuevaMN.colliderect(m) for m in muros):
                monedasNegativas.append(nuevaMN)
                tiempoUltimoSpawnDeMonedaNegativa = tiempoActualPrograma

        # 5. RECOLECCIÓN
        for m in monedas[:]:
            if jugador_rect.colliderect(m):
                monedas.remove(m)
                puntos += 1
                if puntos >= meta_puntos:
                    ganaste = True

        for mn in monedasNegativas[:]:
            if jugador_rect.colliderect(mn):
                monedasNegativas.remove(mn)
                puntos = max(0, puntos - 2)

        # 6. DIBUJO
        ventana.fill((30, 30, 30))
        
        for muro in muros:
            pygame.draw.rect(ventana, (0, 100, 200), muro)
            pygame.draw.rect(ventana, (255, 255, 255), muro, 1)

        for m in monedas:
            pygame.draw.circle(ventana, (255, 215, 50), m.center, 10)

        for mn in monedasNegativas:
            pygame.draw.circle(ventana, (255, 0, 0), mn.center, 10)

        pygame.draw.circle(ventana, (255, 50, 50), jugador_rect.center, 16)

        # 7. INTERFAZ Y VICTORIA
        if ganaste:
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            ventana.blit(overlay, (0, 0))
            txt_v = fuente.render("¡FELICIDADES! HAS GANADO", True, (0, 255, 0))
            ventana.blit(txt_v, (ANCHO // 2 - 150, ALTO // 2 - 20))
            
            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_ESCAPE]:
                EJECUTANDO = False

        # Textos de UI
        txt_p = fuente.render(f"PUNTOS: {puntos}", True, (255, 255, 255))
        ms_falta = tiempoDeSpawnDeMonedas - (tiempoActualPrograma - tiempoUltimoSpawnDeMoneda)
        seg_d = max(0, ms_falta // 1000)
        txt_t = fuente.render(f"Moneda en: {seg_d}s", True, (200, 200, 0))
        
        ventana.blit(txt_p, (20, 20))
        ventana.blit(txt_t, (ANCHO - 250, 20))

        # FINALIZAR FRAME
        pygame.display.flip()
        reloj.tick(60)
        
        # CEDER EL PASO AL NAVEGADOR (Obligatorio para la web)
        await asyncio.sleep(0)

    pygame.quit()

# EJECUCIÓN ASÍNCRONA
asyncio.run(main())