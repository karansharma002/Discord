const { MessageEmbed } = require('discord.js');
const { sendBoard } = require('../main/utility');

module.exports = {
    name: 'start',
    description: 'Starts the game you are the owner of.',
    cooldown: 5,
    execute(message, args, games) {
        const embed = new MessageEmbed()
        let game = games.get(message.author.id);
        if (!game) {
            embed.setDescription("You have not created a game.");
            return message.reply(embed);
        }

        let players = game.getPlayers();
        let reply = "";
        if (players.length < 2) {
            reply += "There are not enough players.";
            embed.setDescription(reply);
            return message.reply(embed);
        } else {
            game.startSetup();
            reply += "The game with players "
            reply += players.map(p => `<@${p}>`).join(" ");
            reply += " is starting.";
        }

        const timeout = game.getNumCards() / Math.log10(game.getNumCards() ** 3) * 1000;
        reply += ` The cards will be shown for a few seconds.`;
        embed.setDescription(reply);
        message.channel.send(embed)
        .then(msg => {
            msg.delete({timeout: 3000})
            .then(() => {
                message.channel.send(game.getOutput(game.getBoardLayout()))
                .then(msg => {
                    msg.delete({ timeout: timeout })
                    .then(() => {
                        message.channel.send(new MessageEmbed().setDescription(`The game has started. <@${game.getCurrentPlayer()}> is starting!`));
                        sendBoard(game, game.getCurrentBoard(), message);
                        game.startGame();
                    })
                    .catch(console.error);
                })
                .catch(console.error);
            })
            .catch(console.error);
        })
        .catch(console.error);
    }    
}