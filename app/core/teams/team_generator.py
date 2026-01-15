import random
import statistics
from typing import List, Optional
from app.schemas.team import Jugador, GenerarEquiposResponse, EquipoResponse


def media_segura(valores: list[float]) -> float:
    return statistics.mean(valores) if valores else 0


def generar_equipos(jugadores_input: List[Jugador]) -> GenerarEquiposResponse:

    if len(jugadores_input) < 2:
        raise ValueError("No hay suficientes jugadores para formar equipos")

    # Normalizar a dict (manteniendo tu lógica original)
    jugadores = []
    for j in jugadores_input:
        jugadores.append({
            "id_jugador":j.id_jugador,
            "Jugador": j.jugador,
            "Puntos": j.puntos,
            "Estrellas": j.estrellas,
            "PosicionJuego": j.posicion,
            "PosicionJuegoNorm": j.posicion.lower(),
            "Mayor": "si" if j.mayor else "no",
            "MayorNorm": "si" if j.mayor else "no",
        })

    # -----------------------
    # BANCA SI ES IMPAR
    # -----------------------
    bench = None
    if len(jugadores) % 2 == 1:
        candidatos = sorted(jugadores, key=lambda x: (x["Puntos"], x["Estrellas"]))
        top4 = sorted(jugadores, key=lambda x: x["Puntos"], reverse=True)[:4]

        for c in candidatos:
            if (
                c["PosicionJuegoNorm"] != "goalkeeper"
                and c not in top4
                and c["MayorNorm"] != "si"
            ):
                bench = c
                break

        if bench is None:
            bench = candidatos[0]

        jugadores.remove(bench)

    # -----------------------
    # CONFIGURACIÓN
    # -----------------------
    por_equipo = len(jugadores) // 2

    arqueros = [j for j in jugadores if j["PosicionJuegoNorm"] == "goalkeeper"]
    if len(arqueros) < 2:
        raise ValueError("Se requieren dos arqueros")

    arquero_rojo = random.choice(arqueros)
    arquero_azul = random.choice([a for a in arqueros if a != arquero_rojo])

    equipo_rojo = [arquero_rojo]
    equipo_azul = [arquero_azul]
    asignados = [arquero_rojo, arquero_azul]

    # -----------------------
    # TOP 4 POR PUNTOS
    # -----------------------
    jugadores_ordenados = sorted(jugadores, key=lambda x: x["Puntos"], reverse=True)

    for i, equipo in zip(range(4), [equipo_rojo, equipo_azul, equipo_rojo, equipo_azul]):
        if i < len(jugadores_ordenados):
            j = jugadores_ordenados[i]
            if j not in asignados and len(equipo) < por_equipo:
                equipo.append(j)
                asignados.append(j)

    # -----------------------
    # JUGADORES MAYOR
    # -----------------------
    mayores = [j for j in jugadores if j["MayorNorm"] == "si" and j not in asignados]
    turno_rojo = True

    for jm in mayores:
        if turno_rojo and len(equipo_rojo) < por_equipo:
            equipo_rojo.append(jm)
        elif len(equipo_azul) < por_equipo:
            equipo_azul.append(jm)
        asignados.append(jm)
        turno_rojo = not turno_rojo

    # -----------------------
    # RESTO DE JUGADORES
    # -----------------------
    restantes = [j for j in jugadores if j not in asignados]

    random.shuffle(restantes)
    for r in restantes:
        if len(equipo_rojo) < por_equipo:
            equipo_rojo.append(r)
        elif len(equipo_azul) < por_equipo:
            equipo_azul.append(r)

    # -----------------------
    # RESPUESTA
    # -----------------------
    def build_equipo(nombre: str, equipo: list):
        return EquipoResponse(
            nombre=nombre,
            media_estrellas=round(media_segura([j["Estrellas"] for j in equipo]), 2),
            jugadores=[
                Jugador(
                    id_jugador=j["id_jugador"],
                    jugador=j["Jugador"],
                    puntos=j["Puntos"],
                    estrellas=j["Estrellas"],
                    posicion=j["PosicionJuego"],
                    mayor=j["MayorNorm"] == "si",
                )
                for j in equipo
            ],
        )

    return GenerarEquiposResponse(
        equipo_rojo=build_equipo("Rojo", equipo_rojo),
        equipo_azul=build_equipo("Azul", equipo_azul),
        banca=Jugador(
            id_jugador=bench["id_jugador"],
            jugador=bench["Jugador"],
            puntos=bench["Puntos"],
            estrellas=bench["Estrellas"],
            posicion=bench["PosicionJuego"],
            mayor=bench["MayorNorm"] == "si",
        )
        if bench
        else None,
    )