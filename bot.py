import discord
from discord import app_commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1547427404379590757

intents = discord.Intents.default()
intents.message_content = True


class MeuBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)

        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

        print("Comandos sincronizados!")


bot = MeuBot()


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


# =========================
# COMANDO DE REGRAS
# =========================

@bot.tree.command(
    name="regras",
    description="Veja o Regulamento Geral do Francisco Morato Roleplay"
)
async def regras(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📜 REGULAMENTO GERAL — FRANCISCO MORATO ROLEPLAY",
        description=(
            "_Estabelece as regras gerais, procedimentos internos "
            "e padrões de conduta do servidor._"
        ),
        color=discord.Color.red()
    )

    embed.add_field(
        name="CAPÍTULO I — DAS REGRAS GERAIS",
        value=(
            "**Art. 1º**\n"
            "Todos os jogadores deverão manter uma conduta respeitosa "
            "e adequada dentro do servidor.\n\n"

            "**Art. 2º — Regras Adicionais**\n"
            "I — Ninguém irá receber mod além da equipe administrativa;\n"
            "II — Proibido uso de Charmusic;\n"
            "III — Evitar atitudes que prejudiquem a experiência dos demais jogadores;\n"
            "IV — Proibido usar o soco para matar sem motivo."
        ),
        inline=False
    )

    embed.add_field(
        name="CAPÍTULO I — DAS PROIBIÇÕES",
        value=(
            "**Art. 3º — Das Proibições**\n\n"
            "I — É proibido utilizar comandos administrativos de forma indevida;\n"
            "II — É proibido utilizar bugs ou falhas do servidor para obter vantagem;\n"
            "III — É proibido atrapalhar ações de outros jogadores;\n"
            "IV — É proibido utilizar informações externas dentro do RP;\n"
            "V — É proibido praticar qualquer tipo de abuso dentro do servidor;\n"
            "VI — É proibido colocar pessoas em um time por serem amigos. "
            "Exemplo: um amigo seu é PM em outro RP e você quer colocá-lo na PM deste RP;\n"
            "VII — É proibido falar conversas fora do contexto no H "
            "e em outros comandos de mensagens em geral."
        ),
        inline=False
    )

    embed.add_field(
        name="CAPÍTULO II — IMPORTANTE",
        value=(
            "**Art. 4º**\n"
            "Todos os jogadores deverão manter o realismo e a coerência "
            "durante as ações.\n\n"

            "**Art. 5º — É proibido:**\n"
            "I — Realizar ações sem sentido dentro do RP;\n"
            "II — Forçar situações contra outros jogadores;\n"
            "III — Interromper ações sem motivo válido;\n"
            "IV — Sair do personagem propositalmente para obter vantagem;\n"
            "V — Utilizar informações obtidas fora do RP;\n"
            "VI — Usar Skin irrealista/zoeira no RP."
        ),
        inline=False
    )

    embed.add_field(
        name="CAPÍTULO III — DOS VEÍCULOS",
        value=(
            "**Art. 6º**\n"
            "Os veículos deverão ser utilizados de maneira coerente com o RP.\n\n"
            "I — É proibido dirigir de forma propositalmente irresponsável sem contexto;\n"
            "II — É proibido utilizar veículos para atrapalhar outros jogadores;\n"
            "III — Ande com responsabilidade para não quebrar seu veículo."
        ),
        inline=False
    )

    embed.add_field(
        name="⚠️ AVISO IMPORTANTE",
        value=(
            "***A alegação de desconhecimento das regras não isenta "
            "o jogador de suas responsabilidades.***\n\n"
            "<@&1547427404379590763>"
        ),
        inline=False
    )

    embed.set_footer(
        text="Francisco Morato - RP • Regulamento Geral"
    )

    await interaction.response.send_message(embed=embed)


# =========================
# COMANDO DE IDIOMA
# =========================

@bot.tree.command(
    name="idioma",
    description="Escolha o idioma do bot"
)
@app_commands.describe(lingua="Escolha o idioma")
@app_commands.choices(
    lingua=[
        app_commands.Choice(
            name="English 🇺🇸",
            value="ingles"
        ),
        app_commands.Choice(
            name="Español 🇪🇸",
            value="espanhol"
        )
    ]
)
async def idioma(
    interaction: discord.Interaction,
    lingua: app_commands.Choice[str]
):

    if lingua.value == "ingles":
        mensagem = "🇺🇸 Language changed to English!"

    else:
        mensagem = "🇪🇸 ¡Idioma cambiado a español!"

    await interaction.response.send_message(mensagem)


# =========================
# INICIAR BOT
# =========================

