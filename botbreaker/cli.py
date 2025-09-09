from rich.console import Console
from botbreaker.version import __version__
import click

console = Console(highlight=False)

modes = ["scan", "fuzz"]
default_mode = "fuzz"
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

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option("-t", "--target", type=str, required=True, help="Target bot username.")
@click.option("-m", "--mode", type=click.Choice(modes), default=default_mode, help=f"Operation mode. (default: {default_mode})")
@click.option("-r", "--rate", type=float, default=3, help="Rate of requests per second. (default: 3)")
def cli(target: str, mode: str, rate: float) -> None:
    if target == "fuzz":
        console.print("fuzz")
