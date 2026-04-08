// Replace with your Render URL when you deploy
const API_BASE = 'https://fashion-ai-jbcu.onrender.com'; 

const recommendBtn = document.getElementById('recommendBtn');
const recommendationsList = document.getElementById('recommendations');
const statusDiv = document.getElementById('status');
const styleInput = document.getElementById('styleInput');
const styleSelect = document.getElementById('styleSelect');

recommendBtn.addEventListener('click', async () => {
    const description = styleInput.value;
    const style = styleSelect.value;

    statusDiv.textContent = '✨ Gemini Stylist is thinking...';
    recommendationsList.innerHTML = ''; 

    try {
        const res = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ style, description }),
        });

        const result = await res.json();
        statusDiv.textContent = result.data.summary || 'Curated just for you:';

        result.data.outfits.forEach(outfit => {
            const li = document.createElement('li');
            li.className = 'outfit-card';
            
            li.innerHTML = `
                <div>
                    <div class="outfit-img" style="display:flex; align-items:center; justify-content:center; background:#f3f0ff; color:#a855f7;">
                        <span>AI Concept</span>
                    </div>
                    <div class="swatch" style="background: linear-gradient(90deg, var(--accent), var(--accent3))"></div>
                </div>
                <div class="card-content">
                    <span class="badge badge-violet">${style}</span>
                    <h3>${outfit.name}</h3>
                    <p class="desc">${outfit.top.item} with ${outfit.bottom.item}</p>
                    <p class="meta">Vibe: ${outfit.vibe}</p>
                    <p class="price">${outfit.price || 'Personalized'}</p>
                </div>
            `;
            recommendationsList.appendChild(li);
        });

    } catch (err) {
        statusDiv.textContent = '❌ Connection Error. Is the backend running?';
    }
});
