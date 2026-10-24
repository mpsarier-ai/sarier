#!/bin/bash
# alinear.sh DIR — guion.txt + audio del video -> captions.json, sin ASR.
#
# espeak-ng sintetiza cada línea del guion, se concatenan, se sacan los MFCC de la síntesis y del
# audio real y un DTW mapea las fronteras. Después snap.py pega cada frontera a una pausa real de
# silencedetect, pero solo cuando no deja la línea ilegible.
#
# No usa ASR a propósito: huggingface.co está bloqueado por la política de red del entorno, así que
# el modelo de whisper no se puede descargar. El guion lo pone el cliente.
set -euo pipefail
DIR="${1:?uso: alinear.sh DIR}"
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

[ -f guion.txt ] || { echo "falta guion.txt en $DIR"; exit 1; }
[ -f orig.mov ] || [ -f orig.mp4 ] || { echo "falta orig.mov / orig.mp4 en $DIR"; exit 1; }
SRC=orig.mov; [ -f orig.mov ] || SRC=orig.mp4

cp -n "$SKILL/align.py" "$SKILL/snap.py" "$SKILL/espeak_say.py" . 2>/dev/null || true
mkdir -p tts tts16
rm -f tts/*.wav tts16/*.wav

[ -f audio16k.wav ] || ffmpeg -nostdin -y -v error -i "$SRC" -vn -ac 1 -ar 16000 audio16k.wav

python3 - <<'PY'
import subprocess, sys
sys.path.insert(0, ".")
from espeak_say import say
lines = [l.rstrip("\n") for l in open("guion.txt", encoding="utf-8") if l.strip()]
for i, l in enumerate(lines, 1):
    say(l, f"tts/{i:02d}.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f"tts/{i:02d}.wav",
                    "-ac", "1", "-ar", "16000", f"tts16/{i:02d}.wav"], check=True)
print(f"{len(lines)} líneas · la más larga: {max(len(x) for x in lines)} caracteres")
PY

python3 -I - <<'PY'
import glob, wave
t, bounds, parts = 0.0, [0.0], []
for p in sorted(glob.glob("tts16/*.wav")):
    w = wave.open(p); t += w.getnframes() / w.getframerate(); w.close()
    bounds.append(round(t, 3)); parts.append(p)
open("bounds.txt", "w").write("\n".join(str(x) for x in bounds))
open("concat.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
PY

ffmpeg -nostdin -y -v error -f concat -safe 0 -i concat.txt -c copy synth16k.wav
python3 align.py audio16k.wav synth16k.wav bounds.txt guion.txt captions.dtw.json > align.log 2>&1
python3 snap.py

echo
echo "Revisa la columna de car/s: por debajo de ~10 o por encima de ~26 la línea no cuadra con"
echo "el audio y hay que repartirla distinto en guion.txt. Una pausa de más de un segundo que"
echo "caiga dentro de una línea casi siempre es un corte de sección: ajústala a mano."
