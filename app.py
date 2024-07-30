from flask import Flask, render_template, request, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random key

boggle_game = Boggle()

@app.route('/')
def index():
    """Display the game board and score."""
    board = boggle_game.make_board()
    session['board'] = board
    session['score'] = 0
    session['games_played'] = session.get('games_played', 0)  # Keep previous count
    session['highest_score'] = session.get('highest_score', 0)  # Keep previous high score
    return render_template('index.html', board=board)

@app.route('/check-word', methods=['POST'])
def check_word():
    """Check if the submitted word is valid."""
    word = request.json.get('word')
    board = session.get('board')
    result = boggle_game.check_valid_word(board, word)
    return jsonify({"result": result})

@app.route('/end-game', methods=['POST'])
def end_game():
    """Handle end of game stats and update scores."""
    score = request.json.get('score')
    games_played = session.get('games_played', 0) + 1
    highest_score = max(session.get('highest_score', 0), score)

    session['games_played'] = games_played
    session['highest_score'] = highest_score

    return jsonify({
        "games_played": games_played,
        "highest_score": highest_score
    })

@app.route('/start-new-game', methods=['POST'])
def start_new_game():
    """Reset the game and provide a new board."""
    board = boggle_game.make_board()  # Generate a new board
    session['board'] = board
    return jsonify({
        "board": board
    })

if __name__ == '__main__':
    app.run(debug=True)
