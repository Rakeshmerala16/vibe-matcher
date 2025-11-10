"""
Vibe Matcher: Data Preparation with Sentence Transformers (FREE)
Run this script first to prepare data: python utils/vibe_matcher.py
"""

import pandas as pd
import numpy as np
import os
from typing import List
import time
from sentence_transformers import SentenceTransformer

# Load free embedding model (downloads ~400MB first time)
print("Loading embedding model...")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
print("✓ Model loaded!\n")

def get_embedding(text: str) -> List[float]:
    """Get embedding using Sentence Transformers (FREE)"""
    try:
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print(f"Error getting embedding for text: {text[:50]}...")
        print(f"Error: {e}")
        raise

def prepare_product_data():
    """Create expanded fashion product dataset - 20 items"""
    
    products_data = {
        'product_id': list(range(1, 21)),
        'name': [
            # Original 8
            'Boho Maxi Dress',
            'Urban Leather Jacket',
            'Cozy Oversized Sweater',
            'Minimalist White Sneakers',
            'Vintage Denim Jacket',
            'Elegant Silk Blouse',
            'Streetwear Cargo Pants',
            'Beach Summer Romper',
            
            # New 12 items
            'Classic Black Blazer',
            'Casual Linen Pants',
            'Sporty Yoga Leggings',
            'Romantic Floral Midi Dress',
            'Edgy Ripped Jeans',
            'Professional Office Skirt',
            'Trendy Oversized Hoodie',
            'Chic Wrap Dress',
            'Athletic Running Shorts',
            'Vintage Band T-Shirt',
            'Luxury Cashmere Cardigan',
            'Bohemian Fringe Vest'
        ],
        'description': [
            # Original 8
            'Flowy maxi dress with earthy tones, perfect for festival vibes and bohemian aesthetics. Features floral patterns and comfortable cotton fabric.',
            'Edgy black leather jacket with silver zippers. Perfect for energetic urban chic style and modern streetwear looks.',
            'Soft oversized knit sweater in warm neutral tones. Ideal for cozy comfort and relaxed casual vibes.',
            'Clean minimalist white sneakers with sleek design. Perfect for modern minimalist and casual urban style.',
            'Classic vintage denim jacket with distressed details. Timeless casual style with retro bohemian charm.',
            'Luxurious silk blouse in champagne color. Sophisticated elegant style for formal occasions and refined aesthetics.',
            'Bold olive green cargo pants with multiple pockets. Perfect for streetwear enthusiasts and urban adventurers.',
            'Lightweight floral romper in pastel colors. Breezy beach vibes and carefree summer energy.',
            
            # New 12 items
            'Tailored black blazer with structured shoulders. Perfect for professional business meetings and formal events.',
            'Breathable linen pants in beige. Relaxed casual style ideal for warm weather and laid-back occasions.',
            'High-waisted yoga leggings with moisture-wicking fabric. Perfect for active lifestyle and fitness enthusiasts.',
            'Midi-length floral dress with ruffle details. Romantic feminine style perfect for dates and garden parties.',
            'Distressed skinny jeans with ripped knees. Edgy rebellious style for bold fashion statements.',
            'A-line pencil skirt in navy blue. Professional polished look for corporate environments and business casual.',
            'Oversized hoodie in charcoal gray with kangaroo pocket. Street-style essential for casual urban comfort.',
            'Elegant wrap dress with V-neckline. Sophisticated chic style that flatters all body types.',
            'Lightweight running shorts with built-in liner. Athletic performance wear for active sports and training.',
            'Retro band t-shirt with vintage concert graphics. Rock-inspired casual style with nostalgic vibes.',
            'Premium cashmere cardigan in soft gray. Luxurious layering piece for elegant refined style.',
            'Bohemian vest with fringe details and earthy tones. Festival-ready piece with free-spirited boho vibes.'
        ],
        'price': [
            # Original 8
            89.99, 249.99, 65.99, 79.99, 119.99, 159.99, 95.99, 55.99,
            
            # New 12 items
            179.99, 69.99, 49.99, 95.99, 89.99, 75.99, 59.99, 
            125.99, 34.99, 45.99, 299.99, 105.99
        ],
        'vibe_tags': [
            # Original 8
            ['boho', 'festival', 'flowy', 'earthy'],
            ['urban', 'edgy', 'chic', 'modern'],
            ['cozy', 'comfort', 'casual', 'relaxed'],
            ['minimalist', 'clean', 'modern', 'casual'],
            ['vintage', 'casual', 'retro', 'boho'],
            ['elegant', 'sophisticated', 'formal', 'luxe'],
            ['streetwear', 'urban', 'bold', 'adventurous'],
            ['beach', 'summer', 'breezy', 'carefree'],
            
            # New 12 items
            ['professional', 'formal', 'elegant', 'business'],
            ['casual', 'relaxed', 'comfortable', 'breezy'],
            ['sporty', 'athletic', 'active', 'fitness'],
            ['romantic', 'feminine', 'floral', 'sweet'],
            ['edgy', 'rebellious', 'bold', 'urban'],
            ['professional', 'polished', 'corporate', 'classic'],
            ['streetwear', 'casual', 'urban', 'comfortable'],
            ['chic', 'elegant', 'sophisticated', 'feminine'],
            ['athletic', 'sporty', 'active', 'performance'],
            ['vintage', 'retro', 'rock', 'casual'],
            ['luxe', 'elegant', 'refined', 'premium'],
            ['boho', 'festival', 'free-spirited', 'earthy']
        ]
    }
    
    df = pd.DataFrame(products_data)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/products.csv', index=False)
    print("✓ Products saved to data/products.csv")
    
    return df


