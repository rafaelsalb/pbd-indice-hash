from flask import Flask, render_template, request, redirect, url_for

from db import Database


app = Flask(__name__)

db: Database | None = None


@app.get("/")
def index():
    return render_template("index.html")

@app.post("/config")
def config_db():
    global db
    bucket_size = int(request.form.get("bucket_size"))
    page_size = int(request.form.get("page_size"))

    db = Database(bucket_size, page_size)
    return redirect(url_for("show_db"))

@app.get("/db")
def show_db():
    if db is None:
        return redirect(url_for("index"))
    return render_template(
        "db.html",
        n_buckets=db.n_buckets,
        bucket_size=db.bucket_size,
        n_pages=db.n_pages,
        page_size=db.page_size,
        collisions=db.collisions,
        overflows=db.overflows,
        pages=db.index.pages,
        buckets=db.index.buckets,
    )


if __name__ == "__main__":
    app.run(debug=True)
