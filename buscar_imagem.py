"""Busca e baixa uma imagem que pode ser usada em vídeo monetizado, com o crédito pronto.

Uso: python3 buscar_imagem.py "termo em inglês" roteiros/img/<NNN_slug>/<nome>.jpg [opções]

  --fonte F  pixabay | openverse | commons | inaturalist | nasa | auto (padrão: auto)
  --listar   só mostra as opções encontradas, sem baixar
  --escolher N  baixa a opção N da lista (padrão: a primeira)

Fontes (em "auto", nesta ordem, pulando as que falharem):
  pixabay      fotos gerais (Pixabay License: uso comercial, sem crédito obrigatório). Precisa de PIXABAY_KEY.
  openverse    fotos gerais com CC0, domínio público, CC BY e CC BY-SA.
  commons      Wikimedia Commons, mesmas licenças.
  inaturalist  animais e plantas (fotos CC0, CC BY, CC BY-SA). Use o nome do bicho ("octopus").
  nasa         espaço e astronomia (domínio público da NASA).

Imprime a linha "CRÉDITO:" para o campo "creditos" do roteiro (obrigatória em CC BY e CC BY-SA).
Sempre abra a imagem baixada e confira se ela mostra mesmo o assunto.
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "CanalCuriosidadesBot/1.0 (github.com/marcopmloa-commits/canal-curiosidades)"}
LIVRES = {"cc0": "CC0", "pdm": "Domínio público", "by": "CC BY", "by-sa": "CC BY-SA"}


def get(url, tries=2, timeout=25):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(3)


def jget(url):
    return json.loads(get(url))


def grande(w, h):
    return (w or 0) >= 900 and (h or 0) >= 700


# Cada fonte devolve uma lista de dicts: url, credito, desc
def pixabay(q):
    key = os.environ.get("PIXABAY_KEY") or (open(os.path.expanduser("~/.pixabay_key")).read().strip()
                                            if os.path.exists(os.path.expanduser("~/.pixabay_key")) else None)
    if not key:
        raise RuntimeError("sem PIXABAY_KEY")
    p = urllib.parse.urlencode({"key": key, "q": q, "image_type": "photo", "per_page": 20, "safesearch": "true"})
    return [{"url": h["largeImageURL"], "desc": h.get("tags", ""),
             "credito": f"Foto de {h.get('user', 'autor')} no Pixabay: {h['pageURL']}"}
            for h in jget(f"https://pixabay.com/api/?{p}")["hits"] if grande(h["imageWidth"], h["imageHeight"])]


def openverse(q):
    p = urllib.parse.urlencode({"q": q, "page_size": 20})
    out = []
    for r in jget(f"https://api.openverse.org/v1/images/?{p}")["results"]:
        if r.get("license") in LIVRES and grande(r.get("width"), r.get("height")):
            lic = LIVRES[r["license"]] + (f" {r['license_version']}" if r["license"] in ("by", "by-sa") else "")
            out.append({"url": r["url"], "desc": r.get("title", ""),
                        "credito": f"{r.get('title') or 'Imagem'} — {r.get('creator') or 'autor desconhecido'} "
                                   f"({lic}), via {r.get('source')}: {r['foreign_landing_url']}"})
    return out


def commons(q):
    p = urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
                                "gsrsearch": f"{q} filetype:bitmap", "gsrlimit": 20, "prop": "imageinfo",
                                "iiprop": "url|size|extmetadata", "iiurlwidth": 1600})
    out = []
    for pg in jget(f"https://commons.wikimedia.org/w/api.php?{p}").get("query", {}).get("pages", {}).values():
        ii = pg["imageinfo"][0]
        m = {k: v.get("value", "") for k, v in ii.get("extmetadata", {}).items()}
        lic = m.get("LicenseShortName", "")
        if not re.match(r"(CC0|Public domain|PD|CC BY(-SA)? [\d.]+$)", lic, re.I) or not grande(ii["width"], ii["height"]):
            continue
        autor = re.sub("<[^>]+>", "", m.get("Artist", "")).strip() or "autor desconhecido"
        out.append({"url": ii.get("thumburl") or ii["url"], "desc": pg["title"],
                    "credito": f"{pg['title'][5:]} — {autor} ({lic}), via Wikimedia Commons: {ii['descriptionurl']}"})
    return out


def inaturalist(q):
    p = urllib.parse.urlencode({"q": q, "per_page": 1})
    taxa = jget(f"https://api.inaturalist.org/v1/taxa?{p}")["results"]
    if not taxa:
        return []
    t = taxa[0]
    p = urllib.parse.urlencode({"taxon_id": t["id"], "photo_license": "cc0,cc-by,cc-by-sa", "quality_grade": "research",
                                "order_by": "votes", "per_page": 30})
    out = []
    for o in jget(f"https://api.inaturalist.org/v1/observations?{p}")["results"]:
        for ph in o.get("photos", [])[:1]:
            dims = ph.get("original_dimensions") or {}
            if ph.get("license_code") not in ("cc0", "cc-by", "cc-by-sa") or not grande(dims.get("width"), dims.get("height")):
                continue
            out.append({"url": ph["url"].replace("square", "large"), "desc": f"{t['name']} ({o.get('place_guess', '')})",
                        "credito": f"{t.get('preferred_common_name') or t['name']} — {ph.get('attribution', '')}, "
                                   f"via iNaturalist: https://www.inaturalist.org/photos/{ph['id']}"})
    return out


def nasa(q):
    p = urllib.parse.urlencode({"q": q, "media_type": "image"})
    out = []
    for it in jget(f"https://images-api.nasa.gov/search?{p}")["collection"]["items"][:20]:
        d = it["data"][0]
        links = it.get("links", [])
        if not links:
            continue
        nid = d["nasa_id"]
        out.append({"url": links[0]["href"].replace("~thumb", "~large"), "desc": d.get("title", ""),
                    "credito": f"{d.get('title', 'Imagem')} — NASA (domínio público): https://images.nasa.gov/details/{nid}"})
    return out


FONTES = {"pixabay": pixabay, "openverse": openverse, "commons": commons, "inaturalist": inaturalist, "nasa": nasa}


def main():
    termo, destino = sys.argv[1], sys.argv[2]
    arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
    fonte = arg("--fonte", "auto")
    ordem = list(FONTES) if fonte == "auto" else [fonte]
    for nome in ordem:
        try:
            ops = FONTES[nome](termo)
        except Exception as e:
            print(f"[{nome}] indisponível: {e}", file=sys.stderr)
            continue
        if not ops:
            print(f"[{nome}] nada encontrado", file=sys.stderr)
            continue
        if "--listar" in sys.argv:
            print(f"[{nome}]")
            for i, o in enumerate(ops):
                print(f"  {i}: {o['desc'][:70]}")
            return
        escolha = int(arg("--escolher", 0))
        for o in ops[escolha:]:
            try:
                from PIL import Image
                im = Image.open(io.BytesIO(get(o["url"], timeout=40))).convert("RGB")
            except Exception as e:
                print(f"[{nome}] falhou ao baixar: {e}", file=sys.stderr)
                continue
            os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
            im.thumbnail((2000, 2000))
            im.save(destino, quality=92)
            print(f"Salvo: {destino} ({im.width}x{im.height}) [{nome}] {o['desc'][:60]}")
            print(f"CRÉDITO: {o['credito']}")
            return
    sys.exit("Nenhuma fonte trouxe imagem. Tente outro termo (em inglês) ou outra fonte.")


if __name__ == "__main__":
    main()
