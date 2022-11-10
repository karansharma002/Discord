function sendBoard(game, board, message) {
    let temps = game.getTempMessages();
    for (let i = 0; i < temps.length; i++) {
        msgId = temps[i];
        message.channel.messages.fetch(msgId)
        .then(msg => msg.delete())
        .catch(console.error);
    }

    game.clearTempMessages();
    
    message.channel.send(game.getOutput(board))
    .then(msg => {
        game.addTempMessage(msg.id);
    })
    .catch(console.error);
    
}

module.exports = {
    sendBoard
}