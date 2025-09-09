from telethon import TelegramClient
from botbreaker.config import Config
from typing import Optional
from pathlib import Path
from rich import print

class TelegramClientManager:
    def __init__(self, config_dir: Optional[str] = None):
        self.config = Config(config_dir)
        self.client: Optional[TelegramClient] = None
        self.session_path = Path(self.config.config_dir)/"session"
    
    async def initialize_client(self) -> TelegramClient:
        api_id, api_hash = self.config.get_api_credentials()
        
        if api_id is None or api_hash is None:
            api_id, api_hash = self.config.setup_config()
            if api_id is None or api_hash is None:
                raise ValueError("[red][ERROR][/red] Failed to setup Telegram API configuration")
        
        self.client = TelegramClient(
            session=str(self.session_path),
            api_id=api_id,
            api_hash=api_hash,
            system_version='4.16.30-vxCUSTOM'
        )
        
        return self.client
    
    async def get_client(self) -> TelegramClient:
        if self.client is None:
            return await self.initialize_client()
        return self.client
    
    async def start(self) -> None:
        client = await self.get_client()
        await client.start()
        print("[green][INFO][/green] Telegram client started successfully")