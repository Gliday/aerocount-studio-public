from __future__ import annotations
import datetime as dt, requests
OPENALEX="https://api.openalex.org/works"
DEFAULT_QUERY="aerial wildlife survey OR oblique camera count OR animal detection aerial imagery"
TIMEOUT=25
def _abs(inv,limit=500):
    if not inv: return ""
    pos={}
    for w,ps in inv.items():
        for p in ps: pos[p]=w
    t=" ".join(pos[i] for i in sorted(pos))
    return (t[:limit]+"…") if len(t)>limit else t
def fetch_articles(query=DEFAULT_QUERY,per_page=25,since_days=1095,mailto="info@savetheelephants.org"):
    since=(dt.date.today()-dt.timedelta(days=since_days)).isoformat()
    p={"search":query,"sort":"publication_date:desc","per_page":max(1,min(per_page,50)),
       "filter":f"from_publication_date:{since}","mailto":mailto}
    r=requests.get(OPENALEX,params=p,timeout=TIMEOUT); r.raise_for_status()
    out=[]
    for w in r.json().get("results",[]):
        au=[a["author"]["display_name"] for a in w.get("authorships",[]) if a.get("author")]
        v=(w.get("primary_location") or {}).get("source") or {}
        out.append({"title":w.get("display_name") or "(untitled)","date":w.get("publication_date",""),
            "authors":", ".join(au[:4])+(" et al." if len(au)>4 else ""),
            "venue":v.get("display_name","") if v else "","doi":w.get("doi") or "",
            "oa_url":(w.get("open_access") or {}).get("oa_url") or "","abstract":_abs(w.get("abstract_inverted_index"))})
    return out
