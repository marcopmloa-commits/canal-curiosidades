"""Envia um Short ao YouTube.

Padrão: PRIVADO (aprovação manual no Studio). Opções:
  --publico                publica na hora como público
  --publicar-em DATAHORA   agenda a publicação (RFC3339, ex.: 2026-11-04T12:00:00-03:00);
                           o vídeo fica privado até esse horário e então vira público sozinho

Requer YT_CLIENT_ID, YT_CLIENT_SECRET e o refresh token, lido de YT_REFRESH_TOKEN_CURIOSIDADES
ou do arquivo indicado em --token.
Na descrição, acrescenta os créditos das imagens (campo "creditos" do roteiro), exigidos pelas licenças CC.

Uso: python3 youtube_upload.py roteiros/001_polvo.json saida/001_polvo [--token ARQUIVO]
     [--publico | --publicar-em DATAHORA]
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request


def opt(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def status():
    st = {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
    if "--publico" in sys.argv:
        st["privacyStatus"] = "public"
    elif opt("--publicar-em"):
        st["publishAt"] = opt("--publicar-em")  # exige privacyStatus private
    return st


def refresh_token():
    if opt("--token"):
        return open(opt("--token")).read().strip()
    return os.environ["YT_REFRESH_TOKEN_CURIOSIDADES"]


def descricao(script):
    d = script["descricao"]
    cred = script.get("creditos", [])
    if cred:
        d += "\n\nImagens:\n" + "\n".join(f"• {c}" for c in cred)
    return d[:5000]


def access_token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": refresh_token(), "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", data) as r:
        return json.load(r)["access_token"]


def call(req):
    try:
        with urllib.request.urlopen(req) as r:
            return r.headers, r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"Erro {e.code}: {e.read().decode()[:800]}")


def confere_canal(tok):
    """Trava: só envia se o token for do canal registrado em canal.json (evita postar no canal errado)."""
    esperado = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canal.json")
    req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
                                 headers={"Authorization": f"Bearer {tok}"})
    canal = json.loads(call(req)[1])["items"][0]
    if not os.path.exists(esperado):
        sys.exit(f"Falta canal.json. O token é do canal '{canal['snippet']['title']}' ({canal['id']}).")
    if canal["id"] != json.load(open(esperado))["id"]:
        sys.exit(f"Token do canal ERRADO ('{canal['snippet']['title']}'). Nada foi enviado.")
    print(f"Canal conferido: {canal['snippet']['title']}", flush=True)


def main():
    script = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    video = os.path.join(out, "short.mp4")
    thumb = os.path.join(out, "thumbnail.jpg")
    tok = access_token()
    confere_canal(tok)
    meta = {
        "snippet": {"title": script["titulo"][:100], "description": descricao(script),
                    "tags": script.get("tags", []), "categoryId": "27", "defaultLanguage": "pt-BR"},
        "status": status(),
    }
    size = os.path.getsize(video)
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        json.dumps(meta).encode(), method="POST", headers={
            "Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    upload_url = call(req)[0]["Location"]
    with open(video, "rb") as f:
        req = urllib.request.Request(upload_url, f.read(), method="PUT", headers={
            "Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
    vid = json.loads(call(req)[1])["id"]
    st = status()
    modo = f"AGENDADO para {st['publishAt']}" if "publishAt" in st else st["privacyStatus"].upper()
    print(f"Enviado ({modo}): https://youtu.be/{vid}", flush=True)
    if os.path.exists(thumb):
        req = urllib.request.Request(
            f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
            open(thumb, "rb").read(), method="POST",
            headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"})
        try:
            urllib.request.urlopen(req).close()
            print("Thumbnail definida.")
        except urllib.error.HTTPError as e:  # canais não verificados não podem usar thumbnail personalizada
            print(f"Thumbnail não aplicada ({e.code}): {e.read().decode()[:300]}")
    json.dump({"video_id": vid}, open(os.path.join(out, "youtube.json"), "w"))


if __name__ == "__main__":
    main()
