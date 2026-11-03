"""Sorteia o formato e a voz de cada Short do dia.

Uso: python3 sortear_formato.py [quantidade]   (padrão: 2)

Formatos:
  curto  30–45 s, 6–7 cenas, 1 fato principal (2 em cada 3 vídeos, em média)
  longo  70–100 s, 10–13 cenas, "N curiosidades sobre X" ou um fato explicado a fundo (1 em cada 3)
Vozes:
  feminina  pt-BR-FranciscaNeural
  masculina pt-BR-AntonioNeural
  dupla     as duas se alternando, como uma conversa (só no formato longo)
"""
import random, sys

VOZES = {"feminina": "pt-BR-FranciscaNeural", "masculina": "pt-BR-AntonioNeural"}

n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
for i in range(1, n + 1):
    formato = "longo" if random.random() < 1 / 3 else "curto"
    opcoes = ["feminina", "masculina"] + (["dupla"] if formato == "longo" else [])
    voz = random.choice(opcoes)
    detalhe = (f'"voz": "{VOZES[voz]}" na raiz' if voz != "dupla"
               else '"voz" em cada segmento, alternando pt-BR-AntonioNeural e pt-BR-FranciscaNeural')
    print(f"Vídeo {i}: formato {formato}, voz {voz} ({detalhe})")
