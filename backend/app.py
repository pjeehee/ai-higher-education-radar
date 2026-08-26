from flask import Flask, jsonify, request, send_from_directory
import sqlite3, os
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
 return jsonify({"evidence":q("SELECT COUNT(*) n FROM evidence")[0]["n"],"institutions":q("SELECT COUNT(DISTINCT institution) n FROM evidence")[0]["n"],"topics":q("SELECT COUNT(DISTINCT topic) n FROM evidence")[0]["n"],"implementation":q("SELECT COUNT(*) n FROM evidence WHERE implementation_evidence=1")[0]["n"]})
@app.get("/")
def root(): return send_from_directory(app.static_folder,"index.html")
@app.get("/health")
def health(): return jsonify({"status":"ok"})
if __name__=="__main__":
 app.run(host="0.0.0.0", port=int(os.environ.get("PORT","8787")), debug=False)
