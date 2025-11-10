from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import time

app = Flask(__name__)
CORS(app)

# Load embedding model
print("Loading Sentence Transformer model...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
print("✓ Model loaded!")

# Load product data
df_products = None
product_embeddings = None

def load_data():
    """Load product data and embeddings on startup"""
    global df_products, product_embeddings
    try:
        df_products = pd.read_csv('data/products.csv')
        product_embeddings = np.load('data/product_embeddings.npy')
        print(f"✓ Loaded {len(df_products)} products with embeddings")
    except FileNotFoundError:
        print("⚠️ Data files not found. Run utils/vibe_matcher.py first")
        df_products = None
        product_embeddings = None

def get_embedding(text: str):
    """Get embedding using Sentence Transformers (FREE - NO API)"""
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print(f"Error getting embedding: {e}")
        raise

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Vibe Matcher API is running',
        'model': 'Sentence Transformers (FREE)',
        'data_loaded': df_products is not None
    })

@app.route('/api/search', methods=['POST'])
def search_vibes():
    """Search products by vibe query"""
    start_time = time.time()
    
    try:
        data = request.json
        query = data.get('query', '')
        top_k = data.get('top_k', 3)
        
        if not query.strip():
            return jsonify({'error': 'Empty query'}), 400
        
        if df_products is None or product_embeddings is None:
            return jsonify({'error': 'Product data not loaded'}), 500
        
        print(f"🔍 Searching for: '{query}'")
        
        # Generate query embedding using Sentence Transformers
        query_embedding = get_embedding(query)
        query_embedding = np.array(query_embedding).reshape(1, -1)
        
        # Compute cosine similarities
        similarities = cosine_similarity(query_embedding, product_embeddings)[0]
        
        # Get top matches
        df_results = df_products.copy()
        df_results['similarity_score'] = similarities
        df_results = df_results.sort_values('similarity_score', ascending=False)
        top_matches = df_results.head(top_k)
        
        # Format results
        results = []
        for _, row in top_matches.iterrows():
            results.append({
                'id': int(row['product_id']),
                'name': row['name'],
                'description': row['description'],
                'price': float(row['price']),
                'vibe_tags': eval(row['vibe_tags']) if isinstance(row['vibe_tags'], str) else row['vibe_tags'],
                'similarity_score': float(row['similarity_score'])
            })
        
        latency = time.time() - start_time
        
        print(f"✓ Found {len(results)} matches in {latency*1000:.2f}ms")
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results),
            'latency_ms': latency * 1000
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_all_products():
    """Get all products"""
    try:
        if df_products is None:
            return jsonify({'error': 'Product data not loaded'}), 500
        
        products = df_products.to_dict('records')
        return jsonify({'products': products, 'count': len(products)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_data()
    print("\n" + "="*50)
    print("🚀 VIBE MATCHER API READY")
    print("="*50)
    print("✓ Using FREE Sentence Transformers (No API costs!)")
    print("✓ Ready to accept requests")
    print("="*50 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
