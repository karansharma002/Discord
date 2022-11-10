const prefix = process.env.PREFIX;
const { MessageEmbed } = require('discord.js');

module.exports = {
    name: 'help',
    aliases: ['h', 'info', 'commands'],
    description: 'List information about all commands.',
    usage: '<command name>(optional)',
    cooldown: 0,
    execute(message, args) { 
        // `!play <size>: sizes can be <4,3>, <5,4>, <6,5>\n` +
        // `!join <user>: eg !join @who\n` + 
        // `!flip <row, column>: flips card in the row and column\n` +
        // `!forfeit: forfeits the game\n` +
        // `!score: shows the current successful matches for all players\n` +
        // `!board: shows the current board\n` +
        // `!players: shows the current players`
        
        const embed = new MessageEmbed();
        const { commands } = message.client

        if (!args.length) {
            embed.setTitle(`Available Commands`);
            embed.setDescription(commands.map(command => `${prefix}${command.name}`).join('\n'));
            embed.setFooter(`\nYou can send *${prefix}help <command name>* for more info!`);
        } else {
            const name = args[0].toLowerCase();
            const command = commands.get(name) || commands.find(cmd => cmd.aliases && cmd.aliases.includes(name));

            if (!command) return message.reply(`That command does not exist. Use *!help* for more.`);

            embed.addField(`Name`, `${command.name}`);
            if (command.aliases) embed.addField(`Aliases`, `${command.aliases.join(', ')}`);
            if (command.description) embed.addField(`Description`, `${command.description}`);
            if (command.usage) embed.addField(`Usage`, `${prefix}${command.name} ${command.usage}`);
        }

        return message.author.send(embed)
        .then(() => {
            if (message.channel.type === "dm") return;
            message.reply(`DM sent.`);
        })
        .catch(error => {
            console.error(`Could not send help DM to ${message.author.tag}.\n`);
            message.reply(`DM was unable to be sent.`);
        })
    }
}
