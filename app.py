from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User, get_user_by_username, Participant

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DBとLoginManagerの初期化
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ユーザー読み込み関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログインルート
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        questions = request.form.get('questions')
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # ロールに応じてリダイレクト
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        return 'ログイン失敗'
    return render_template('login.html')

# ログイン後のトップページ
@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username)

# ✅ 修正済み：ログアウトルート
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 出席管理ページ
@app.route('/attendance', methods=['GET', 'POST'], endpoint='user_dashboard')
@login_required
def user_dashboard():
    if request.method == 'POST':
        email = request.form.get('email')
        questions = request.form.get('questions')
        position = request.form.get('position')
        name = request.form.get('name')
        status = request.form.get('status')

        participant = Participant.query.filter_by(name=name, user_id=current_user.id).first()
        if participant:
            participant.position = position
            participant.email = email
            participant.questions = questions
            participant.status = status
        else:
            participant = Participant(
                email=email,
                questions=questions,position=position, name=name, status=status, user_id=current_user.id)
            db.session.add(participant)
        db.session.commit()
        return redirect(url_for('user_dashboard'))

    participants = Participant.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', username=current_user.username, participants=participants)

@app.route('/update/<int:participant_id>', methods=['POST'])
@login_required
def update_participant(participant_id):
    participant = Participant.query.get_or_404(participant_id)
    participant.status = request.form['status']
    db.session.commit()
    return redirect(url_for('user_dashboard'))

@app.route('/delete/<int:participant_id>', methods=['POST'])
@login_required
def delete_participant(participant_id):
    participant = Participant.query.get_or_404(participant_id)
    db.session.delete(participant)
    db.session.commit()
    return redirect(url_for('user_dashboard'))

# 管理者用ダッシュボード（未使用モデル Attendance に注意）
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))

    participants = Participant.query.all()
    present_count = Participant.query.filter_by(status='出席').count()  # ✅ 出席者数をカウント
    return render_template('admin_dashboard.html', participants=participants, present_count=present_count)

# アプリ起動時にDB作成（ローカル開発用）
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Response
import io
import csv

@app.route('/download_csv')
@login_required
def download_csv():
    if current_user.role != 'admin':
        return redirect(url_for('index'))

    participants = Participant.query.all()

    output = io.StringIO()
    output.write('\ufeff')  # UTF-8 BOM を追加
    writer = csv.writer(output)
    writer.writerow(['名前', 'メール', '質問', '役職', 'ステータス'])

    for p in participants:
        writer.writerow([p.name, p.email, p.questions, p.position, p.status])

    output.seek(0)
    return Response(output, mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=participants.csv"})
