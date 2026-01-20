import polars as pl
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

console = Console()

def purf_check():
    # Header
    console.print(Panel.fit("🐱 [bold orange1]PurrfectData[/bold orange1] v0.1\n[italic]Cleaning your messy datasets...[/italic]", border_style="orange1"))

    # Simulación de carga (Gatificación)
    with console.status("[bold green]Sniffing data for hairballs...[/bold green]", spinner="dots"):
        time.sleep(1.5) # Drama effect
        
        # Datos Mock
        data = {"product": ["Catnip", "Laser Pointer", None], "price": [15.50, -5.00, 120.00]}
        df = pl.DataFrame(data)
        
        # Regla: Price > 0
        hairballs = df.filter(pl.col("price") < 0)

    # Tabla de Resultados
    if hairballs.height > 0:
        table = Table(title="😿 Hairballs Detected", border_style="red")
        table.add_column("Row", style="cyan")
        table.add_column("Issue", style="bold red")

        for row in hairballs.rows(named=True):
            table.add_row("2", f"Hiss! Negative price found: {row['price']}")

        console.print(table)
        console.print("\n[bold red]✖ The dataset is not purrfect yet![/bold red]")
    else:
        console.print("\n[bold green]😺 Purrfect! No hairballs found.[/bold green]")

if __name__ == "__main__":
    purf_check()