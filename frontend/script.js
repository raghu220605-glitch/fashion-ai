const API_BASE = 'https://fashion-ai-jbcu.onrender.com/api'; // Update to your live URL

const recommendBtn = document.getElementById('recommendBtn');
const recommendationsList = document.getElementById('recommendations');
const statusDiv = document.getElementById('status');

recommendBtn.addEventListener('click', async () => {
    const skinTone = document.getElementById('skinTone').value;
    const itemType = document.getElementById('itemType').value;

    statusDiv.innerHTML = '<div class="spinner"></div> Curating your style...';

    try {
        const res = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ skinTone, itemType }),
        });

        const result = await res.json();
        recommendationsList.innerHTML = '';

        result.data.outfits.forEach(outfit => {
            const li = document.createElement('li');
            li.className = 'outfit-card';
            
            // Using Unsplash Source for real-world images
            const imageUrl = `https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=400&q=80&sig=${Math.random()}`;

            li.innerHTML = `
                <img src="${imageUrl}" class="outfit-img" alt="fashion">
                <div class="card-content">
                    <div class="swatch" style="background: ${outfit.color}"></div>
                    <h3>${outfit.name}</h3>
                    <p><strong>Top:</strong> ${outfit.top}</p>
                    <p><strong>Bottom:</strong> ${outfit.bottom}</p>
                </div>
            `;
            recommendationsList.appendChild(li);
        });

        statusDiv.innerHTML = `<strong>Stylist Note:</strong> ${result.data.summary}`;
        document.getElementById('result').classList.remove('hidden');

    } catch (err) {
        statusDiv.textContent = "Unable to load suggestions.";
    }
});
