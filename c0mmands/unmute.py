  async def mute_members(self, message, targets, reason):
		unmutes = []
		mute_role = db.field('SELECT MutedRole FROM guilds WHERE GuildID = ?', message.guild.id)
		for target in targets:
			if not mute_role in target.roles:
        
				if message.guild.me.top_role.position > target.top_role.position:
					role_ids = ",".join([str(r.id) for r in target.roles])
					theRole = message.guild.get_role(int(mute_role))
					await target.add_roles(theRole)
					print("checkpoint 1")
					db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
							   target.id, role_ids, message.guild.id)
					print("checkpoint 2")
					#does this work?/?!?!?!?/1/11//!/1/1/1 yep it just wasn't awaited big bad :(((
					await message.channel.send(f"{target} has been muted (pog)")
					print("checkpoint 3")
					#IT WORKED IT WORKED IT WORKED I REPEAT IT WORKEDkmn
					#time to work on unmute Sadge its ez its legit just remove role it shouldnt have taken us this long for an add role command

					#This is why raw SQL sucks, matt.
					#no :)
					#we are doing indefinente mutes anyway, we dont need an end time column
					#i deleted the db OMEGTALUL
					#i know
					#ik shut up
#wait if theres no muted role set it wont work
					#epic :sunglasses:
					
					db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
							   target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())
					
					
			

					embed = Embed(title="Member muted",
								  colour=0xDD2222,
								  timestamp=datetime.utcnow())

					embed.set_thumbnail(url=target.avatar_url)

					fields = [("Member", target.display_name, False),
							  ("Actioned by", message.author.display_name, False),
							  ("Reason", reason, False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)
					log_channel = message.guild.get_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID  = ?", message.guild.id))

					#It needs to be the role object.
                    
					await log_channel.send(embed=embed)

					if hours:
						unmutes.append(target)
		return unmutes

	@command(name="mute")
	@has_permissions(ban_members=True)
	@bot_has_permissions(manage_roles=True)
	@has_permissions(manage_roles=True, manage_guild=True)
	async def mute_command(self, ctx, targets: Greedy[Member], *,
						   reason: Optional[str] = "No reason provided."):
		if not len(targets):
			await ctx.send("One or more required arguments are missing.")

		else:
			unmutes = await self.mute_members(ctx.message, targets, reason)
			await ctx.send("Action complete.")

			if len(unmutes):
				mute_role = db.field('SELECT MutedRole FROM guilds WHERE GuildID = ?', ctx.guild.id) 
				TheRole = ctx.guild.get_role(int(mute_role))
				for target in targets:
					await target.remove_roles(TheRole)
					db.execute("DELETE FROM mutes WHERE VALUES = (?, ?)", target.id, ctx.guild.id)
					await ctx.send("Unmuted! <:PogU:560267624966258690>")

	@command(name="unmute")
	@has_permissions(ban_members=True)
	@bot_has_permissions(manage_roles=True)
	@has_permissions(manage_roles=True, manage_guild=True)
	async def delmute_command(self, ctx, targets: Greedy[Member]):
		mute_role = db.field('SELECT MutedRole FROM guilds WHERE GuildID = ?', ctx.guild.id) 
		TheRole = ctx.guild.get_role(int(mute_role))
		for target in targets:
			await target.remove_roles(TheRole)
			db.execute("DELETE FROM mutes WHERE VALUES = (?, ?)", target.id, ctx.guild.id)
			await ctx.send("Unmuted! <:PogU:560267624966258690>")
#lmfao xD easy way out 
#idk raw sql so u do this :)
#i think i did it right lol
#       do the other one... :|
#oooooooooooooooooooooooooooooooooooooohkewl :thumsup:
#EZbut we need to get my completion message working 
#yeah it didn't work before sooooo! lmfao
	@mute_command.error
	async def mute_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")
