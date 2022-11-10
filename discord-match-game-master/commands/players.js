const { MessageEmbed } = require('discord.js');

module.exports = {
    name: 'players',
    description: 'Display the current players of the game you are in.',
    cooldown: 5,
    execute(message, args, games, users) {
        let gameMaster = users.get(message.author.id);
        let reply = "";
        if (gameMaster) {
            let game = games.get(gameMaster);
            let players = game.getPlayers();
            reply += `Current Players:\n`;
            for (let i = 0; i < players.length; i++) {
                reply += `${i+1}. <@${players[i]}>\n`;
            }

            return message.channel.send(new MessageEmbed().setDescription(reply));
        } else {
            reply += `You are not in a game.`;
        }

        const embed = new MessageEmbed()
        .setDescription(reply);
        return message.channel.send(embed);
    }
}