import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from keep_alive import keep_alive
# Load environment variables
load_dotenv()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
@bot.command(name='key')
async def key_command(ctx):
    """
    Command to copy text from 🔑〡mod-key channel and repost it
    Only users with the 🎓〡Staff role can use this command
    """
    try:
        # Get the guild (server) where the command was executed
        guild = ctx.guild
        if not guild:
            await ctx.send("❌ This command can only be used in a server.")
            return
        # Check if user has the required role
        required_role_name = "🎓〡Staff"
        user_roles = [role.name for role in ctx.author.roles]
        
        if required_role_name not in user_roles:
            await ctx.send(f"❌ You need the '{required_role_name}' role to use this command.")
            logger.info(f"User {ctx.author.name} attempted to use !key without required role")
            return
        # Look for the specific channel by name
        target_channel_name = "🔑〡mod-key"
        target_channel = None
        
        for channel in guild.text_channels:
            if channel.name == target_channel_name:
                target_channel = channel
                break
        
        if not target_channel:
            await ctx.send(f"❌ Channel '{target_channel_name}' not found in this server.")
            logger.warning(f"Channel '{target_channel_name}' not found in guild {guild.name}")
            return
        # Check if bot has permission to read the target channel
        if not target_channel.permissions_for(guild.me).read_messages:
            await ctx.send(f"❌ I don't have permission to read messages from '{target_channel_name}'.")
            logger.warning(f"No read permission for channel '{target_channel_name}' in guild {guild.name}")
            return
        # Get the latest message from the target channel
        try:
            async for message in target_channel.history(limit=1):
                if message.content.strip():  # Check if message has content
                    # Post the message content to the current channel
                    await ctx.send(f"📋 **Message from {target_channel_name}:**\n{message.content}")
                    logger.info(f"Successfully copied message from {target_channel_name} to {ctx.channel.name}")
                    return
                else:
                    await ctx.send(f"❌ The latest message in '{target_channel_name}' is empty or contains no text.")
                    logger.info(f"Latest message in {target_channel_name} is empty")
                    return
            
            # If no messages found
            await ctx.send(f"❌ No messages found in '{target_channel_name}'.")
            logger.info(f"No messages found in channel '{target_channel_name}'")
            
        except discord.Forbidden:
            await ctx.send(f"❌ I don't have permission to read message history from '{target_channel_name}'.")
            logger.warning(f"No history permission for channel '{target_channel_name}'")
        except discord.HTTPException as e:
            await ctx.send("❌ An error occurred while fetching messages.")
            logger.error(f"HTTP error while fetching messages: {e}")
    except Exception as e:
        await ctx.send("❌ An unexpected error occurred while processing the command.")
        logger.error(f"Unexpected error in key_command: {e}")
@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required arguments for this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ I don't have the required permissions to execute this command.")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("❌ This command cannot be used in direct messages.")
    else:
        await ctx.send("❌ An error occurred while executing the command.")
        logger.error(f"Command error: {error}")
def main():
    """Main function to run the bot"""
    # Start the keep-alive web server
    keep_alive()
    
    # Get bot token from environment variables
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not bot_token:
        logger.error("DISCORD_BOT_TOKEN environment variable is not set!")
        print("Error: Please set the DISCORD_BOT_TOKEN environment variable.")
        return
    
    try:
        logger.info("Starting Discord bot...")
        bot.run(bot_token)
    except discord.LoginFailure:
        logger.error("Failed to login - invalid bot token")
        print("Error: Invalid bot token. Please check your DISCORD_BOT_TOKEN.")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Error starting bot: {e}")
if __name__ == "__main__":
    main()
