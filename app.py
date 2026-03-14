from dataclasses import asdict

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

    try:
        db = Database(bucket_size, page_size)
        db.fill(words)
    except Exception as e:
        return f"Houve um erro ao configurar o banco de dados: {e}", 400
    # assert type(db.index.buckets[0].items[0]) == tuple, "Expected items in buckets to be tuples of (str, tuple[int, int])"
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
        index_build_time=db.index_build_time,
        collision_rate=db.collisions / word_count
    )

@app.get("/db/pages")
def get_pages():
    if db is None:
        return []

    # Get pagination parameters
    page_num = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 50))

    # Calculate pagination
    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size
    total_pages = len(db.pages)

    # Get paginated slice
    paginated_pages = db.pages[start_idx:end_idx]

    def generate():
        for page in paginated_pages:
            page_data = {
                "size": page._size,
                "index": page.index,
                "items": page.items,
                "is_full": page.is_full()
            }
            yield json.dumps(page_data) + "\n"

    return Response(
        stream_with_context(generate()),
        mimetype='application/x-ndjson',
        headers={
            'X-Total-Count': str(total_pages),
            'X-Page': str(page_num),
            'X-Page-Size': str(page_size),
            'X-Total-Pages': str((total_pages + page_size - 1) // page_size)
        }
    )

@app.get("/db/index")
def get_index():
    if db is None:
        return []

    # Get pagination parameters
    page_num = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 50))

    # Calculate pagination
    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size
    total_buckets = len(db.index.buckets)

    # Get paginated slice
    paginated_buckets = list(enumerate(db.index.buckets))[start_idx:end_idx]

    def serialize_bucket(bucket):
        """Recursively serialize a bucket including its overflow chain"""
        overflow_data = None
        if bucket._overflow is not None:
            overflow_data = serialize_bucket(bucket._overflow)

        return {
            "items": [[item, list(page_addr)] for item, page_addr in bucket.items],
            "size": bucket.size,
            "is_overflow": bucket.is_overflow,
            "overflow": overflow_data
        }

    def generate():
        for i, bucket in paginated_buckets:
            bucket_data = {
                "index": i,
                "bucket": serialize_bucket(bucket)
            }
            yield json.dumps(bucket_data) + "\n"

    return Response(
        stream_with_context(generate()),
        mimetype='application/x-ndjson',
        headers={
            'X-Total-Count': str(total_buckets),
            'X-Page': str(page_num),
            'X-Page-Size': str(page_size),
            'X-Total-Pages': str((total_buckets + page_size - 1) // page_size)
        }
    )

@app.get("/db/search")
def search_db():
    if db is None:
        return {"error": "Database not configured"}, 400

    query = request.args.get("query", "")
    if not query:
        return {"error": "Query parameter is required"}, 400

    # (page_index, record_index), search_time = db.query(query)
    result = db.query(query)
    # page_index = result.query_result.page_index
    # record_index = result.query_result.record_index
    # search_time = result.search_time_ms
    # bucket_index = result.bucket_index
    # bucket_position = result.bucket_position
    # print(f"Search for '{query}' returned page index {page_index}, record index {record_index} with search time {search_time} ms")
    if result.query_result.page_index == -1:
        return {"message": f"Registro '{query}' não encontrado.", "search_time_ms": result.search_time}

    return asdict(result)

@app.get("/db/table_scan")
def search_table_scan():
    if db is None:
        return {"error": "Database not configured"}, 400

    query = request.args.get("query", "")
    if not query:
        return {"error": "Query parameter is required"}, 400

    result = db.table_scan_query(query)
    if not result.found:
        return {"message": f"Registro '{query}' não encontrado.", "search_time_ms": result.search_time_ms}

    return asdict(result)


if __name__ == "__main__":
    app.run(debug=True)
