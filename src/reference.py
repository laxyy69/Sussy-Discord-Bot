import discord


class Reference:
    class NoneReference(Exception): 
        def __init__(self, description: str=None) -> None:
            super().__init__(description or "You didn't reply to a message.")

    def __init__(self, client) -> None:
        self.client = client


    async def __call__(self, message: discord.Message) -> discord.Message:
        self.message = message
        self.reference = message.reference

        if self.reference is None:
            raise self.NoneReference()

        return await self.get_reference()


    async def get_reference(self) -> discord.Message:
        self.channel = self.client.get_channel(self.reference.channel_id)

        message: discord.Message = await self.channel.fetch_message(self.reference.message_id)

        return message


    async def __aenter__(self) -> discord.Message:
        self.channel = self.client.get_channel(self.reference.channel_id)

        return await self.channel.fetch_message(self.reference.message_id)

    async def __aexit__(self, *args) -> None:
        return False