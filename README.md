# Canal de Curiosidades

Canal de Shorts de curiosidades (ciência, natureza, história, corpo humano, espaço, tecnologia).
2 Shorts por dia, gerados e publicados automaticamente.

## Gerar um Short

```bash
pip install -r requirements.txt
python3 make_short.py roteiros/001_polvo.json saida/001_polvo
```

Saída em `saida/<nome>/`: `short.mp4` (1080x1920), `thumbnail.jpg`, `post.txt` e `tempos.json`.

## Imagens

```bash
python3 buscar_imagem.py "octopus" roteiros/img/001_polvo/01.jpg --listar   # ver opções
python3 buscar_imagem.py "octopus" roteiros/img/001_polvo/01.jpg            # baixar a primeira boa
```

Busca no Openverse só fotos com licença livre (CC0, domínio público, CC BY, CC BY-SA) e imprime a
linha de crédito, que vai no campo `creditos` do roteiro. O envio põe os créditos na descrição.

## Roteiro (JSON)

Cada item de `segmentos`: `fala` (narração), `destaque` (título na tela), `sub` (selo, opcional),
`tamanho` (fonte, opcional), `imagem` (caminho relativo ao JSON, opcional), `foco` (0–1, recorte vertical).
Na raiz: `titulo`, `descricao`, `tags`, `thumb`, `thumb_sub`, `thumb_imagem`, `voz`, `velocidade`,
`tag` (selo do topo, padrão "VOCÊ SABIA?"), `creditos` (lista) e `fontes` (lista de links que confirmam os fatos).

## Envio ao YouTube

```bash
python3 youtube_upload.py roteiros/001_polvo.json saida/001_polvo --publicar-em 2026-11-04T12:00:00-03:00
```

Usa `YT_CLIENT_ID` e `YT_CLIENT_SECRET` (o mesmo projeto do Google Cloud do canal de manhwa) e
`YT_REFRESH_TOKEN_CURIOSIDADES` (token autorizado no canal de curiosidades, via `youtube_auth.py`).
Antes de enviar, confere se o token é do canal registrado em `canal.json`: se não for, não envia nada.

## Regras do canal

- Todo fato precisa de pelo menos uma fonte confiável (enciclopédia, universidade, museu, agência
  científica, revista científica, veículo de imprensa estabelecido). Nada de "dizem que" ou mito popular.
  Se o fato for um mito famoso, o vídeo só pode falar dele para desmentir. Na dúvida, cortar a frase.
- Imagens só com licença livre e crédito na descrição. Nada de imagem de banco pago, print de filme,
  logo de marca ou foto de pessoa comum identificável.
- Trilha gerada pelo próprio código (sem direitos autorais).
