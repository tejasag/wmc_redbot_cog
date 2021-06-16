import discord
from redbot.core import commands, Config
from typing import Optional


class ProfileCogWmc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=838844992296969)
        default_user = {
            "profile": {
                "shell": None,
                "distro": None,
                "bar": None,
                "system_specs": None,
                "wm_de": None,
                "dotfiles": None,
                "terminal": None,
                "screenshot_link": None,
                "editor": None,
                "theme": None,
            }
        }
        self.config.register_user(**default_user)

    @commands.group(name="profile", invoke_without_command=True)
    async def profile(self, ctx, member: Optional[discord.User]):
        if not member:
            member = ctx.author

        embed = discord.Embed(
            title=f"{member.name}'s profile", color=discord.Color(0).from_rgb(47, 48, 55)
        )
        data = await self.config.user(member).profile()
        for k, v in data.items():
            if not v:
                continue
            if k == "screenshot_link" and v is not None:    
                embed.set_image(url=v)
                continue
            embed.add_field(name=f"**{k}**", value=v, inline=True)
        embed.set_author(name=member.name, icon_url=member.avatar_url_as())
        await ctx.reply(embed=embed)

    @profile.command(name="set")
    async def set(self, ctx, field=None, *, value=None):
        if not field:
            return await ctx.reply("Choose one from: `shell`, `distro`, `bar`, `system_specs`, `wm_de`, `dotfiles`, `terminal`, `screenshot_link`, `editor`, `theme`\nCommand Usage: `-profile set [field] [value]`")
        field = field.lower()
        fields = [
            "shell",
            "distro",
            "bar",
            "system_specs",
            "systemspecs",
            "wm_de",
            "wm",
            "de",
            "desktopenvironment",
            "windowmanager",
            "dotfiles",
            "terminal",
            "screenshot_link",
            "screenshot",
            "image",
            "editor",
            "theme",
        ]

        if field not in fields:
            return await ctx.send(
                f"Bruh, you cannot set that ://\n Choose one from: `shell`, `distro`, `bar`, `system_specs`, `wm_de`, `dotfiles`, `terminal`, `screenshot_link`, `editor`, `theme`"
            )
        

        field = "system_specs" if field in ["system_specs", "systemspecs"] else field
        field = (
            "wm_de"
            if field in ["wm_de", "wm", "de", "desktopenvironment", "windowmanager"]
            else field
        )
        field = "screenshot_link" if field in ["screenshot_link", "screenshot", "image"] else field
        if field == "screenshot_link":
            if not (value.startswith("https://") and  (value.endswith("png") or value.endswith("jpg") or value.endswith("jpeg") or value.endswith("gif") or value.endswith("webp"))):
               return await ctx.send("Please enter a valid image/gif url for profile screenshot!")
        old = await self.config.user(ctx.author).profile()

        if not value:
            old[field] = None
            await self.config.user(ctx.author).profile.set(old)
            return ctx.reply(f"Done! I have reset the `{field} field!`")

        old[field] = value
        await self.config.user(ctx.author).profile.set(old)

        embed = discord.Embed(
            title=f"Done!",
            description=f"The value of `{field}` is now `{value}`",
            color=discord.Color(0).from_rgb(47, 48, 55),
        )
        await ctx.reply(embed=embed)


