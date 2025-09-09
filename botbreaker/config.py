from pathlib import Path
from rich import print
import configparser

class Config:
    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or self.get_default_config_dir()
        self.config_path = Path(self.config_dir)/"config.ini"
        self.config = configparser.ConfigParser()
        
    def get_default_config_dir(self) -> str:
        home_dir = Path.home()
        config_dir = home_dir/".config"/"botbreaker"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir)
    
    def load_config(self) -> bool:
        if self.config_path.exists():
            self.config.read(self.config_path)
            return True
        
        return False
    
    def save_config(self, api_id: int, api_hash: str) -> None:
        self.config['Telegram'] = {
            'api_id': str(api_id),
            'api_hash': api_hash
        }
        
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
    
    def get_api_credentials(self) -> tuple:
        if not self.load_config():
            return None, None
        
        try:
            api_id = int(self.config['Telegram']['api_id'])
            api_hash = self.config['Telegram']['api_hash']
            print(f"[green][INFO][/green] Use config from [yellow]{self.config_path}[/yellow]")
            return api_id, api_hash
        except (KeyError, ValueError):
            return None, None
    
    def setup_config(self) -> tuple:
        print("Telegram API configuration")
        
        try:
            api_id = int(input("Enter your API ID: "))
            api_hash = input("Enter your API Hash: ")
            
            self.save_config(api_id, api_hash)
            print(f"[green][INFO][/green] Configuration saved to [yellow]{self.config_path}[/yellow]")
            return api_id, api_hash
            
        except ValueError:
            print("[red][ERROR][/red] API ID must be a number")
            return None, None