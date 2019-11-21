import os
import discord
from discord.ext import commands
from beginner.cog import Cog
from functools import lru_cache


class BeginnerCog(Cog):
	@Cog.listener()
	async def on_ready(self):
		print("Bot is ready.")

	@staticmethod
	@lru_cache()
	def get_client() -> commands.Bot:
		client = commands.Bot(
			command_prefix="!",
			activity=discord.Activity(
				name="for '!help' to show you all commands",
				type=discord.ActivityType.watching
			)
		)
		client.remove_command('help')
		return client

	@staticmethod
	@lru_cache()
	def get_token():
		if "DISCORD_TOKEN" in os.environ:
			return os.environ.get("DISCORD_TOKEN")
		with open("bot.token", "r") as token_file:
			return token_file.readline().strip()

	@staticmethod
	@lru_cache()
	def is_dev_env():
		return not os.environ.get("PRODUCTION_BOT", False)

	@staticmethod
	def load_cogs(client):
		client.load_extension('beginner.cogs.google')
		client.load_extension('beginner.cogs.help')
		client.load_extension('beginner.cogs.python')
		client.load_extension('beginner.cogs.rules')

		if BeginnerCog.is_dev_env():
			import beginner.devcog
			client.add_cog(beginner.devcog.DevCog(client))

		client.add_cog(BeginnerCog(client))
