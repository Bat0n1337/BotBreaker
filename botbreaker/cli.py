from botbreaker.client import TelegramClientManager
from botbreaker.modes.fuzz import Fuzzer
from botbreaker.version import __version__
from rich.console import Console
import click, asyncio

console = Console(highlight=False)
client_manager = TelegramClientManager()

banner = f"""
'││              ││    '││                           '││                    
 ││              ││     ││                            ││                    
 ││''│, .│''│, ''││''   ││''│, '││''│ .│''│,  '''│.   ││ ╱╱`  .│''│, '││''│ 
 ││  ││ ││  ││   ││     ││  ││  ││    ││..││ .│''││   ││<<    ││..││  ││    
.││..│' `│..│'   `│..' .││..│' .││.   `│...  `│..││. .││ ╲╲.  `│...  .││.   
                                                                            
               v{__version__}                             by @Bat0n1337                                        
"""

def print_banner() -> None:
    console.print(banner, style="bold")

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.pass_context
def cli(ctx: click.Context) -> None:
    pass
  
@cli.command()
@click.option("-t", "--target", type=str, required=True, help="Target bot username (e.g., BotFather).")
@click.option("-c", "--command", type=str, required=True, help="Command with placeholders (e.g., FUZZ, USERNAME).")
@click.option("-w", "--wordlist", multiple=True, required=True, help="Wordlist in format path or path:keyword (e.g., wordlist.txt, wordlist.txt:USERNAME).")
@click.option("-r", "--rate", type=int, default=1, help="Rate of requests per second (default: 1).")
@click.option("--timeout", type=int, default=10, help="Time to wait in seconds before timeout (default: 10).")
@click.pass_context
def fuzz(ctx: click.Context, target: str, command: str, wordlist: str, rate: int, timeout: int) -> None:
    client_manager = TelegramClientManager()

    wordlists = []
    for w in wordlist:
        if ':' in w:
            path, keyword = w.split(':', 1)
            wordlists.append((path, keyword))
        else:
            wordlists.append((w, "FUZZ"))
 
    async def run_fuzz() -> None:
        await client_manager.start()
        client = await client_manager.get_client()
        
        await Fuzzer(client=client, wordlists=wordlists, target=target, command=command, rate=rate, timeout=timeout).run()
    
    asyncio.run(run_fuzz())