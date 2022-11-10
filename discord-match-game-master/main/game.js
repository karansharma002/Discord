const { MessageEmbed } = require('discord.js');
const { MATCH, NO_MATCH } = require('../constants/flip');
const { utility, cardCollection } = require('../constants/emoji');

const boardColors = [0xf57334, 0xf5ea73, 0xa0f573, 0x73f5ce, 0x73c7f5, 0x7773f5, 0xd073f5, 0xf573ba];

module.exports = class Game {
    constructor(row, column) {
        this.row = row;
        this.column = column;
        this.color = boardColors[Math.floor(Math.random() * boardColors.length)];
        this.numCards = row * column;
        this.boardLayout = [];
        this.currentBoard = Array.from({ length: row }, () => Array.from({ length: column }, () => utility.cardDown));
        this.players = [];
        this.setupStarted = false;
        this.gameStarted = false;
        this.currentPlayer = null;
        this.flips = [];
        this.scores = {};
        this.totalMatches = 0;
        this.tempMessages = []
    }

    setup() {
        let cards = [];
        let emoji = cardCollection.slice(0);
        for (let i = 0; i < this.numCards / 2; i++) {
            let chosen = emoji.splice(Math.floor(Math.random() * emoji.length), 1)[0];
            cards.push(chosen);
            cards.push(chosen);
        }

        this.boardLayout = Array.from({ length: this.row }, () => Array.from({ length: this.column }, () => cards.splice(Math.floor(Math.random() * cards.length), 1)[0]));
        this.currentPlayer = Math.floor(Math.random() * this.players.length);

        for (let i = 0; i < this.players.length; i++) {
            this.scores[this.players[i]] = 0;
        }
    }

    startSetup() {
        this.setupStarted = true;
        this.setup();
    }

    startGame() {
        this.gameStarted = true;
    }

    isSetupStarted() {
        return this.setupStarted;
    }

    isGameStarted() {
        return this.gameStarted;
    }

    getNumCards() {
        return this.numCards;
    }

    getCurrentBoard() {
        let boardOutput = "";
        for (let i = 0; i <= this.row; i++) {
            for (let j = 0; j <= this.column; j++) {
                if (i == 0 && j == 0) {
                    boardOutput += utility.blackSquare;
                } else if (i == 0) {
                    boardOutput += utility[j];
                } else if (j == 0) {
                    boardOutput += utility[String.fromCharCode('A'.charCodeAt(0) + i - 1)];
                } else {
                    boardOutput += this.currentBoard[i-1][j-1];
                }
            }
            boardOutput += "\n";
        }

        return boardOutput;
    }

    getBoardLayout() {
        let boardOutput = "";
        for (let i = 0; i <= this.row; i++) {
            for (let j = 0; j <= this.column; j++) {
                if (i == 0 && j == 0) {
                    boardOutput += utility.blackSquare;
                } else if (i == 0) {
                    boardOutput += utility[j];
                } else if (j == 0) {
                    boardOutput += utility[String.fromCharCode('A'.charCodeAt(0) + i - 1)];
                } else {
                    boardOutput += this.boardLayout[i-1][j-1];
                }
            }
            boardOutput += "\n";
        }

        return boardOutput;
    }

    getOutput(board) {
        let output = new MessageEmbed()
        .setTitle(`${this.row}x${this.column} Board`)
        .setColor(this.color)
        .setDescription(board)
        .addField('Current Player', `<@${this.players[this.currentPlayer]}>`, true)
        .addField('All Players', this.players.map(p => `<@${p}>`).join(" "), true);
        return output;
    }

    getPlayers() {
        return this.players;
    }

    setPlayers(players) {
        this.players = players;
    }

    getCurrentPlayer() {
        return this.players[this.currentPlayer];
    }

    hasFlipped() {
        return this.flips.length == 2;
    }

    flip(row, column) {
        row = row.toLowerCase().charCodeAt(0) - 97;
        column -= 1;
        if (row < 0 || row >= this.row || column < 0 || column >= this.column) {
            return false;
        }

        if (this.currentBoard[row][column] != utility.cardDown){
            return false;
        }

        this.currentBoard[row][column] = this.boardLayout[row][column];
        this.flips.push([row, column]);
        if (this.flips.length == 2) {
            return this.checkFlip();
        }
        return true;
    }

    checkFlip() {
        let firstFlipRow = this.flips[0][0];
        let firstFlipCol = this.flips[0][1];
        let secFlipRow = this.flips[1][0];
        let secFlipCol = this.flips[1][1];

        if (this.currentBoard[firstFlipRow][firstFlipCol] == this.currentBoard[secFlipRow][secFlipCol]) {
            this.scores[this.players[this.currentPlayer]] += 1;
            this.flips = [];
            this.totalMatches += 1;
            return MATCH
        } else {
            return NO_MATCH
        }
    }

    resetFlip() {
        let firstFlipRow = this.flips[0][0];
        let firstFlipCol = this.flips[0][1];
        let secFlipRow = this.flips[1][0];
        let secFlipCol = this.flips[1][1];
        this.flips = [];
        this.currentPlayer = (this.currentPlayer + 1) % this.players.length;
        this.currentBoard[firstFlipRow][firstFlipCol] = utility.cardDown;
        this.currentBoard[secFlipRow][secFlipCol] = utility.cardDown;
    }
    
    getScoreOutput() {
        let output = new MessageEmbed()
        .setTitle(`Scores`)
        .setColor(this.color);

        let description = "";
        for (let score in this.scores) {
            if (this.players.includes(score)) {
                description += `<@${score}>: ${this.scores[score]}\n`;
            } else {
                description += `<@${score}> (Player has left): ${this.scores[score]}\n`;
            }
        }
        
        output.setDescription(description);
        return output;
    }

    checkEnd() {
        if (this.totalMatches == ((this.row * this.column) / 2) || this.players.length == 1) {
            let winners = [];
            let max = 0;
            for (let score in this.scores) {
                if (!this.players.includes(score)) {
                    continue;
                }
                
                if (this.scores[score] > max) {
                    winners = [];
                    winners.push(score);
                    max = this.scores[score];
                } else if (this.scores[score] == max) {
                    winners.push(score);
                }
            }

            let output = new MessageEmbed()
            .setTitle(`Winner(s)`)
            .setColor(this.color);

            let desc = "";
            for (let i = 0; i < winners.length; i++) {
                desc += `<@${winners[i]}>\n`
                
            }

            output.setDescription(desc);
            return output;
        }

        return null;
    }

    addTempMessage(id) {
        this.tempMessages.push(id);
    }

    getTempMessages() {
        return this.tempMessages;
    }

    clearTempMessages() {
        this.tempMessages = [];
    }
}
