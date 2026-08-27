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
 return jsonify({
  "evidence":q("SELECT COUNT(*) n FROM evidence WHERE status!='deleted'")[0]["n"],
  "institutions":q("SELECT COUNT(DISTINCT institution) n FROM evidence WHERE status!='deleted'")[0]["n"],
  "topics":q("SELECT COUNT(DISTINCT topic) n FROM evidence WHERE status!='deleted'")[0]["n"],
  "implementation":q("SELECT COUNT(*) n FROM evidence WHERE implementation_evidence=1 AND status!='deleted'")[0]["n"],
  "as_of":q("SELECT date(MAX(ingested_at)) d FROM evidence")[0]["d"]
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
 page=page.replace("__DB_EVIDENCE_COUNT__",str(stats["n"]))
 page=page.replace("__DB_AS_OF__",stats["as_of"] or "—")
 return Response(page,mimetype="text/html")
@app.get("/health")
def health(): return jsonify({"status":"ok"})
if __name__=="__main__":
 app.run(host="0.0.0.0", port=int(os.environ.get("PORT","8787")), debug=False)
