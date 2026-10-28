#!/usr/bin/env python3
"""espeak-ng via ctypes (libespeak-ng.so de espeakng-loader): texto -> wav mono.
Sustituye al binario espeak-ng, que no está instalado en este contenedor."""
import ctypes, sys, wave, array
import espeakng_loader as L

AUDIO_OUTPUT_RETRIEVAL = 1
espeakRATE = 1
espeakCHARS_UTF8 = 1

lib = ctypes.CDLL(str(L.get_library_path()))
lib.espeak_Initialize.restype = ctypes.c_int
SR = lib.espeak_Initialize(AUDIO_OUTPUT_RETRIEVAL, 0, str(L.get_data_path()).encode(), 0)
if SR <= 0:
    sys.exit(f"espeak_Initialize failed: {SR}")

buf = array.array("h")
CB = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)
def _cb(wav, n, events):
    if wav and n > 0:
        buf.extend(wav[i] for i in range(n))
    return 0
cb = CB(_cb)
lib.espeak_SetSynthCallback(cb)

def say(text, out, voice="es-419", rate=165):
    del buf[:]
    if lib.espeak_SetVoiceByName(voice.encode()) != 0:
        sys.exit(f"voz no encontrada: {voice}")
    lib.espeak_SetParameter(espeakRATE, rate, 0)
    t = text.encode("utf-8")
    lib.espeak_Synth(t, len(t) + 1, 0, 0, 0, espeakCHARS_UTF8, None, None)
    lib.espeak_Synchronize()
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(buf.tobytes())
    return len(buf) / SR

if __name__ == "__main__":
    print(f"{say(sys.argv[1], sys.argv[2]):.3f} {SR}")
