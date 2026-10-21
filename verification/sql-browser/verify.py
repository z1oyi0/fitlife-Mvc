"""Exercise the UNMODIFIED course application against a disposable SQL Server.
Only synthetic fixtures are used. Failed checks are retained, not hidden.
This script is AI-assisted verification added after the original coursework.
"""
from __future__ import annotations
import datetime as dt
import json
import os
import re
import sys
import traceback
from pathlib import Path
from urllib.parse import urlencode

import pymssql
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:5080'
DATABASE = 'FitLifeVerification'
OUT = Path('validation-artifacts')
OUT.mkdir(exist_ok=True)
RESULTS: list[dict] = []
ERRORS: list[str] = []
META = {'source_commit': os.environ.get('GITHUB_SHA', ''),
        'application_baseline': '906de25d73f2d13dcc2e9c1e676faa930ff3cfd5',
        'tested_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'database': DATABASE, 'data': 'synthetic fixtures only',
        'application_changes': False, 'production_deployment': False}


def write_results():
    counts = {k: sum(x['status'] == k for x in RESULTS) for k in ['PASS', 'FAIL', 'ERROR']}
    data = {'environment': META, 'counts': counts, 'checks': RESULTS,
            'browser_errors': ERRORS, 'not_tested': [
                'Original school/production SQL Server and its original schema/data',
                'Production deployment, TLS, real accounts, multi-user isolation',
                'Full security audit, penetration testing, load/performance testing',
                'Firefox/WebKit/mobile compatibility and credential rotation']}
    (OUT / 'results.json').write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    lines = ['# FitLife SQL Server 與瀏覽器驗證', '',
             f"測試版本：`{META['source_commit']}`", '',
             '使用隔離 SQL Server 與人工建立的測試資料。應用程式保持不變；未正式部署。', '',
             f"PASS {counts['PASS']} / FAIL {counts['FAIL']} / ERROR {counts['ERROR']}", '',
             '|分類|檢查|結果|預期|實際|', '|---|---|---|---|---|']
    def cell(x):
        return str(x).replace('|', '/').replace('\n', ' ')[:800]
    for r in RESULTS:
        lines.append('|' + '|'.join(cell(r[k]) for k in ['category', 'name', 'status', 'expected', 'actual']) + '|')
    lines += ['', 'FAIL 表示此測試的品質／安全預期未滿足；ERROR 表示檢查未能完成，不能當成通過。',
              '一般 CRUD 通過不等於權限與安全性合格；查詢及圖表只驗證本次測試資料範圍。',
              '部署、安全性全面審查及原始資料庫均不在本次驗證範圍。', '',
              '測試程式與文件使用 AI 協助建立，並非原課程開發當時的除錯歷程。']
    (OUT / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def record(category, name, passed, expected, actual):
    r = dict(category=category, name=name, status='PASS' if passed else 'FAIL', expected=expected, actual=actual)
    RESULTS.append(r)
    print(json.dumps(r, ensure_ascii=False, default=str), flush=True)
    write_results()


def scenario(name, func):
    try:
        func()
    except Exception as exc:
        RESULTS.append(dict(category='execution', name=name, status='ERROR',
                            expected='scenario completes', actual=f'{type(exc).__name__}: {str(exc)[:700]}'))
        print(f'ERROR in {name}: {type(exc).__name__}: {exc}', flush=True)
        traceback.print_exc()
        write_results()


conn = pymssql.connect(server='127.0.0.1', port=1433, user='sa',
                       password=os.environ['MSSQL_SA_PASSWORD'], database=DATABASE,
                       login_timeout=15, timeout=20, charset='UTF-8', as_dict=True, autocommit=True)


def query(text, params=()):
    with conn.cursor() as c:
        c.execute(text, params)
        return c.fetchall() if c.description else []


def reset():
    name = query('SELECT DB_NAME() AS name')[0]['name']
    if name != DATABASE:
        raise RuntimeError('Refusing to modify a non-test database')
    query('TRUNCATE TABLE dbo.TableMealRecords1132024')
    query('TRUNCATE TABLE dbo.TableExerciseRecords1132024')


def meal_rows():
    return query('SELECT * FROM dbo.TableMealRecords1132024 ORDER BY Id')


def exercise_rows():
    return query('SELECT * FROM dbo.TableExerciseRecords1132024 ORDER BY Id')


def seed_meal(name, mealtype, calories, note, day='2026-10-20'):
    query('INSERT dbo.TableMealRecords1132024 (MealName,MealType,MealDate,Calories,Note) VALUES (%s,%s,%s,%s,%s)',
          (name, mealtype, day, calories, note))


def seed_exercise(name, calories, day='2026-10-20', duration=30):
    query('INSERT dbo.TableExerciseRecords1132024 (ExerciseName,ExerciseDate,Duration,Calories,Note) VALUES (%s,%s,%s,%s,%s)',
          (name, day, duration, calories, '僅供測試'))


version = query('SELECT DB_NAME() AS name, @@VERSION AS version')[0]
META['sql_server'] = version['version']
record('database', 'SQL Server 真實連線與測試資料庫', version['name'] == DATABASE, DATABASE, version['name'])

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    META['browser'] = browser.version
    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, locale='zh-TW', timezone_id='Asia/Taipei')
    page = context.new_page()
    page.on('pageerror', lambda err: ERRORS.append(str(err)))
    page.set_default_timeout(20000)
    anonymous = pw.request.new_context(base_url=BASE)
    cdn = []
    page.on('response', lambda r: cdn.append({'url': r.url, 'status': r.status}) if 'cdn.jsdelivr.net/npm/chart.js' in r.url else None)

    def go(path):
        return page.goto(BASE + path, wait_until='networkidle', timeout=45000)

    def screenshot(name):
        page.screenshot(path=str(OUT / name), full_page=True, animations='disabled')

    def submit():
        with page.expect_navigation(wait_until='networkidle', timeout=45000):
            page.locator('button[type="submit"]').click()

    def ids():
        return [int(re.search(r'/Edit/(\d+)', x).group(1)) for x in page.locator('tbody a[href*="/Edit/"]').evaluate_all('(els) => els.map(e => e.getAttribute("href"))')]

    go('/Login/Index')
    page.locator('[name="username"]').fill('admin')
    page.locator('[name="password"]').fill('1234')
    submit()
    record('functional', '示範登入與首頁', '/Home' in page.url, 'redirect to Home', page.url)
    screenshot('01-home.png')

    def meals_crud():
        reset()
        go('/MealRecords/Create')
        page.locator('[name="MealName"]').fill('測試雞肉飯')
        page.locator('[name="MealType"]').select_option('午餐')
        page.locator('[name="MealDate"]').fill('2026-10-20')
        page.locator('[name="Calories"]').fill('450')
        page.locator('[name="Note"]').fill('自動化測試資料')
        screenshot('02-meal-create.png')
        submit()
        rows = meal_rows()
        ok = len(rows) == 1 and rows[0]['MealName'] == '測試雞肉飯' and rows[0]['MealType'] == '午餐' and rows[0]['Calories'] == 450 and rows[0]['MealDate'].date().isoformat() == '2026-10-20'
        record('functional', '飲食新增：瀏覽器表單寫入 SQL Server', ok, '1 row, 午餐, 450 kcal, 2026-10-20', rows)
        rid = rows[0]['Id']
        record('functional', '飲食查詢：畫面對回資料庫', ids() == [rid] and '測試雞肉飯' in page.locator('tbody').inner_text(), [rid], ids())
        screenshot('03-meal-list.png')
        go(f'/MealRecords/Edit/{rid}')
        selected = page.locator('[name="MealType"]').input_value()
        record('quality', '編輯表單保留原餐別', selected == '午餐', '午餐', selected)
        screenshot('04-meal-edit.png')
        page.locator('[name="MealName"]').fill('測試修改後餐點')
        page.locator('[name="MealType"]').select_option('晚餐')
        page.locator('[name="MealDate"]').fill('2026-10-21')
        page.locator('[name="Calories"]').fill('525')
        page.locator('[name="Note"]').fill('已修改')
        submit()
        row = meal_rows()[0]
        record('functional', '飲食修改：資料庫值與表單一致', row['MealName'] == '測試修改後餐點' and row['Calories'] == 525 and row['MealType'] == '晚餐' and row['Note'] == '已修改', 'name, type, calories, note updated', row)
        go('/MealRecords')
        record('functional', '飲食修改後重新查詢', '測試修改後餐點' in page.locator('tbody').inner_text() and '525 kcal' in page.locator('tbody').inner_text(), 'updated row in view', page.locator('tbody').inner_text())
        page.locator(f'a[href="/MealRecords/Delete/{rid}"]').click()
        page.wait_for_load_state('networkidle')
        record('functional', '飲食刪除：資料庫及清單均移除', not meal_rows() and page.locator('tbody tr').count() == 0, 'no rows', meal_rows())

    def exercises_crud():
        reset()
        go('/ExerciseRecords/Create')
        for key, value in {'ExerciseName':'測試慢跑', 'ExerciseDate':'2026-10-20', 'Duration':'30', 'Calories':'240', 'Note':'自動化測試資料'}.items():
            page.locator(f'[name="{key}"]').fill(value)
        submit()
        rows = exercise_rows()
        record('functional', '運動新增：瀏覽器表單寫入 SQL Server', len(rows) == 1 and rows[0]['Calories'] == 240 and rows[0]['Duration'] == 30, '1 row, 30 minutes, 240 kcal', rows)
        rid = rows[0]['Id']
        record('functional', '運動查詢：畫面對回資料庫', ids() == [rid] and '測試慢跑' in page.locator('tbody').inner_text(), [rid], ids())
        go(f'/ExerciseRecords/Edit/{rid}')
        for key, value in {'ExerciseName':'測試快走', 'Duration':'45', 'Calories':'310', 'Note':'已修改'}.items():
            page.locator(f'[name="{key}"]').fill(value)
        submit()
        row = exercise_rows()[0]
        record('functional', '運動修改：資料庫值與表單一致', row['ExerciseName'] == '測試快走' and row['Duration'] == 45 and row['Calories'] == 310, '快走, 45, 310', row)
        go('/ExerciseRecords')
        record('functional', '運動修改後重新查詢', '測試快走' in page.locator('tbody').inner_text() and '310 kcal' in page.locator('tbody').inner_text(), 'updated row in view', page.locator('tbody').inner_text())
        page.locator(f'a[href="/ExerciseRecords/Delete/{rid}"]').click()
        page.wait_for_load_state('networkidle')
        record('functional', '運動刪除：資料庫及清單均移除', not exercise_rows() and page.locator('tbody tr').count() == 0, 'no rows', exercise_rows())

    def meal_queries():
        reset()
        for i in range(1, 9):
            seed_meal(f'測試餐點{i:02}', '午餐' if i % 2 else '晚餐', i * 100, '標籤A' if i <= 6 else '標籤B')
        rows = meal_rows()
        go('/MealRecords')
        first = ids()
        visible_sum = sum(r['Calories'] for r in rows if r['Id'] in first)
        text = page.locator('h5 strong').inner_text()
        actual_sum = int(re.search(r'-?\d+', text).group())
        record('functional', '飲食目前頁面熱量加總', actual_sum == visible_sum, visible_sum, actual_sum)
        go('/MealRecords?pageNumber=2')
        second = ids()
        record('functional', '飲食基本分頁：5+3 筆且不重複', len(first) == 5 and len(second) == 3 and not set(first) & set(second) and set(first + second) == {r['Id'] for r in rows}, '5 + 3, no overlap, complete set', {'page1': first, 'page2': second})
        for label, term, field in [('名稱', '餐點03', 'MealName'), ('餐別', '晚餐', 'MealType'), ('備註', '標籤B', 'Note'), ('無結果', 'NOT_FOUND_XYZ', 'MealName')]:
            go('/MealRecords?' + urlencode({'searchText': term}))
            expected = sorted(r['Id'] for r in rows if term in (r[field] or ''))
            record('functional', '飲食條件查詢－' + label, sorted(ids()) == expected, expected, sorted(ids()))
        go('/MealRecords?' + urlencode({'searchText':'標籤A', 'pageNumber': 2}))
        direct = ids()
        record('functional', '直接指定查詢＋第二頁', len(direct) == 1 and all(rows[i-1]['Note'] == '標籤A' for i in direct), '1 matching row', direct)
        go('/MealRecords?' + urlencode({'searchText':'標籤A'}))
        page.get_by_role('link', name='下一頁', exact=True).click()
        page.wait_for_load_state('networkidle')
        actual = ids()
        record('quality', '查詢後按下一頁保留篩選條件', len(actual) == 1 and all(rows[i-1]['Note'] == '標籤A' for i in actual), 'only remaining 1 matching row', {'url':page.url, 'ids':actual})
        screenshot('05-query-pagination.png')
        response = go('/MealRecords?pageNumber=0')
        record('quality', '不合理頁碼不造成伺服器錯誤', response.status < 500, 'no HTTP 5xx', response.status)

    def charts():
        reset()
        for name, calories, day in [('測試快走',180,'2026-10-19'), ('測試慢跑',260,'2026-10-20'), ('測試騎車',320,'2026-10-21')]:
            seed_exercise(name, calories, day)
        sql_rows = exercise_rows()
        before = len(ERRORS)
        go('/ExerciseRecords')
        page.wait_for_function("typeof Chart !== 'undefined' && !!Chart.getChart('exerciseChart')", timeout=30000)
        page.wait_for_timeout(1500)
        chart = page.evaluate("""() => { const c = Chart.getChart('exerciseChart'); const canvas = c.canvas; const pixels = c.ctx.getImageData(0,0,canvas.width,canvas.height).data; return {labels:c.data.labels, values:Array.from(c.data.datasets[0].data), type:c.config.type, width:canvas.width, height:canvas.height, hasPixels:Array.from(pixels).some((v,i)=>i%4===3 && v>0), version:Chart.version}; }""")
        META['chart_js'] = chart['version']
        expected = [(r['ExerciseDate'].strftime('%m/%d'), r['Calories']) for r in sql_rows]
        actual = list(zip(chart['labels'], chart['values']))
        record('browser', 'Chart.js 數值及日期與 SQL Server 一致', sorted(actual) == sorted(expected), expected, actual)
        record('browser', 'Chart.js 真實 canvas 繪製', chart['type'] == 'line' and chart['width'] > 0 and chart['height'] > 0 and chart['hasPixels'], 'line + visible nonempty canvas', chart)
        record('browser', 'Chart.js 頁面無 JavaScript 例外', len(ERRORS) == before, 'no new pageerror', ERRORS[before:])
        screenshot('06-exercise-chart.png')
        record('browser', '操作截圖已產生', (OUT / '06-exercise-chart.png').stat().st_size > 1000, 'actual browser PNG > 1000 bytes', (OUT / '06-exercise-chart.png').stat().st_size)
        go('/ExerciseRecords?' + urlencode({'searchText': '慢跑'}))
        page.wait_for_function("typeof Chart !== 'undefined' && !!Chart.getChart('exerciseChart')")
        filtered = page.evaluate("() => ({labels:Chart.getChart('exerciseChart').data.labels, values:Chart.getChart('exerciseChart').data.datasets[0].data})")
        record('functional', '運動查詢結果與圖表同步', len(ids()) == 1 and filtered['values'] == [260] and filtered['labels'] == ['10/20'], {'values':[260], 'labels':['10/20']}, filtered)
        go('/ExerciseRecords?' + urlencode({'searchText':'NOT_FOUND_XYZ'}))
        page.wait_for_function("typeof Chart !== 'undefined' && !!Chart.getChart('exerciseChart')")
        empty = page.evaluate("() => ({labels:Chart.getChart('exerciseChart').data.labels, values:Chart.getChart('exerciseChart').data.datasets[0].data})")
        record('browser', '空查詢結果可呈現空圖表', ids() == [] and empty['labels'] == [] and empty['values'] == [], 'empty rows and arrays', empty)
        META['chart_cdn_responses'] = cdn

    def security_and_validation():
        reset()
        seed_meal('測試權限資料', '午餐', 300, 'synthetic')
        response = anonymous.get(BASE + '/MealRecords')
        record('security', '未登入不可讀取資料清單', response.status in [401,403] or '/Login' in response.url, 'login or 401/403', {'status':response.status, 'data_visible':'測試權限資料' in response.text()})
        response = anonymous.post(BASE + '/MealRecords/Create', form={'MealName':'UNAUTH_WRITE','MealType':'午餐','Calories':'11'})
        created = query('SELECT COUNT(*) AS n FROM dbo.TableMealRecords1132024 WHERE MealName=%s', ('UNAUTH_WRITE',))[0]['n']
        record('security', '未登入不可新增資料', created == 0, 'no row inserted', {'inserted':created, 'status':response.status})
        rid = meal_rows()[0]['Id']
        response = anonymous.get(BASE + f'/MealRecords/Delete/{rid}')
        still_exists = query('SELECT COUNT(*) AS n FROM dbo.TableMealRecords1132024 WHERE Id=%s', (rid,))[0]['n']
        record('security', '未登入 GET 不可刪除資料', still_exists == 1, 'row preserved', {'row_exists':still_exists, 'status':response.status})
        context.request.post(BASE + '/MealRecords/Create', form={'MealName':'NO_CSRF_TOKEN','Calories':'12'})
        n = query('SELECT COUNT(*) AS n FROM dbo.TableMealRecords1132024 WHERE MealName=%s', ('NO_CSRF_TOKEN',))[0]['n']
        record('security', '資料變更需驗證防偽權杖', n == 0, 'no-token request rejected', {'inserted_without_token':n})
        context.request.post(BASE + '/MealRecords/Create', form={'MealName':'NEGATIVE_CALORIES','Calories':'-10'})
        n = query('SELECT COUNT(*) AS n FROM dbo.TableMealRecords1132024 WHERE MealName=%s AND Calories<0', ('NEGATIVE_CALORIES',))[0]['n']
        record('validation', '建議規則：熱量不可負數', n == 0, 'negative value rejected', {'negative_rows':n})
        context.request.post(BASE + '/MealRecords/Create', form={'MealName':'INVALID_NUMBER','Calories':'not-a-number'})
        n = query('SELECT COUNT(*) AS n FROM dbo.TableMealRecords1132024 WHERE MealName=%s', ('INVALID_NUMBER',))[0]['n']
        record('validation', '無效數字不可靜默寫入', n == 0, 'invalid numeric input rejected', {'inserted':n})
        reset()
        payload = '<script>window.fitlifeXssProbe=1</script>'
        context.request.post(BASE + '/MealRecords/Create', form={'MealName':'HTML_ESCAPE_TEST','Calories':'100','Note':payload})
        go('/MealRecords')
        probe = page.evaluate('window.fitlifeXssProbe || null')
        record('security', '一般備註 HTML 由 Razor 編碼', probe is None and payload in page.locator('tbody').inner_text(), 'text visible, script not executed', {'probe':probe, 'literal_text':payload in page.locator('tbody').inner_text()})

    for name, fn in [('meal CRUD',meals_crud), ('exercise CRUD',exercises_crud), ('meal queries',meal_queries), ('charts',charts), ('security and validation',security_and_validation)]:
        scenario(name, fn)
    write_results()
    anonymous.dispose()
    context.close()
    browser.close()
conn.close()
failed = sum(r['status'] != 'PASS' for r in RESULTS)
print(f'FINAL: {len(RESULTS)-failed} passed; {failed} failed/errors; {len(RESULTS)} checks', flush=True)
sys.exit(1 if failed else 0)
