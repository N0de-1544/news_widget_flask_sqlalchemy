from flask import Flask, render_template, request, url_for
from data import db_session
from data.news import News
from sqlalchemy.orm import session
from random import randint
app = Flask(__name__)
app.config['SECRET_KEY'] = str(randint(10000, 100000000))


def main():
    db_session.global_init("db/news.db")
    app.run()

@app.route('/')
def show_news():
    db_sess = db_session.create_session()
    news = [(i.title, i.content, i.description) for i in db_sess.query(News).all()]
    print(news)
    return render_template('news.html', news=news)




@app.route('/news/<article_name>')
def article(article_name):
    return render_template(f'{article_name}.html', template_folder='templates')


@app.route('/create_article', methods=["POST", "GET"])
def news_creator():
    if request.method == "POST":
        news_name = request.form['newsname']
        desc = request.form['description']
        content = request.form['newscontent']
        with open(f'templates/{news_name}.html', 'w') as page:
            page.write(content)
            page.close()
        db_sess = db_session.create_session()
        news_db = News()
        news_db.title = news_name
        news_db.content = url_for('.article', article_name=news_name)
        news_db.description = desc
        db_sess.add(news_db)
        db_sess.commit()
        return show_news()
    else:
        return render_template('index.html')


if __name__ == '__main__':
    main()