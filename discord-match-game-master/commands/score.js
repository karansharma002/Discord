const { MessageEmbed } = require('discord.js');

module.exports = {
    name: 'score',
    description: 'Display the current scores of the game you are in.',
    cooldown: 7,
    execute(message, args, games, users) {
        let gameMaster = users.get(message.author.id);
        let reply = "";
        if (gameMaster) {
            let game = games.get(gameMaster);
            if (!game.isGameStarted()) {
                reply += `You cannot check the scores yet`;
            } else {
                return message.channel.send(game.getScoreOutput());
            }
        } else {
            reply += `You are not in a game.`;
        }

        const embed = new MessageEmbed()
        .setDescription(reply);
        return message.channel.send(embed);
    }
}