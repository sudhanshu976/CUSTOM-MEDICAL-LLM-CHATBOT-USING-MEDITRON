from flask import Flask, render_template, request, jsonify
from langchain.vectorstores import Qdrant
from langchain.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient

app = Flask(__name__)

# Initialize SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")

# Initialize Qdrant client
url = "http://localhost:6333/dashboard"
client = QdrantClient(url=url, prefer_grpc=False)

# Initialize Qdrant database
db = Qdrant(client=client, embeddings=embeddings, collection_name="vector_db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        docs = db.similarity_search_with_score(query=query, k=2)
        results = [doc.page_content for doc, _ in docs]
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
