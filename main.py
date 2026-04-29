import asyncio
import pygame
import random

# 1. INICIALIZACION
pygame.init()

# CONFIGURACIONES DE PANTALLA
ANCHO = 800
ALTO = 550
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TestPygame")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 25, bold=True)

# TAMANO TILE Y MAPA
TAMANO_TILE = 50
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

muros = []
for f, fila in enumerate(mapa_data):
    for c, valor in enumerate(fila):
        if valor == 1:
            muros.append(pygame.Rect(c * TAMANO_TILE, f * TAMANO_TILE, TAMANO_TILE, TAMANO_TILE))

async def main():
    jugador_rect = pygame.Rect(60, 60, 35, 35)
    velocidad = 5
    puntos = 0
    meta_puntos = 10
    ganaste = False
    ejecutando = True

    monedas = []
    monedasNegativas = []
    t_spawn = 3000
    t_spawn_neg = 3500
    ultimo_t = pygame.time.get_ticks()
    ultimo_t_neg = pygame.time.get_ticks()

    while ejecutando:
        t_actual = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False

        ventana.fill((30, 30, 30))
        pos_anterior = jugador_rect.copy()
        
        if not ganaste:
            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_LEFT]:  jugador_rect.x -= velocidad 
            if tecla[pygame.K_RIGHT]: jugador_rect.x += velocidad
            if tecla[pygame.K_UP]:    jugador_rect.y -= velocidad 
            if tecla[pygame.K_DOWN]:  jugador_rect.y += velocidad 

            for muro in muros:
                if jugador_rect.colliderect(muro):
                    jugador_rect = pos_anterior

        # SPAWN
        if (t_actual - ultimo_t) >= t_spawn:
            m_x, m_y = random.randint(50, 750), random.randint(50, 500)
            nueva = pygame.Rect(m_x, m_y, 20, 20)
            if not any(nueva.colliderect(m) for m in muros):
                monedas.append(nueva)
                ultimo_t = t_actual

        if (t_actual - ultimo_t_neg) >= t_spawn_neg:
            m_x, m_y = random.randint(50, 750), random.randint(50, 500)
            nueva = pygame.Rect(m_x, m_y, 20, 20)
            if not any(nueva.colliderect(m) for m in muros):
                monedasNegativas.append(nueva)
                ultimo_t_neg = t_actual

        # RECOLECCION
        for m in monedas[:]:
            if jugador_rect.colliderect(m):
                monedas.remove(m)
                puntos += 1
                if puntos >= meta_puntos: ganaste = True

        for m in monedasNegativas[:]:
            if jugador_rect.colliderect(m):
                monedasNegativas.remove(m)
                puntos = max(0, puntos - 2)

        # DIBUJO
        for muro in muros:
            pygame.draw.rect(ventana, (0, 100, 200), muro)
            pygame.draw.rect(ventana, (255, 255, 255), muro, 1)

        for m in monedas: pygame.draw.circle(ventana, (255, 215, 50), m.center, 10)
        for m in monedasNegativas: pygame.draw.circle(ventana, (255, 0, 0), m.center, 10)
        pygame.draw.circle(ventana, (255, 50, 50), jugador_rect.center, 16)

        if ganaste:
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            ventana.blit(overlay, (0, 0))
            txt = fuente.render("VICTORIA! ESC para salir", True, (0, 255, 0))
            ventana.blit(txt, (ANCHO // 2 - 150, ALTO // 2))
            if pygame.key.get_pressed()[pygame.K_ESCAPE]: ejecutando = False

        txt_p = fuente.render(f"PUNTOS: {puntos}", True, (255, 255, 255))
        ventana.blit(txt_p, (20, 20))

        pygame.display.flip()
        reloj.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())