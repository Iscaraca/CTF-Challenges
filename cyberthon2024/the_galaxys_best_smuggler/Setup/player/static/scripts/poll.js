function pollFlaskBackend() {
    fetch("/poll")
        .then(response => response.json())
        .then(data => {
            // Check for a win
            if ("game_ended" in data) {
                if (data["game_ended"]) {
                    document.getElementById('turn-signaller').textContent = "";
                    document.getElementById('flag').textContent = data["flag"];
                    document.getElementById('modal-overlay').style.display = 'block';
                    document.getElementById('modal').style.display = 'block';
                } else {
                    document.getElementById('modal-overlay').style.display = 'none';
                    document.getElementById('modal').style.display = 'none';
                }
            }

            // Update players' hands
            if ("player_2_hand" in data) {
                document.getElementById('join-button').textContent = "";

                const opponentCardValues = data["player_2_hand"]
                const handOpponentDiv = document.querySelector('.hand-opponent');
                handOpponentDiv.innerHTML = '';

                opponentCardValues.forEach(value => {
                    const cardDiv = document.createElement('div');
                    if ("game_ended" in data && data["game_ended"]) {
                        cardDiv.classList.add('card-opponent', 'black');
                    } else {
                        cardDiv.classList.add('card-opponent', 'black', 'face-down');
                    }
                    const valueDiv = document.createElement('div');
                    valueDiv.classList.add('value-opponent');
                    valueDiv.textContent = value;
                    cardDiv.appendChild(valueDiv);
                    handOpponentDiv.appendChild(cardDiv);
                });

                const cardValues = data["player_1_hand"]
                const handDiv = document.querySelector('.hand');
                handDiv.innerHTML = '';

                cardValues.forEach(value => {
                    const cardDiv = document.createElement('div');
                    cardDiv.classList.add('card', 'black');
                
                    const valueDiv = document.createElement('div');
                    valueDiv.classList.add('value');
                    valueDiv.textContent = value;
                    cardDiv.appendChild(valueDiv);
                    handDiv.appendChild(cardDiv);
                });
            }

            
            // Update menu
            document.getElementById('menu').style.display = 'none';
            if ("turn_number" in data) {
                if (data["turn_number"] % 2 == 0) {
                    document.getElementById('turn-signaller').textContent = "Your turn";
                    document.getElementById('menu').style.display = 'inline';
                } else {
                    document.getElementById('turn-signaller').textContent = "Opponent's turn";
                }
            } else {
                document.getElementById('turn-signaller').textContent = "";
            }
        })
        .catch(error => console.error('Error:', error));
}

pollFlaskBackend()

// Poll every 0.5s
setInterval(pollFlaskBackend,  500)