#!/usr/bin/env python3
"""Perfil de luminancia del plano, por bandas horizontales.

Sirve para decidir dos cosas antes de diseñar nada:

  1. Dónde van los subtítulos y de qué color. Una banda **uniformemente clara** admite tinta;
     una **uniformemente oscura** admite papel; una **mixta** no admite ninguna tinta plana y
     hay que ir a blanco con halo o apoyar el texto en una superficie beige.
  2. Qué franja queda libre para los gráficos (la que nunca cruza la persona).

Mide el mínimo y el máximo reales, no solo la media: un cuaderno crema o el suelo de la tienda
cruzando la banda tira el contraste aunque el promedio parezca cómodo.

    python3 bandas.py video.mp4                 # barrido de todo el alto
    python3 bandas.py video.mp4 1400 1500 1600  # solo esas bandas
"""
import subprocess
import sys

H = 140          # alto de la banda, ~2 renglones de subtítulo
X, W = 190, 700  # el ancho que ocupan de verdad los glifos de un subtítulo centrado
FPS = 2          # muestras por segundo


def luma(video, y):
    """Devuelve (min, p5, mediana, p95, max) de la banda, a lo largo de todo el video."""
    r = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", video,
         "-vf", f"fps={FPS},crop={W}:{H}:{X}:{y},scale=6:2",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        capture_output=True)
    v = sorted(r.stdout)
    if not v:
        return None
    return v[0], v[len(v) // 20], v[len(v) // 2], v[len(v) * 19 // 20], v[-1]


def ratio(fg, bg):
    """Contraste WCAG entre dos grises de 0 a 255."""
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    a, b = sorted((lin(fg) * 1.0, lin(bg) * 1.0), reverse=True)
    return (a + 0.05) / (b + 0.05)


# Tintas del sistema, como gris equivalente.
INK, PAPER = 28, 251


def veredicto(p5, p95, lo, hi):
    """Qué tinta aguanta la banda.

    El juicio va por percentiles, no por el extremo absoluto: un reflejo de un fotograma suelto
    no decide el montaje, porque los subtítulos ni siquiera están en pantalla todo el rato. El
    extremo se imprime al lado como aviso, para ir a mirar ese momento en un snapshot."""
    ink, paper = ratio(INK, p5), ratio(PAPER, p95)
    aviso = ""
    if ink >= 3.0 and ratio(INK, lo) < 3.0:
        aviso = f" · ojo: cae a {ratio(INK, lo):.1f}:1 en el peor fotograma"
    if paper >= 3.0 and ratio(PAPER, hi) < 3.0:
        aviso = f" · ojo: cae a {ratio(PAPER, hi):.1f}:1 en el peor fotograma"
    if ink >= 3.0 and paper >= 3.0:
        return f"cualquiera de las dos (tinta {ink:.1f}:1 · papel {paper:.1f}:1){aviso}"
    if ink >= 3.0:
        return f"tinta ({ink:.1f}:1){aviso}"
    if paper >= 3.0:
        return f"papel ({paper:.1f}:1){aviso}"
    return "ninguna tinta plana · blanco con halo, o el texto sobre una superficie beige"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    video = sys.argv[1]
    ys = [int(a) for a in sys.argv[2:]] or list(range(0, 1920 - H + 1, 120))
    print("banda          min  p5  med  p95  max   qué aguanta")
    for y in ys:
        m = luma(video, y)
        if not m:
            continue
        lo, p5, med, p95, hi = m
        print(f"{y:4d}..{y + H:<4d}  {lo:5d}{p5:4d}{med:5d}{p95:5d}{hi:5d}   {veredicto(p5, p95, lo, hi)}")
    print("\nLos subtítulos van donde el veredicto sea limpio y la franja quede sobre la cintura")
    print("de seguridad de Instagram (y+alto < 1650). Los gráficos, en la franja de arriba que")
    print("nunca cruce la persona: compruébalo con un contact sheet, no solo con la luminancia.")


if __name__ == "__main__":
    main()
