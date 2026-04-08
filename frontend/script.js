// Update this line with your actual live URL
const API_BASE = 'https://fashion-ai-jbcu.onrender.com/api';

const recommendBtn = document.getElementById('recommendBtn');
const recommendationsList = document.getElementById('recommendations');
const statusDiv = document.getElementById('status');

recommendBtn.addEventListener('click', async () => {
    const skinTone = document.getElementById('skinTone').value;
    const itemType = document.getElementById('itemType').value;

    statusDiv.textContent = 'Asking Gemini Stylist...';
    recommendationsList.innerHTML = '';

    try {
        const res = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ skinTone, itemType }),
        });

        const result = await res.json();
        
        // Handle Fallback Notification
        if (result.note === "fallback_active") {
            statusDiv.innerHTML = "⚠️ <strong>Offline Mode:</strong> Using saved recommendations.";
        } else {
            statusDiv.textContent = result.data.summary;
        }

        result.data.outfits.forEach(outfit => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div style="margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                    <strong>${outfit.name}</strong><br>
                    👕 ${outfit.top.item}<br>
                    👖 ${outfit.bottom.item}
                </div>
            `;
            recommendationsList.appendChild(li);
        });

        document.getElementById('result').classList.remove('hidden');

    } catch (err) {
        statusDiv.textContent = "Could not connect to server.";
    }
});
