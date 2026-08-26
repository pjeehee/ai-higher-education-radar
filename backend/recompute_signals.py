import sqlite3, os
DB=os.path.join(os.path.dirname(os.path.dirname(__file__)),"radar.db")
MAP={"Assessment Redesign":["AI in Assessment"],"AI Competency":["AI Curriculum & Competencies","Student AI Use & Literacy"],"Governance":["AI Policy & Governance"],"Institutional Transformation":["Institutional Transformation"],"Trust & Integrity":["Academic Integrity & Trust","AI Transparency & Trust"]}
c=sqlite3.connect(DB); cur=c.cursor()
for sig,topics in MAP.items():
 ph=','.join('?'*len(topics)); r=cur.execute(f"SELECT COUNT(*),COUNT(DISTINCT institution),COUNT(DISTINCT source_group),SUM(implementation_evidence) FROM evidence WHERE topic IN ({ph})",topics).fetchone(); n,i,f,impl=r[0],r[1],r[2],r[3] or 0; status='CORROBORATED' if f>=3 and i>=4 and impl>=2 else ('EMERGING' if f>=2 else 'SINGLE-STREAM'); score=min(100,n*2+i*4+f*8+impl*3); cur.execute("INSERT OR REPLACE INTO signals VALUES (?,?,?,?,?,?,?,datetime('now'))",(sig,n,i,f,impl,status,score))
c.commit(); c.close(); print('signals recomputed')
