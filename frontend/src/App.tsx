import { useState } from 'react';
import axios from 'axios';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  vibe_tags: string[];
  similarity_score: number;
}

interface SearchResponse {
  query: string;
  results: Product[];
  count: number;
  latency_ms: number;
}

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [latency, setLatency] = useState<number | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults([]);

    try {
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const response = await axios.post<SearchResponse>(
    `${BACKEND_URL}/api/search`,
    { query: query, top_k: 3 }
  );

  setResults(response.data.results);
  setLatency(response.data.latency_ms);

} catch (err: any) {
  setError(err.response?.data?.error || 'Failed to fetch results');
} finally {
  setLoading(false);
}

  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to bottom, #eff6ff, #faf5ff, #fef3c7)', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      
      {/* HEADER - COMPACT */}
      <div style={{ textAlign: 'center', paddingTop: '40px', paddingBottom: '30px', width: '100%', maxWidth: '1200px', paddingLeft: '20px', paddingRight: '20px' }}>
        
        <h1 style={{ fontSize: '48px', fontWeight: 900, marginBottom: '15px', background: 'linear-gradient(to right, #6366f1, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
          Vibe Matcher ✨
        </h1>
        
        <p style={{ fontSize: '16px', color: '#374151', fontWeight: 600, marginBottom: '30px' }}>
          Find Fashion That Matches Your Energy
        </p>

        {/* COMPACT SEARCH BAR */}
        <form onSubmit={handleSearch} style={{ maxWidth: '700px', margin: '0 auto', marginBottom: '20px' }}>
          <div style={{ background: 'white', borderRadius: '25px', boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.2)', padding: '5px', display: 'flex', alignItems: 'center', gap: '10px', border: '2px solid #e0e7ff' }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe your vibe..."
              style={{ flex: 1, padding: '15px 20px', fontSize: '14px', fontWeight: 600, outline: 'none', border: 'none', borderRadius: '25px', background: 'transparent' }}
            />
            <button
              type="submit"
              disabled={loading}
              style={{ padding: '15px 30px', background: loading ? '#9ca3af' : 'linear-gradient(to right, #6366f1, #ec4899)', color: 'white', fontSize: '16px', fontWeight: 900, borderRadius: '25px', border: 'none', cursor: loading ? 'not-allowed' : 'pointer', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
            >
              {loading ? '⏳' : '🔍'}
            </button>
          </div>
        </form>

        {error && (
          <div style={{ maxWidth: '600px', margin: '0 auto', background: '#fee2e2', border: '2px solid #fca5a5', color: '#991b1b', padding: '12px', borderRadius: '12px', fontSize: '14px', fontWeight: 700 }}>
            ❌ {error}
          </div>
        )}
        
        {latency && (
          <div style={{ maxWidth: '600px', margin: '0 auto', background: '#d1fae5', border: '2px solid #6ee7b7', color: '#065f46', padding: '12px', borderRadius: '12px', fontSize: '14px', fontWeight: 700 }}>
            ⚡ Found in {latency.toFixed(0)}ms
          </div>
        )}
      </div>

      {/* COMPACT SUGGESTIONS */}
      {results.length === 0 && !loading && (
        <div style={{ width: '100%', maxWidth: '1200px', paddingLeft: '20px', paddingRight: '20px', paddingBottom: '40px' }}>
          <h2 style={{ fontSize: '24px', fontWeight: 900, textAlign: 'center', color: '#1f2937', marginBottom: '30px' }}>
            ✨ Popular Vibes
          </h2>
          
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '12px' }}>
            
            {[
              { text: 'energetic urban chic', emoji: '⚡', bg: 'linear-gradient(to bottom right, #ddd6fe, #e9d5ff)' },
              { text: 'cozy comfortable', emoji: '☁️', bg: 'linear-gradient(to bottom right, #fed7aa, #fde68a)' },
              { text: 'elegant formal', emoji: '💎', bg: 'linear-gradient(to bottom right, #bfdbfe, #dbeafe)' },
              { text: 'beach summer', emoji: '🌊', bg: 'linear-gradient(to bottom right, #99f6e4, #d1fae5)' },
            ].map((item) => (
              <button
                key={item.text}
                onClick={() => setQuery(item.text)}
                style={{ padding: '15px 25px', background: item.bg, borderRadius: '25px', border: 'none', cursor: 'pointer', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)', transition: 'all 0.3s' }}
                onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-4px)'}
                onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
              >
                <span style={{ fontSize: '24px', marginRight: '6px' }}>{item.emoji}</span>
                <span style={{ fontSize: '14px', fontWeight: 900, color: '#1f2937' }}>{item.text}</span>
              </button>
            ))}
            
          </div>
        </div>
      )}

      {/* COMPACT RESULTS */}
      {results.length > 0 && (
        <div style={{ width: '100%', maxWidth: '1200px', paddingLeft: '20px', paddingRight: '20px', paddingBottom: '40px' }}>
          <h2 style={{ fontSize: '28px', fontWeight: 900, textAlign: 'center', color: '#1f2937', marginBottom: '30px' }}>
            🛒 Results for <span style={{ color: '#6366f1' }}>"{query}"</span>
          </h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
            
            {results.map((product, idx) => (
              <div key={product.id} style={{ background: 'white', borderRadius: '16px', boxShadow: '0 10px 20px -5px rgba(0, 0, 0, 0.15)', overflow: 'hidden', border: '2px solid #e5e7eb', transition: 'all 0.3s' }}
                onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-6px)'}
                onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
              >
                
                {/* Product Image */}
                <div style={{ height: '160px', background: 'linear-gradient(to bottom right, #ddd6fe, #fce7f3, #fed7aa)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
                  <span style={{ fontSize: '60px' }}>
                    {['👗', '🧥', '👕'][idx]}
                  </span>
                  <div style={{ position: 'absolute', top: '10px', right: '10px', background: 'white', padding: '6px 12px', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
                    <span style={{ fontSize: '13px', fontWeight: 900, color: '#10b981' }}>
                      {(product.similarity_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>

                {/* Product Info */}
                <div style={{ padding: '16px' }}>
                  <h3 style={{ fontSize: '18px', fontWeight: 900, color: '#1f2937', marginBottom: '8px' }}>
                    {product.name}
                  </h3>
                  <p style={{ fontSize: '13px', color: '#6b7280', marginBottom: '12px', lineHeight: 1.4, overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>
                    {product.description}
                  </p>
                  
                  {/* Tags */}
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginBottom: '12px' }}>
                    {product.vibe_tags.map((tag, i) => (
                      <span key={i} style={{ padding: '4px 8px', background: '#ede9fe', color: '#6366f1', fontSize: '10px', fontWeight: 700, borderRadius: '10px', border: '1px solid #c7d2fe' }}>
                        #{tag}
                      </span>
                    ))}
                  </div>

                  {/* Price & Button */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', borderTop: '2px solid #f3f4f6' }}>
                    <span style={{ fontSize: '24px', fontWeight: 900, background: 'linear-gradient(to right, #6366f1, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                      {product.price}
                    </span>
                    <button style={{ padding: '8px 16px', background: 'linear-gradient(to right, #10b981, #059669)', color: 'white', fontSize: '12px', fontWeight: 900, borderRadius: '8px', border: 'none', cursor: 'pointer', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
                      🛒 Add
                    </button>
                  </div>
                </div>
              </div>
            ))}

          </div>
        </div>
      )}

      {/* COMPACT FOOTER */}
      <footer style={{ background: 'white', borderTop: '2px solid #e5e7eb', padding: '20px', width: '100%', textAlign: 'center', marginTop: '40px' }}>
        <p style={{ fontSize: '14px', fontWeight: 700, color: '#1f2937', marginBottom: '4px' }}>
          Built with ❤️ using React + TypeScript + Flask + AI
        </p>
        <p style={{ fontSize: '12px', color: '#6b7280' }}>
          © 2025 Vibe Matcher • Powered by Sentence Transformers
        </p>
      </footer>

    </div>
  );
}

export default App;
