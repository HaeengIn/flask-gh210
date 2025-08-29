from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import date

app = Flask(__name__)

load_dotenv()

supabaseUrl = os.getenv("SUPABASE_URL")
supabaseKey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabaseUrl, supabaseKey)

@app.route('/')
def index():
    today = date.today().isoformat()

    bd = supabase.table("birthday").select("name", "date").eq("date", today).execute()
    bdName = [item['name'] for item in bd.data] if bd.data else []
    
    test = supabase.table("performance").select("subject", "date").execute()
    rows = test.data()
    alertSubject = None
    alertDate = None

    for row in rows:
        subject = row["subject"]
        dbDate = datetime.strptime(row["data"], "%Y-%m-%d").date()
        dday = (dbDate - today).days
    """
    if 0 <= dday =< 7:
    results.append({
        'subject'
    })"""

    return render_template('index.html', name=bdName, today=today)

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