const gameBoard = document.getElementById("game-board");
const timerDisplay = document.getElementById("timer");
const movesDisplay = document.getElementById("moves");
const matchesDisplay = document.getElementById("matches");
const messageDisplay = document.getElementById("message");
const newGameButton = document.getElementById("new-game-btn");

const symbols = [
    "🍎", "🍎",
    "🍌", "🍌",
    "🍇", "🍇",
    "🍉", "🍉",
    "🍓", "🍓",
    "🥝", "🥝",
    "🍒", "🍒",
    "🥭", "🥭"
];

let firstCard = null;
let secondCard = null;
let lockBoard = false;

let moves = 0;
let matches = 0;
let timeLeft = 60;
let timer = null;
let gameStarted = false;


// Shuffle cards
function shuffleCards() {
    return [...symbols].sort(() => Math.random() - 0.5);
}


// Create the game board
function createBoard() {
    gameBoard.innerHTML = "";

    const shuffledCards = shuffleCards();

    shuffledCards.forEach((symbol) => {
        const card = document.createElement("button");

        card.classList.add("card");
        card.dataset.symbol = symbol;
        card.textContent = "?";

        card.addEventListener("click", () => flipCard(card));

        gameBoard.appendChild(card);
    });
}


// Flip a card
function flipCard(card) {
    if (
        lockBoard ||
        card === firstCard ||
        card.classList.contains("matched") ||
        card.classList.contains("flipped")
    ) {
        return;
    }

    if (!gameStarted) {
        startTimer();
        gameStarted = true;
    }

    card.classList.add("flipped");
    card.textContent = card.dataset.symbol;

    if (!firstCard) {
        firstCard = card;
        return;
    }

    secondCard = card;
    moves++;

    movesDisplay.textContent = moves;

    checkMatch();
}


// Check whether two cards match
function checkMatch() {
    const isMatch =
        firstCard.dataset.symbol === secondCard.dataset.symbol;

    if (isMatch) {
        firstCard.classList.add("matched");
        secondCard.classList.add("matched");

        matches++;
        matchesDisplay.textContent = matches;

        resetCards();

        if (matches === symbols.length / 2) {
            endGame(true);
        }

    } else {
        lockBoard = true;

        setTimeout(() => {
            firstCard.classList.remove("flipped");
            secondCard.classList.remove("flipped");

            firstCard.textContent = "?";
            secondCard.textContent = "?";

            resetCards();
        }, 800);
    }
}


// Reset selected cards
function resetCards() {
    firstCard = null;
    secondCard = null;
    lockBoard = false;
}


// Start timer
function startTimer() {
    timer = setInterval(() => {
        timeLeft--;

        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            endGame(false);
        }
    }, 1000);
}


// End game
function endGame(won) {
    clearInterval(timer);
    lockBoard = true;

    if (won) {
        messageDisplay.textContent =
            `🎉 Congratulations! You matched all pairs in ${moves} moves.`;
    } else {
        messageDisplay.textContent =
            "⏰ Time's up! Press New Game to try again.";
    }
}


// Start a new game
function startNewGame() {
    clearInterval(timer);

    firstCard = null;
    secondCard = null;
    lockBoard = false;

    moves = 0;
    matches = 0;
    timeLeft = 60;
    gameStarted = false;

    movesDisplay.textContent = "0";
    matchesDisplay.textContent = "0";
    timerDisplay.textContent = "60";
    messageDisplay.textContent = "";

    createBoard();
}


// New Game button
newGameButton.addEventListener("click", startNewGame);


// Start the first game
startNewGame();