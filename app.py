from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import date, datetime

app = Flask(__name__)

load_dotenv()

supabaseUrl = os.getenv("SUPABASE_URL")
supabaseKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabaseUrl, supabaseKey)

@app.route('/')
def index():
    today = date.today()

    bd = supabase.table("birthday").select("name", "date").eq("date", today.isoformat()).execute()
    bdName = [item['name'] for item in bd.data] if bd.data else []

    # performance 테이블에서 subject와 date 가져오기
    perf = supabase.table("performance").select("subject,date").execute()
    perf_list = perf.data or []

    # dday별로 과목 그룹화 (0 <= dday <= 7)
    dday_groups: dict[int, list[str]] = {}
    for item in perf_list:
        dstr = item.get("date")
        subj = item.get("subject") or ""
        if not dstr:
            continue
        try:
            pdate = date.fromisoformat(dstr)
        except Exception:
            try:
                pdate = datetime.strptime(dstr, "%Y-%m-%d").date()
            except Exception:
                continue
        dday = (pdate - today).days
        if 0 <= dday <= 7:
            dday_groups.setdefault(dday, []).append(subj)

    # 메시지 생성: 같은 D-Day면 과목명 쉼표 연결, D-Day 별로 별도 라인
    dday_msgs: list[str] = []
    for d in sorted(dday_groups.keys()):
        subjects = [s for s in dday_groups[d] if s]
        if not subjects:
            continue
        subj_str = ", ".join(subjects)
        if d == 0:
            msg = f"오늘은 {subj_str} 수행평가가 실시되는 날입니다!"
        else:
            msg = f"{subj_str} 수행평가까지 {d}일 남았습니다!"
        dday_msgs.append(msg)

    return render_template('index.html', name=bdName, today=today.isoformat(), dday_msgs=dday_msgs)

@app.route('/math')
def math():
    return render_template('cloud/math.html')

@app.route('/eng')
def eng():
    return render_template('cloud/eng.html')

@app.route('/gram')
def gram():
    return render_template('cloud/gram.html')

@app.route('/essay')
def essay():
    return render_template('cloud/essay.html')

@app.route('/phys')
def phys():
    return render_template('cloud/phys.html')

@app.route('/chem')
def chem():
    return render_template('cloud/chem.html')

@app.route('/bio')
def bio():
    return render_template('cloud/bio.html')

@app.route('/earth')
def earth():
    return render_template('cloud/earth.html')

@app.route('/ethic')
def ethic():
    return render_template('cloud/ethic.html')

@app.route('/stat')
def stat():
    return render_template('cloud/stat.html')

@app.route('/jp')
def jp():
    return render_template('cloud/jp.html')

@app.route('/music')
def music():
    return render_template('cloud/music.html')

@app.route('/pe')
def pe():
    return render_template('cloud/pe.html')

@app.route('/kor')
def kor():
    return render_template('cloud/kor.html')

@app.route('/notice')
def notice():
    return render_template('notice.html')

if __name__ == '__main__':
    app.run(debug=True)