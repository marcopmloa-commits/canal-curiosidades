# Produção automática diária (2 Shorts)

Executado todo dia por uma tarefa agendada do Claude Code. Os vídeos são publicados sem revisão
manual: por isso as regras abaixo são obrigatórias.

## Passo a passo

1. **Pré-checagem:** `YT_CLIENT_ID`, `YT_CLIENT_SECRET` e `YT_REFRESH_TOKEN_CURIOSIDADES` precisam existir
   (nunca imprimir os valores), e `canal.json` precisa estar no repositório. Se faltar algo, parar e avisar.
   **Nunca** usar `YT_REFRESH_TOKEN` (é do canal de manhwa).
2. **Histórico:** ler `historico.md` e `roteiros/*.json` para não repetir tema dos últimos 30 dias nem
   a mesma categoria nos 2 vídeos do dia.
3. **Escolher 2 temas** de categorias diferentes entre: animais, corpo humano, espaço, história,
   ciência/física, tecnologia, geografia/planeta, comida, idiomas/palavras. Preferir fatos surpreendentes
   e verificáveis ("por que o céu é azul" é fraco; "o polvo tem três corações" é bom).
4. **Fatos:** confirmar cada afirmação com WebSearch em fonte confiável (ver README). Número só com fonte.
   Na dúvida, cortar a frase. Anotar os links no campo `fontes` do roteiro e em `historico.md`.
5. **Imagens:** 3–4 por Short com `buscar_imagem.py` (termos em inglês). Olhar cada imagem baixada
   (abrir o arquivo) antes de usar: tem que mostrar o assunto de verdade. Sem imagem boa, trocar o termo
   ou o tema. Copiar a linha `CRÉDITO:` para `creditos`.
6. **Roteiro:** `roteiros/<NNN>_<slug>.json` no formato de `001_polvo.json` (numeração sequencial;
   6–7 segmentos; 30–45 s de narração; gancho forte no 1º segmento; pergunta + "segue o canal" no final;
   título com emoji e `#curiosidades`; descrição com hashtags; tags).
7. **Gerar:** `python3 make_short.py roteiros/<NNN>_<slug>.json saida/<NNN>_<slug>` e conferir 3–4 quadros
   do MP4 (`ffmpeg -ss`): texto legível, imagem certa.
8. **Enviar agendado** (público sozinho no horário de Brasília, `-03:00`):
   vídeo 1 → 12:30, vídeo 2 → 18:30 do mesmo dia:
   `python3 youtube_upload.py roteiros/<NNN>_<slug>.json saida/<NNN>_<slug> --publicar-em AAAA-MM-DDT12:30:00-03:00`
   Thumbnail: o script tenta; se der 403, seguir.
9. **Registrar:** acrescentar em `historico.md` data, temas, categorias, links e fontes; commitar roteiros,
   imagens, `saida/*/youtube.json`, `post.txt`, `tempos.json`, `thumbnail.jpg` e `historico.md`; push na `main`.
10. **Avisar** com os 2 títulos, links e horários.

## Cota da API

O projeto do Google Cloud é o mesmo do canal de manhwa (10.000 unidades/dia no total, renovadas à
meia-noite do horário do Pacífico). Desde dezembro de 2025 cada envio custa cerca de 100 unidades,
então a cota sobra. Mesmo assim, não reenviar um vídeo que falhou mais de uma vez no mesmo dia.
