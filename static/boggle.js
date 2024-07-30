document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("word-form");
    const result = document.getElementById("result");
    const scoreSpan = document.getElementById("score");
    const highestScoreSpan = document.getElementById("highest-score");
    const gamesPlayedSpan = document.getElementById("games-played");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const wordInput = document.getElementById("word");
        const word = wordInput.value;

        // Send the word to the server for checking
        const response = await fetch(`/check-word?word=${word}`);
        const data = await response.json();
        result.textContent = data.result;

        // Clear the input box after submission
        wordInput.value = '';

        // Update score logic here
        let score = parseInt(scoreSpan.textContent);
        if (data.result === 'ok') {
            score += word.length; // Increase score by the length of the word
        }
        scoreSpan.textContent = score;

        // Post the score to the server
        const postResponse = await fetch("/post-score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ score: score })
        });
        const postData = await postResponse.json();

        // Update highest score and games played
        if (postData.brokeRecord) {
            highestScoreSpan.textContent = score;
        }
        let gamesPlayed = parseInt(gamesPlayedSpan.textContent);
        gamesPlayed += 1;
        gamesPlayedSpan.textContent = gamesPlayed;
    });
});