# =========================
# SISTEMA DE TICKETS
# =========================

CATEGORIA_TICKETS = 1547427407399485472

CARGOS_EQUIPE = [
    1547427404463603789,
    1547427404463603788,
    1547427404463603790
]


class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Denúncias",
                description="Faça uma denúncia contra um jogador.",
                emoji="🔨",
                value="denuncias"
            ),
            discord.SelectOption(
                label="Suporte",
                description="Precisa de ajuda? Abra um atendimento.",
                emoji="🆘",
                value="suporte"
            ),
            discord.SelectOption(
                label="Denúncias Staff",
                description="Denúncia ou reclamação sobre um membro da Staff.",
                emoji="👮",
                value="denuncias_staff"
            )
        ]

        super().__init__(
            placeholder="🎫 Selecione o tipo de atendimento...",
            options=options,
            custom_id="ticket_categoria"
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild

        if guild is None:
            return

        categoria = guild.get_channel(CATEGORIA_TICKETS)

        if categoria is None:
            await interaction.response.send_message(
                "❌ A categoria de tickets não foi encontrada.",
                ephemeral=True
            )
            return

        nomes = {
            "denuncias": "🔨 Denúncia",
            "suporte": "🆘 Suporte",
            "denuncias_staff": "👮 Denúncia Staff"
        }

        nome_ticket = nomes[self.values[0]]

        # Impede o usuário de abrir mais de um ticket
        for canal in categoria.channels:
            if canal.name.endswith(str(interaction.user.id)):
                await interaction.response.send_message(
                    f"❌ Você já possui um ticket aberto: {canal.mention}",
                    ephemeral=True
                )
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True
            ),

            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                read_message_history=True
            )
        }

        # Permissões da equipe
        for cargo_id in CARGOS_EQUIPE:
            cargo = guild.get_role(cargo_id)

            if cargo:
                overwrites[cargo] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    manage_channels=True
                )

        canal = await guild.create_text_channel(
            name=f"🎫・ticket-{interaction.user.id}",
            category=categoria,
            overwrites=overwrites,
            topic=f"{nome_ticket} | Usuário: {interaction.user}"
        )

        embed = discord.Embed(
            title=f"{nome_ticket}",
            description=(
                f"Olá, {interaction.user.mention}! 👋\n\n"
                "Seu atendimento foi criado.\n"
                "Explique com detalhes o motivo do seu ticket "
                "e aguarde a equipe responsável.\n\n"
                "🔒 Quando o atendimento terminar, utilize o botão "
                "**Fechar Ticket**."
            ),
            color=discord.Color.red()
        )

        embed.set_footer(
            text="Francisco Morato - RP • Sistema de Tickets"
        )

        view = FecharTicketView()

        await canal.send(
            content=f"{interaction.user.mention}",
            embed=embed,
            view=view
        )

        await interaction.response.send_message(
            f"✅ Seu ticket foi criado: {canal.mention}",
            ephemeral=True
        )


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


class FecharTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Fechar Ticket",
            emoji="🔒",
            style=discord.ButtonStyle.danger,
            custom_id="fechar_ticket"
        )

    async def callback(self, interaction: discord.Interaction):
        canal = interaction.channel

        if canal is None:
            return

        await interaction.response.send_message(
            "🔒 Este ticket será fechado em 5 segundos."
        )

        await asyncio.sleep(5)

        await canal.delete(
            reason=f"Ticket fechado por {interaction.user}"
        )


class FecharTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FecharTicketButton())


@bot.tree.command(
    name="ticket",
    description="Envia o painel para abrir tickets"
)
@app_commands.checks.has_permissions(administrator=True)
async def ticket(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎫 CENTRAL DE ATENDIMENTO",
        description=(
            "**Francisco Morato - RP**\n\n"
            "Precisa de ajuda? Selecione abaixo o tipo de atendimento "
            "que você deseja.\n\n"

            "🔨 **Denúncias**\n"
            "Para denunciar jogadores.\n\n"

            "🆘 **Suporte**\n"
            "Para dúvidas e problemas.\n\n"

            "👮 **Denúncias Staff**\n"
            "Para denúncias ou reclamações relacionadas à Staff.\n\n"

            "👇 **Selecione uma opção no menu abaixo.**"
        ),
        color=discord.Color.red()
    )

    embed.set_footer(
        text="Francisco Morato - RP • Central de Atendimento"
    )

    await interaction.response.send_message(
        embed=embed,
        view=TicketView()
    )
    
if not TOKEN:
    print("ERRO: DISCORD_TOKEN não foi configurado no arquivo .env")
    raise SystemExit

else:
    bot.run(TOKEN)
