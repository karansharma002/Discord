const fs = require('fs');

const prefix = process.env.PREFIX;
const token = process.env.TOKEN;

const Discord = require('discord.js');
const client = new Discord.Client();
client.commands = new Discord.Collection();
const cooldowns = new Discord.Collection();
// game rooms, stores game creator and players in the room
const games = new Discord.Collection();
// stores users and the user's room they are in
const users = new Discord.Collection();

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (file of commandFiles) {
    const command = require(`./commands/${file}`);
    client.commands.set(command.name, command);
}

client.once('ready', () => {
    console.log("Ready!");
});

client.on('message', message => {
    if (!message.content.startsWith(prefix) || message.author.bot) return;

    const args = message.content.substring(prefix.length).split(/ +/);
    const commandName = args.shift().toLowerCase();

    const command = client.commands.get(commandName) || client.commands.find(cmd => cmd.aliases && cmd.aliases.includes(commandName));

    const embed = new Discord.MessageEmbed();

    if (!command) {
        embed.setDescription(`That command does not exist. Use *!help* for more.`);
        return message.reply(embed);
    }    

    if ((command.args && !args.length) || (command.users && !message.mentions.users.first())) {
        let reply = "Incorrect usage. Use *!help* for more.";
        if (command.usage) {
            reply += `\nUsage: *${prefix}${command.name} ${command.usage}*`;
    
        }
        embed.setDescription(reply);
        return message.reply(embed);
    }

    if (!cooldowns.has(command.name)) {
        cooldowns.set(command.name, new Discord.Collection());
    }

    const now = Date.now();
    const timestamps = cooldowns.get(command.name);
    const cooldownAmount = (command.cooldown || 1) * 1000;

    if (timestamps.has(message.author.id)) {
        const expirationTime = timestamps.get(message.author.id) + cooldownAmount;

        if (now < expirationTime) {
            const timeLeft = (expirationTime - now) / 1000;
            embed.setDescription(`Please wait ${timeLeft.toFixed(1)} more second(s) before reusing the *${command.name}* command. `);
            return message.reply(embed);
        }
    }

    timestamps.set(message.author.id, now);
    setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);

    try {
        command.execute(message, args, games, users);
    } catch (error) {
        console.log(error);
        embed.setDescription('This command does not exist. Use !help for more.');
        return message.reply(embed);
    }
});

client.login(token)
