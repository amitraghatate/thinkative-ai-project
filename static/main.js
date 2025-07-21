document.addEventListener("DOMContentLoaded", function () {
    const editor = document.getElementById('editor');
    const suggestionsList = document.getElementById('suggestions');
    const suggestBtn = document.getElementById('suggestBtn');

    const socket = io();
    socket.emit('join');

    editor.addEventListener('input', () => {
        socket.emit('text_update', { content: editor.value });
    });

    socket.on('text_update', (data) => {
        editor.value = data.content;
    });

    suggestBtn.addEventListener('click', () => {
        const text = editor.value;
        console.log("[Client] Sending text for suggestions:", text);

        fetch('/suggest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        })
        .then(res => {
            console.log("[Client] Got response:", res);
            return res.json();
        })
        .then(data => {
            console.log("[Client] Suggestions received:", data);
            suggestionsList.innerHTML = "";
            data.suggestions.forEach(msg => {
                const li = document.createElement('li');
                li.innerText = msg;
                suggestionsList.appendChild(li);
            });
        })
        .catch(err => {
            console.error("[Client] Error during suggestion fetch:", err);
        });
    });
});
