const { MessageEmbed, DiscordAPIError } = require('discord.js');
const Game = require('../main/game.js');

module.exports = {
    name: 'play',
    aliases: ['create', 'p'],
    description: 'Start a match game of a specified size.',
    usage: '<size>',
    cooldown: 4,
    args: true,
    execute(message, args, games, users) {
        let embed = new MessageEmbed();
        if (users.get(message.author.id)) {
            embed.setDescription(`You are already in a game. Please exit it first.`);
            return message.reply(embed);
        }

        if (args.length > 2) {
            embed.setDescription(`Too many size dimensions provided. Please specify at most two dimensions.`);
            return message.reply(embed);
        }

        for (let i = 0; i < args.length; i++) {
            let arg = args[i];
            if (isNaN(arg) || arg < 0) {
                embed.setDescription(`Board dimensions must be a positive number.`);
                return message.reply(embed);
            }
        }
        
        let row = args[0];
        let column = 0;
        if (args.length == 1) {
            column = row;
        } else {
            column = args[1];
        }

        if (row > 10 || column > 10 || row < 2 || column < 2) {
            embed.setDescription(`Rows and columns must be in the range 2-10.`);
            return message.reply(embed);
        }

        const numCards = row * column;
        if (numCards % 2 != 0) {
            embed.setDescription(`Please specify dimensions that create a board with an even number of cards.`);
            return message.reply(embed);
        }

        if (numCards > 100) {
            embed.setDescription(`Board dimensions are too large. Maximum number of cards is 100.`);
            return message.reply(embed);
        }

        let game = new Game(row, column);
        game.setPlayers([message.author.id]);
        games.set(message.author.id, game);
        users.set(message.author.id, message.author.id);
        embed.setDescription(`Please wait for users to join the game.`);
        return message.reply(embed);
    }
}