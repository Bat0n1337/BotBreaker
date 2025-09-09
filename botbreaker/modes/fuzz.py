from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from telethon import TelegramClient
from typing import Tuple, List, Dict
from itertools import product
from rich import print
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import asyncio, sys, re

class Fuzzer:
    def __init__(self, client: TelegramClient, target: str, command: str, wordlists: List[Tuple[str, str]], rate: int = 1, timeout: int = 10) -> None:
        self.client = client
        self.target = target
        self.command = command
        self.rate = rate
        self.timeout = timeout
        self.wordlists = wordlists
        self.keywords = list(set(re.findall(r'[A-Z_][A-Z0-9_]*', self.command)))

        if not self.keywords:
            print(f"[red][ERROR][/red] No fuzzing parameters found in command")
            sys.exit()
        
        self.payloads = self.load_wordlists()
    
    def load_wordlists(self) -> List[Dict[str, str]]:
        loaded_wordlists = {}
        
        for path, keyword in self.wordlists:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    payloads = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                loaded_wordlists[keyword] = payloads
                print(f"[green][INFO][/green] Loaded [cyan]{len(payloads)}[/cyan] payloads for [yellow]{keyword}[/yellow] from [yellow]{path}[/yellow]")
            except Exception as e:
                print(f"[red][ERROR][/red] Error loading wordlist {path}: [red]{e}[/red]")
                sys.exit()
        
        for keyword in self.keywords:
            if keyword not in loaded_wordlists:
                print(f"[red][ERROR][/red] No wordlist provided for keyword [yellow]{keyword}[/yellow]")
                sys.exit()
        
        keys = list(loaded_wordlists.keys())
        values = list(loaded_wordlists.values())
        
        combinations = []
        for combination in product(*values):
            payload_dict = dict(zip(keys, combination))
            combinations.append(payload_dict)
        
        print(f"[green][INFO][/green] Generated [cyan]{len(combinations)}[/cyan] total combinations")
        return combinations
    
    def apply_payloads(self, payload_dict: Dict[str, str]) -> str:
        result = self.command
        for keyword, payload in payload_dict.items():
            result = result.replace(keyword, payload)
        return result
        
    async def run(self) -> None:
        try:
            entity = await self.client.get_entity(self.target)
            if entity.bot:
                print(f"[green][INFO][/green] Starting fuzzing the [blue]@{entity.username or entity.usernames[0].username}[/blue]")
        except:
            print(f"[red][ERROR][/red] Bot with username [blue]@{self.target}[/blue] not found")
            sys.exit()
        
        progress = Progress(
            TextColumn("[bold blue]{task.fields[payload]}", justify="right"),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        )
        
        task = progress.add_task("", total=len(self.payloads), payload="Starting...")

        stats = {
            "sent": 0,
            "errors": 0,
            "vulnerabilities": 0
        }
        
        with Live(progress, refresh_per_second=10):
            for i, payload_dict in enumerate(self.payloads):
                fuzzed_command = self.apply_payloads(payload_dict)
                
                progress.update(task, advance=1, payload=fuzzed_command[:50] + "..." if len(fuzzed_command) > 50 else fuzzed_command)
                
                try:
                    await self.client.send_message(self.target, fuzzed_command)
                    stats["sent"] += 1

                    if i != len(self.payloads) - 1:
                        await asyncio.sleep(self.rate)
                    
                except Exception as e:
                    stats["errors"] += 1
            
            progress.update(task, payload="Complete!")
        
        self.show_summary(stats)
    
    def show_summary(self, stats: Dict[str, int]) -> None:
        table = Table(title="Fuzzing Summary", show_header=False)
        
        table.add_row("Total payloads", f"[bold cyan]{len(self.payloads)}[/bold cyan]")
        table.add_row("Sent messages", f"[bold green]{stats['sent']}[/bold green]")
        table.add_row("Errors", f"[bold red]{stats['errors']}[/bold red]")
        
        print()
        print(table)
        print()




