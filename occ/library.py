from __future__ import annotations
import os, datetime as dt
def list_pdfs(folder):
    if not folder or not os.path.isdir(folder): return []
    items=[]
    for fn in os.listdir(folder):
        if fn.lower().endswith(".pdf"):
            path=os.path.join(folder,fn)
            try:
                s=os.stat(path)
                items.append({"name":fn,"path":path,"size_mb":round(s.st_size/1_000_000,2),
                    "modified":dt.datetime.fromtimestamp(s.st_mtime).strftime("%Y-%m-%d")})
            except OSError: pass
    return sorted(items,key=lambda x:x["name"].lower())
def read_pdf_bytes(path):
    with open(path,"rb") as f: return f.read()
