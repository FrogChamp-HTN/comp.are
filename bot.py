import discord
import matplotlib.pyplot as plt
import dotenv
import datetime
import os
import io
import json
import dropbase

from urllib.request import urlopen
from discord.ext import commands
from matplotlib import gridspec
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
	jobid = dropbase.upload_file_via_presigned_url("[" + json.dumps(userdata) + "]")
	print(jobid)
	dropbase.get_status(jobid)

	print(dropbase.query_db("users").text)

	await ctx.send("Done!")

def process(json_file):
	# read json
	languages = json.loads(json_file["languages"])
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
	gs = gridspec.GridSpec(2, 1, height_ratios = [1, 3])
	ax = plt.subplot(gs[1], polar="True")
	ax.set_theta_offset(pi / 2)
	ax.set_theta_direction(-1)
	bx = plt.subplot(gs[0])
	# get the query result
	# results = query(username_args[0])
	# gen color array
	colors = ['r', 'g', 'b']
	# gen categories and number of categories
	categories = [" C++", "C", "Python", "Java"]
	print(categories)
	N = len(categories)
	# generate results from request
	results = []
	languages = []

	a = open("userexample.json", "r")
	b = open("anotherexample.json", "r")
	results = [json.load(a)[0], json.load(b)[0]]
	# for user in usernames_args:
	# 	results.append(query(user)[0])

	# plot the other stuff (point, performance point, problem solved)
	barData = []
	for i in range(len(usernames_args)):
		barData.append([usernames_args[i], int(results[i]["points"] + .5), int(results[i]["performance_points"] +.5), results[i]["solved"]])
	bx.axis('tight')
	bx.axis('off')
	tb = bx.table(cellText=barData, colLabels=("User", "Points", "Weighted Points", "Solved"), loc='center')

	# initialize the upper bound for the graph
	for result in results:
		languages.append(process(result))
	maxVal = 0
	# gen angles
	angles = [n / float(N) * 2 * pi for n in range(N)]
	angles += angles[:1]
	# graph the data
	for i in range(len(languages)):
		print(languages[i], colors[i], usernames_args[i])
		ax.plot(angles, languages[i], colors[i], linestyle='solid', label=usernames_args[i])
		ax.fill(angles, languages[i], colors[i], alpha=0.3)
		maxVal = max(maxVal, max(languages[i]))
		# print(max(a[i]))
	# gen y ticks
	yDist = [i for i in range(0, maxVal, maxVal//4)]
	# x and y ticks
	ax.set_xticks(angles[:-1])
	ax.set_xticklabels(categories)
	for tick in ax.xaxis.get_major_ticks():
		tick.label.set_fontsize(8)
	ax.set_rlabel_position(0)
	ax.set_yticks(yDist)
	for tick in ax.yaxis.get_major_ticks():
		tick.label.set_fontsize(8)
	# ax.set_ytickslabels(size=10)

	ax.set_ylim(0, maxVal*1.1)
	# graph :monkey:
	ax.legend(loc='lower right', bbox_to_anchor=(.9, .9), fontsize='small')
	plt.savefig("tmp.png")
	# generate the embed
	embed = discord.Embed(
			title = "result",
			colour = discord.Colour.blue()
	)
	# add the image onto the embed
	with open('tmp.png', 'rb') as img:
		# io.BytesIO(img.read())
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