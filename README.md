# Comp.are

Our Hack the North 2020++ project was a Discord bot that looks at profiles from an online judge platform (a site to practice competative programming problems) and comprehensively compares them using on a radial plot of favoured programming langauges, ranking, points, and problems solved. This allows users to very quickly compare thier programming language proficiencies, and their competance in competative porgramming.

## Inspiration

We usually have an only general idea about what we langauges friends and people have just met use or are good at. Knowing each other's strenghts and weaknesses is key to having a functional team project, we thought, so we asked ourselves: where might there be data that could help us make this process easier? Our solution: use data from a popular local competative programming judge, and and use that to have a visaul representation of a person's skills!

## What it does

Our project comes in the form of a Discord bot, which can act as a REPL like enviroment where many people can interact with the bot. It uses the judge, [DM::OJ](https://dmoj.ca) to gather data about specific profiles on the site, and then on request can create a graphic comparing the skills of two or more users.

## How We built it

We used Discord.py as the library for handling the bot logic. For API calles to both DM::OJ and Dropbase, we used native Python. We used Dropbase here as a sort of online Postgres database, where we could upload user data once to Dropbase to make comparisons between profiles already in the database very fast. Finally, for visualisation, we used Python's matplotlib library.

## Challenges I ran into

Dropbase itself is a fairly new product, which meant having many bugs especially since we were useing the Postgres API, which was in Beta. The challenge here was the extra debugging, with the help of the friendly Dropbase reps on the Hack the North Discord server. Eventually, most of the problems we were having with the API were solved.

## Accomplishments that I'm proud of

What I personally am proud of is making such a complicated internet scheme into realiliy. As can bee seen in the image below,
writing the different interactions between each server was very difficult, and managing all of the possible exceptions was daunting to say the least. We overcame this obsticle, however, to have an effective finished product.
![Scheme](https://cdn.discordapp.com/attachments/766301767540408371/800282442808033290/generalmodel2.png)

## What I learned

I learned how to use Discord.py, and how to do internet networking in Python as well. I also learned a bit about collaberation thourgh git, such as merging, which is rare because I usually work alone.

I also learned not to commit my Discord Bot token on a public repo. Discord messaged the creator of the bot in our team almost immedietly saying that it was compromised!

## What's next for Comp.are

Some next steps would be obviously adding in more depth to our analysis. We could, as we were initially planning to do, include problem types, which would be a better indicator of area of skill. We could also add info from other popular judges such as Codeforces, making our bot more acessable.