import discord
import matplotlib.pyplot as plt
import dotenv
import datetime
import os
import io
import json

from urllib.request import urlopen
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

def filter(json_file):
	# read json
	results = json.load(json_file)[0]
	languages = json.loads(results["languages"])
	# calc values
	values = [0 for i in range(4)]
	for key, value in languages.items():
		if "cpp" in key.lower() or "clang++" in key.lower():
			values[0] += value
		elif key[0].lower() == "c":
			values[1] += value
		elif key.lower()[:2] == "py":
			values[2] += value
		elif "java" in key.lower():
			values[3] += value
	values += values[:1]
	# return values
	return values

@bot.command(name="plot")
async def plot(ctx, *usernames_args):
	# figure and subplot
	# fig = plt.figure(figsize=(6,6))
	ax = plt.subplot(polar="True")
	# get the query result
	# results = query(username_args[0])
	# gen color array
	color = ['r', 'o', 'y', 'g', 'c', 'b', 'p']
	# gen categories and number of categories
	categories = ["C++", "C", "Python", "Java"]
	print(categories)
	N = len(categories)
	# gen result
	results = []
	for user in usernames_args:
		results.append(process(query(user)))
	# initialize the upper bound for the graph
	maxVal = 0
	# gen angles
	angles = [n / float(N) * 2 * pi for n in range(N)]
	angles += angles[:1]
	# graph the data
	for i in range(len(a)):
		plt.polar(angles, a[i], color[i], linestyle='solid', label=usernames_args[i], marker='.')
		plt.fill(angles, a[i], color[i], alpha=0.3)
		maxVal = max(maxVal, max(a[i]))
		print(max(a[i]))
	# gen y ticks
	yDist = [i for i in range(0, maxVal, maxVal//4)]
	# x and y ticks
	plt.xticks(angles[:-1], categories)
	ax.set_rlabel_position(0)
	plt.yticks(yDist, color="grey", size=10)
	plt.ylim(0, maxVal + 10)
	# graph :monkey:

	plt.legend(loc='lower right', bbox_to_anchor=(.9, .9), fontsize='small')
	plt.savefig("tmp.png")
	# generate the embed
	embed = discord.Embed(
			title = "Status",
			description = "Online",
			colour = discord.Colour.blue()
	)
	# add the image onto the embed
	with open('tmp.png', 'r') as img:
		img = discord.File(io.BytesIO(img.read()), filename='graph.png')
	embed.set_image(url=f'attachment://graph.png',)
	return await ctx.send(embed=embed, file=img)

# start to run the bot
def main():
	with open("log.txt", "w") as log:
		log.write(f"[{datetime.datetime.now()}] Bot Started! Waiting for Query...\n")
	bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
	main()