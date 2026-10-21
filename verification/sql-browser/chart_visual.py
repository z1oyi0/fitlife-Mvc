"""Read actual chart geometry and compare screenshot modes; do not modify app/CSS."""
import base64
import html
import json
import os
from pathlib import Path
import pymssql
from playwright.sync_api import sync_playwright

out = Path('validation-artifacts')
out.mkdir(exist_ok=True)
conn = pymssql.connect(server='127.0.0.1', port=1433, user='sa', password=os.environ['MSSQL_SA_PASSWORD'], database='FitLifeVerification', charset='UTF-8', autocommit=True)
with conn.cursor() as c:
    c.execute('SELECT DB_NAME()')
    assert c.fetchone()[0] == 'FitLifeVerification'
    c.execute('TRUNCATE TABLE dbo.TableExerciseRecords1132024')
    for name, day, calories in [('測試快走','2026-10-19',180),('測試慢跑','2026-10-20',260),('測試騎車','2026-10-21',320)]:
        c.execute('INSERT dbo.TableExerciseRecords1132024 (ExerciseName,ExerciseDate,Duration,Calories,Note) VALUES (%s,%s,%s,%s,%s)', (name,day,30,calories,'僅供測試'))
    c.execute('TRUNCATE TABLE dbo.TableMealRecords1132024')
    c.execute('INSERT dbo.TableMealRecords1132024 (MealName,MealType,MealDate,Calories,Note) VALUES (%s,%s,%s,%s,%s)', ('測試權限資料','午餐','2026-10-20',300,'僅供測試'))
conn.close()
script = """() => {const c=Chart.getChart('exerciseChart'), e=c.canvas, r=e.getBoundingClientRect(), p=e.parentElement.getBoundingClientRect(), s=getComputedStyle(e); return {rect:{x:r.x,y:r.y,width:r.width,height:r.height}, parent:{width:p.width,height:p.height}, attributes:{width:e.width,height:e.height}, css:{width:s.width,height:s.height,display:s.display}, chart:{width:c.width,height:c.height,labels:c.data.labels,values:Array.from(c.data.datasets[0].data)}, dpr:devicePixelRatio};}"""
records=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    ctx=browser.new_context(viewport={'width':1440,'height':1000},locale='zh-TW',timezone_id='Asia/Taipei')
    ctx.request.post('http://127.0.0.1:5080/Login/Index', form={'username':'admin','password':'1234'})
    for mode, full, animation in [('viewport-allow',False,'allow'),('fullpage-allow',True,'allow'),('fullpage-disabled',True,'disabled')]:
        page=ctx.new_page()
        page.goto('http://127.0.0.1:5080/ExerciseRecords',wait_until='networkidle')
        page.wait_for_function("typeof Chart !== 'undefined' && !!Chart.getChart('exerciseChart')")
        samples=[]
        for _ in range(3):
            page.wait_for_timeout(1000)
            samples.append(page.evaluate(script))
        dataurl=page.locator('#exerciseChart').evaluate("e => e.toDataURL('image/png')")
        (out / ('chart-canvas-'+mode+'.png')).write_bytes(base64.b64decode(dataurl.split(',',1)[1]))
        page.screenshot(path=str(out / ('chart-'+mode+'.png')),full_page=full,animations=animation)
        page.wait_for_timeout(400)
        after=page.evaluate(script)
        rect_ok=all(s['rect']['width']>=600 and s['rect']['height']>=250 for s in samples+[after])
        records.append({'mode':mode,'samples_before_screenshot':samples,'after_screenshot':after,'geometry_check':rect_ok})
        page.close()
    anon=pw.request.new_context()
    r=anon.get('http://127.0.0.1:5080/MealRecords')
    anonymous_result={'status':r.status,'final_url':r.url,'synthetic_record_visible_after_html_decode':'測試權限資料' in html.unescape(r.text())}
    anon.dispose()
    ctx.close()
    browser.close()
result={'application_modified':False,'cases':records,'anonymous_read_followup':anonymous_result,'note':'Screenshot modes are compared without application or stylesheet changes. Geometry checks do not by themselves establish screenshot readability; inspect PNGs.'}
(out/'chart-visual-diagnostic.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
