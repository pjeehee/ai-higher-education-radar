from flask import Flask, jsonify, request, send_from_directory, Response
import sqlite3, os, json
ROOT=os.path.dirname(os.path.dirname(__file__))
DB=os.environ.get("RADAR_DB_PATH", os.path.join(ROOT,"radar.db"))
app=Flask(__name__, static_folder=os.path.join(ROOT,"web"), static_url_path="")
def q(sql,args=()):
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; r=[dict(x) for x in c.execute(sql,args).fetchall()]; c.close(); return r
@app.get("/api/evidence")
def evidence():
 term=request.args.get("q","").strip(); topic=request.args.get("topic","").strip(); sql="SELECT * FROM evidence WHERE 1=1"; a=[]
 if term: sql+=" AND (institution LIKE ? OR title LIKE ? OR fact LIKE ?)"; a += [f"%{term}%"]*3
 if topic: sql+=" AND topic=?"; a.append(topic)
 return jsonify(q(sql+" ORDER BY evidence_date DESC",a))
@app.get("/api/stats")
def stats():
 groups=q("""SELECT source_group name, COUNT(*) n
             FROM evidence WHERE status!='deleted'
             GROUP BY source_group ORDER BY n DESC, name""")
 top_inst=q("""SELECT institution name, COUNT(*) n
              FROM evidence WHERE status!='deleted'
              GROUP BY institution ORDER BY n DESC, name LIMIT 1""")
 top_group=groups[:1]
 return jsonify({
  "evidence":q("SELECT COUNT(*) n FROM evidence WHERE status!='deleted'")[0]["n"],
  "institutions":q("SELECT COUNT(DISTINCT institution) n FROM evidence WHERE status!='deleted'")[0]["n"],
  "topics":q("SELECT COUNT(DISTINCT topic) n FROM evidence WHERE status!='deleted'")[0]["n"],
  "implementation":q("SELECT COUNT(*) n FROM evidence WHERE implementation_evidence=1 AND status!='deleted'")[0]["n"],
  "as_of":q("SELECT MAX(evidence_date) d FROM evidence WHERE status!='deleted'")[0]["d"],
  "top_institution": top_inst[0] if top_inst else {"name":"—","n":0},
  "top_source_family": top_group[0] if top_group else {"name":"—","n":0},
  "source_groups":groups,
  "build":"source-clean-v4"
 })
@app.get("/")
def root():
 path=os.path.join(app.static_folder,"index.html")
 with open(path,"r",encoding="utf-8") as f: page=f.read()
 records=q("""SELECT id, institution, source_group, topic, title, evidence_date, year, fact, why, url,
                    evidence_type, importance, verification_status, evidence_class, source_authority,
                    authority_score, implementation_evidence, confidence_score, confidence_label, status
             FROM evidence WHERE status!='deleted' ORDER BY evidence_date DESC, id""")
 mapped=[]
 for x in records:
  mapped.append({"record_id":x["id"],"institution":x["institution"],"group":x["source_group"],"topic":x["topic"],
   "title":x["title"],"date":x["evidence_date"],"year":x["year"],"fact":x["fact"],"why":x["why"],
   "url":x["url"],"type":x["evidence_type"],"importance":x["importance"],
   "verification_status":x["verification_status"],"evidence_class":x["evidence_class"],
   "source_authority":x["source_authority"],"authority_score":x["authority_score"],
   "implementation_evidence":bool(x["implementation_evidence"]),"confidence_score":x["confidence_score"],
   "confidence_label":x["confidence_label"],"status":x["status"]})
 payload=json.dumps(mapped,ensure_ascii=False)
 page=page.replace("__RADAR_EVIDENCE__",payload)
 stats=q("""SELECT COUNT(*) n, MAX(evidence_date) as_of FROM evidence WHERE status!='deleted'""")[0]
 top_inst=q("""SELECT institution name, COUNT(*) n FROM evidence WHERE status!='deleted'
              GROUP BY institution ORDER BY n DESC, name LIMIT 1""")
 groups=q("""SELECT source_group name, COUNT(*) n FROM evidence WHERE status!='deleted'
             GROUP BY source_group ORDER BY n DESC, name""")
 top_group=groups[:1]
 page=page.replace("__DB_EVIDENCE_COUNT__",str(stats["n"]))
 page=page.replace("__DB_AS_OF__",stats["as_of"] or "—")
 page=page.replace("__TOP_INSTITUTION_COUNT__",str(top_inst[0]["n"] if top_inst else 0))
 page=page.replace("__TOP_INSTITUTION_NAME__",top_inst[0]["name"] if top_inst else "—")
 page=page.replace("__TOP_SOURCE_FAMILY_COUNT__",str(top_group[0]["n"] if top_group else 0))
 page=page.replace("__TOP_SOURCE_FAMILY_NAME__",top_group[0]["name"] if top_group else "—")
 dist=[]
 for g in groups:
  pct=round((g["n"]/stats["n"])*100) if stats["n"] else 0
  dist.append(f'<div class="sideitem"><b>{g["name"]}</b><small>{g["n"]}건 · {pct}%</small></div>')
 page=page.replace("__SOURCE_GROUP_DISTRIBUTION__","".join(dist))
 resp=Response(page,mimetype="text/html")
 resp.headers["Cache-Control"]="no-store, no-cache, must-revalidate, max-age=0"
 resp.headers["Pragma"]="no-cache"
 resp.headers["Expires"]="0"
 resp.headers["X-Radar-Build"]="source-clean-v4"
 return resp
@app.get("/health")
def health(): return jsonify({"status":"ok","build":"source-clean-v4"})
if __name__=="__main__":
 app.run(host="0.0.0.0", port=int(os.environ.get("PORT","8787")), debug=False)
