from flask import Flask, render_template, request, redirect, url_for, Response, stream_with_context
import json

from db import Database


app = Flask(__name__)

db: Database | None = None
word_count: int = 0


@app.get("/")
def index():
    return render_template("index.html")

@app.post("/config")
def config_db():
    global db, word_count
    bucket_size = int(request.form.get("bucket_size"))
    page_size = int(request.form.get("page_size"))
    words_file = request.form.get("words")
    try:
        with open(words_file, "r") as f:
            words = [line.strip() for line in f]
            word_count = len(words)
            if word_count == 0:
                return f"O arquivo '{words_file}' está vazio.", 400
    except Exception:
        return f"Houve um erro ao ler o arquivo de palavras.", 400

    db = Database(bucket_size, page_size)
    db.fill(words)
    return redirect(url_for("show_db"))

@app.get("/db")
def show_db():
    if db is None:
        return redirect(url_for("index"))
    return render_template(
        "db.html",
        registries=word_count,
        n_buckets=db.n_buckets,
        bucket_size=db.bucket_size,
        n_pages=db.n_pages,
        page_size=db.page_size,
        collisions=db.collisions,
        overflows=db.overflows,
    )

@app.get("/db/pages")
def get_pages():
    if db is None:
        return []

    def generate():
        for page in db.pages:
            page_data = {
                "size": page._size,
                "index": page.index,
                "items": page.items,
                "is_full": page.is_full()
            }
            yield json.dumps(page_data) + "\n"

    return Response(stream_with_context(generate()), mimetype='application/x-ndjson')

@app.get("/db/index")
def get_index():
    if db is None:
        return []

    def serialize_bucket(bucket):
        """Recursively serialize a bucket including its overflow chain"""
        overflow_data = None
        if bucket._overflow is not None:
            overflow_data = serialize_bucket(bucket._overflow)

        return {
            "items": [(item, page_addr) for item, page_addr in bucket.items],
            "size": bucket.size,
            "is_overflow": bucket.is_overflow,
            "overflow": overflow_data
        }

    def generate():
        for i, bucket in enumerate(db.index.buckets):
            bucket_data = {
                "index": i,
                "bucket": serialize_bucket(bucket)
            }
            yield json.dumps(bucket_data) + "\n"

    return Response(stream_with_context(generate()), mimetype='application/x-ndjson')



if __name__ == "__main__":
    app.run(debug=True)
