# Produção automática diária (2 Shorts)

Executado todo dia por uma tarefa agendada do Claude Code. Os vídeos são publicados sem revisão
manual: por isso as regras abaixo são obrigatórias.

## Passo a passo

1. **Pré-checagem:** `YT_CLIENT_ID`, `YT_CLIENT_SECRET` e `YT_REFRESH_TOKEN_CURIOSIDADES` precisam existir
   (nunca imprimir os valores), e `canal.json` precisa estar no repositório. Se faltar algo, parar e avisar.
   **Nunca** usar `YT_REFRESH_TOKEN` (é do canal de manhwa).
2. **Pauta:** ler `PAUTA.md`. Se houver pedido pendente para a data de hoje (horário de Brasília), ele tem
   prioridade sobre a escolha de categoria do passo 3. Ao terminar, marcar o pedido como `feito`.
   **Histórico:** ler `historico.md` e `roteiros/*.json` para não repetir tema dos últimos 30 dias nem
   a mesma categoria nos 2 vídeos do dia.
3. **Escolher 2 temas** de categorias diferentes entre: animais, corpo humano, espaço, história,
   ciência/física, tecnologia, geografia/planeta, comida, idiomas/palavras. Preferir fatos surpreendentes
   e verificáveis ("por que o céu é azul" é fraco; "o polvo tem três corações" é bom).
4. **Fatos:** confirmar cada afirmação com WebSearch em fonte confiável (ver README). Número só com fonte.
   Na dúvida, cortar a frase. Anotar os links no campo `fontes` do roteiro e em `historico.md`.
5. **Imagens:** 3–4 por Short curto, 6–8 por longo, com `buscar_imagem.py` (termos em inglês). Olhar cada imagem baixada
   (abrir o arquivo) antes de usar: tem que mostrar o assunto de verdade. Sem imagem boa, trocar o termo
   ou o tema. Copiar a linha `CRÉDITO:` para `creditos`.
6. **Formato e voz:** rodar `python3 sortear_formato.py 2` e seguir o sorteio de cada vídeo:
   - **curto:** 6–7 segmentos, 30–45 s de narração, 3–4 imagens, 1 fato principal.
   - **longo:** 10–13 segmentos, 70–100 s de narração (nunca passar de 2 min), 6–8 imagens.
     Ex.: "5 curiosidades sobre X" (numerar na tela: "1", "2"…) ou um fato explicado a fundo.
     Cada fato extra também precisa de fonte.
   - **voz feminina/masculina:** `"voz"` na raiz do roteiro.
   - **voz dupla:** `"voz"` em cada segmento, alternando homem e mulher como uma conversa
     (um pergunta ou puxa o assunto, o outro responde). O gancho e o final ficam com a mesma voz.
7. **Roteiro:** `roteiros/<NNN>_<slug>.json` no formato de `001_polvo.json` (numeração sequencial;
   gancho forte no 1º segmento; pergunta + "segue o canal" no final;
   título com emoji e `#curiosidades`; descrição com hashtags; tags).
8. **Gerar:** `python3 make_short.py roteiros/<NNN>_<slug>.json saida/<NNN>_<slug>` e conferir 3–4 quadros
   do MP4 (`ffmpeg -ss`): texto legível, imagem certa.
9. **Enviar agendado** (público sozinho no horário de Brasília, `-03:00`):
   vídeo 1 → 12:30, vídeo 2 → 18:30 do mesmo dia:
   `python3 youtube_upload.py roteiros/<NNN>_<slug>.json saida/<NNN>_<slug> --publicar-em AAAA-MM-DDT12:30:00-03:00`
   Thumbnail: o script tenta; se der 403, seguir.
10. **Registrar:** acrescentar em `historico.md` data, temas, categorias, links e fontes; commitar roteiros,
   imagens, `saida/*/youtube.json`, `post.txt`, `tempos.json`, `thumbnail.jpg` e `historico.md`; push na `main`.
11. **Avisar** com os 2 títulos, links e horários.

## Cota da API

O projeto do Google Cloud é o mesmo do canal de manhwa (10.000 unidades/dia no total, renovadas à
meia-noite do horário do Pacífico). Desde dezembro de 2025 cada envio custa cerca de 100 unidades,
então a cota sobra. Mesmo assim, não reenviar um vídeo que falhou mais de uma vez no mesmo dia.
