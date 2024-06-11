from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    intro = db.Column(db.String(240), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    img = db.Column(db.String)

    @property
    def formatted_category(self):
        normalized_categories = {"игровые": "game", "офисные": "office"}
        return normalized_categories.get(self.category.lower(), None)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/tovari')
def tovari():
    vivodikrana = Article.query.order_by(Article.date.desc()).all()
    return render_template('tovari.html', articles=vivodikrana)

@app.route('/tovari/<int:id>')
def tovari_podrobnee(id):
    vivodikran = Article.query.get(id)
    return render_template('tovari_podrobnee.html', article=vivodikran)

@app.route('/tovari/<int:id>/delete')
def tovari_delete(id):
    vivodikran = Article.query.get_or_404(id)

    try:
        db.session.delete(vivodikran)
        db.session.commit()
        return redirect('/tovari')
    except:
        return 'При удалении товара возникла ошибка'

@app.route('/tovari/<int:id>/update', methods=['POST','GET'])
def tovari_update(id):
    vivodikran = Article.query.get(id)
    if request.method == 'POST':
        vivodikran.title = request.form['title']
        vivodikran.intro = request.form['intro']
        vivodikran.text = request.form['text']
        vivodikran.category = request.form['category']

        try:
            db.session.commit()
            return redirect('/tovari')
        except:
            return 'При редактировании товара возникла ошибка'
    else:
        return render_template('tovari_update.html', article=vivodikran)

@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        category = request.form['category']
        img = request.files["img"]
        imgname = img.filename
        if imgname:
            img.save(os.path.join(app.root_path, 'static', 'image', imgname))

        article = Article(title=title, intro=intro, text=text, img=imgname, category=category)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/tovari')
        except:
            return 'При добавлении товара возникла ошибка'
    else:
        return render_template('create-article.html')

if __name__ == '__main__':
    app.run(debug=True)
