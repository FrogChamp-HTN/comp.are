import discord
import matplotlib.pyplot as plt
import dotenv
import datetime
import os
from urllib.request import urlopen
import json

from discord.ext import commands
from math import pi
dotenv.load_dotenv()

# retrieve discord and DMOJ api key
DISCORD_TOKEN = os.environ.get("bot-token")
# DMOJ_API = os.environ.get("dmoj-api")
# set prefix
print(DISCORD_TOKEN)
bot = commands.Bot(command_prefix="!")

def filterAC(sub):
	return sub['result'] == 'AC'

@bot.command(name="cache")
async def cache(ctx, *username_args):
	print("Command: cache")
	username = username_args[0]

	#request for user info
	userresponse = urlopen("https://dmoj.ca/api/user/info/" + username)
	userdata = json.loads(userresponse.read())
	subs = []
	
	for i in range(5):
		submissionresponse = urlopen("https://dmoj.ca/api/v2/submissions?user=" + username + "&page=" + str(i+1))
		submissiondata = json.loads(submissionresponse.read())
		subs.extend(submissiondata['data']['objects'])

		if not submissiondata['data']['has_more']:
			break
	
	# filter only AC
	ac = list(filter(filterAC, subs))

	languages = {}

	for submission in ac:
		if submission["language"] in languages:
			languages[submission["language"]] += 1
		else:
			languages[submission["language"]] = 1
	
	# remove nested data from userdata
	userdata["contests"] = None

	# add in more data to profile
	userdata["languages"] = json.dumps(languages)
	userdata["solved"] = len(ac)
	userdata["username"] = username

	#print("[" + json.dumps(userdata) + "]")

	# send all of this to Dropbase



@bot.command(name="plot")
async def plot(ctx, *username_args):
	# figure and subplot
	fig = plt.figure(figsize=(6,6))
	ax = plt.subplot(polar="True")

	# gen categories and number of categories
	categories = ["A", "B", "C", "D", "E"]
	N = len(categories)
	# gen result
	# results = query(username_args[0])
	results = [100, 200, 150, 200, 120]
	results += results[:1]
	# gen angles
	angles = [n / float(N) * 2 * pi for n in range(N)]
	angles += angles[:1]
	# gen y ticks
	yDist = [i for i in range(0, 200, 50)]
	# fill the in area
	plt.polar(angles, results, marker='.')
	plt.fill(angles, results, alpha=0.3)
	# x and y ticks
	plt.xticks(angles[:-1], categories)
	ax.set_rlabel_position(0)
	plt.yticks(yDist, color="grey", size=10)
	plt.ylim(0, 210)
	plt.savefig("tmp.png")
	# generate the embed
	embed = discord.Embed(
			title = "Status",
			description = "Online",
			colour = discord.Colour.blue()
	)
	embed.set_thumbnail(url="")
	return await ctx.send(embed=embed)

def main():
	with open("log.txt", "w") as log:
		log.write(f"[{datetime.datetime.now()}] Bot Started! Waiting for Query...\n")
	bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
	main()