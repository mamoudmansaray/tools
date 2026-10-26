"""Run with Python 3. Only standard-library modules are used."""
from pathlib import Path
import csv, sqlite3, json, html
BASE=Path(__file__).resolve().parent
config=json.loads((BASE/'config.json').read_text())
with (BASE/'data.csv').open(newline='') as f:
    reader=csv.DictReader(f)
    assert reader.fieldnames==config['headers'], 'Unexpected headers'
    records=list(reader)
assert records, 'No source rows'
converted=[]
for row in records:
    assert None not in row, 'Unexpected extra CSV fields'
    converted.append(tuple(None if row[h]=='' else float(row[h]) if h in config['numeric'] else row[h] for h in config['headers']))
with sqlite3.connect(BASE/'project.db') as conn:
    conn.execute('DROP TABLE IF EXISTS data')
    fields=', '.join('"'+h+'" '+('REAL' if h in config['numeric'] else 'TEXT') for h in config['headers'])
    conn.execute('CREATE TABLE data ('+fields+')')
    conn.executemany('INSERT INTO data VALUES ('+','.join('?' for _ in config['headers'])+')',converted)
    assert conn.execute('SELECT COUNT(*) FROM data').fetchone()[0]==len(records)
    cursor=conn.execute((BASE/'analysis.sql').read_text())
    headers=[x[0] for x in cursor.description]
    output=cursor.fetchall()
with (BASE/'results.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(headers);writer.writerows(output)
label_index=headers.index(config['label']);metric_index=headers.index(config['metric'])
scale=max([abs(float(row[metric_index] or 0)) for row in output]+[1])
chart=''
for row in output:
    value=float(row[metric_index] or 0);width=round(abs(value)/scale*100,1)
    color='#ad3939' if value<0 else '#17687a'
    chart+=f'<div class="barrow"><b>{html.escape(str(row[label_index]))}</b><div class="track"><div style="width:{width}%;background:{color}"></div></div><span>{value:,.2f}</span></div>'
head=''.join('<th>'+html.escape(h)+'</th>' for h in headers)
body=''.join('<tr>'+''.join('<td>'+html.escape(str(v) if v is not None else 'Missing')+'</td>' for v in row)+'</tr>' for row in output)
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{font:16px Arial,sans-serif;max-width:1050px;margin:40px auto;padding:0 24px;color:#182c36;background:#f8fafb}}h1{{font-size:30px}}p{{line-height:1.6}}.panel{{background:white;padding:22px;margin:20px 0;border:1px solid #d6e1e5}}.barrow{{display:grid;grid-template-columns:180px 1fr 100px;align-items:center;gap:12px;margin:18px 0}}.track{{background:#e9eef0;height:22px}}.track div{{height:22px}}table{{width:100%;border-collapse:collapse}}td,th{{text-align:left;padding:12px;border-bottom:1px solid #ddd}}th{{background:#e9f1f4}}.scroll{{overflow:auto}}@media(max-width:600px){{.barrow{{grid-template-columns:110px 1fr 65px;font-size:12px}}}}</style><h1>{title}</h1><p>Synthetic data | Guided sample project</p><p>{question}</p><div class="panel"><h2>{metric}</h2>{chart}<p>Bar lengths show absolute magnitude. Negative values are red; read the signed values.</p></div><div class="panel scroll"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div><p>{limit}</p><p>Generated from data.csv by analyze.py and analysis.sql. Open README.md for the method, definitions, and Excel exercises.</p></html>'
page=page.format(title=html.escape(config['title']),question=html.escape(config['question']),metric=html.escape(config['metric']),chart=chart,head=head,body=body,limit=html.escape(config['limit']))
(BASE/'dashboard.html').write_text(page,encoding='utf-8')
print(f"Validated {len(records)} rows. Saved results.csv, project.db, dashboard.html.")
print(headers)
for row in output: print(row)