def generate_embeddings(df: pd.DataFrame):
    """Generate embeddings using Sentence Transformers"""
    
    print("\n" + "="*60)
    print("GENERATING EMBEDDINGS (FREE - NO API NEEDED)")
    print("="*60)
    print(f"Model: all-MiniLM-L6-v2 (Sentence Transformers)")
    print(f"Total products: {len(df)}")
    print("="*60 + "\n")
    
    embeddings = []
    total_time = 0
    
    for idx, row in df.iterrows():
        start_time = time.time()
        
        print(f"Processing {idx+1}/{len(df)}: {row['name'][:30]}...", end=" ")
        
        try:
            embedding = get_embedding(row['description'])
            embeddings.append(embedding)
            
            latency = time.time() - start_time
            total_time += latency
            
            print(f"✓ ({latency:.2f}s)")
            
        except Exception as e:
            print(f"✗ Failed: {e}")
            raise
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings)
    
    # Save embeddings
    np.save('data/product_embeddings.npy', embeddings_array)
    
    print("\n" + "="*60)
    print("EMBEDDING GENERATION COMPLETE")
    print("="*60)
    print(f"✓ Generated {len(embeddings)} embeddings")
    print(f"✓ Embedding dimension: {embeddings_array.shape[1]}")
    print(f"✓ Total time: {total_time:.2f}s")
    print(f"✓ Average time per embedding: {total_time/len(embeddings):.2f}s")
    print(f"✓ Saved to: data/product_embeddings.npy")
    print("="*60 + "\n")
    
    return embeddings_array

def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("VIBE MATCHER - DATA PREPARATION")
    print("="*60 + "\n")
    
    # Step 1: Create product data
    print("Step 1: Creating product dataset...")
    df = prepare_product_data()
    print()
    
    # Step 2: Generate embeddings
    print("Step 2: Generating embeddings...")
    embeddings = generate_embeddings(df)
    print()
    
    print("✅ DATA PREPARATION COMPLETE!")
    print("\nNext steps:")
    print("  1. Run the Flask backend: python app.py")
    print("  2. Start the React frontend: npm run dev")
    print("  3. Test the vibe matcher!\n")

if __name__ == '__main__':
    main()
