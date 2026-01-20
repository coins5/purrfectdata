import typer
from rich.console import Console
from rich.panel import Panel
import time

# Inicializamos la app Typer y la consola Rich
app = typer.Typer(help="🐱 PurrfectData: The data linter that cleans your messy datasets.")
console = Console()

@app.callback()
def callback():
    """
    PurrfectData CLI Tool 🐾
    """
    # Esta función se ejecuta antes de cualquier comando (útil para configs globales)
    pass

@app.command()
def sniff(
    file_path: str = typer.Argument(..., help="Path to the dataset file (CSV, JSON, Parquet)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show all the gritty details")
):
    """
    👃 Sniffs a file looking for hairballs (data errors).
    """
    # Header del comando
    console.print(Panel("🐱 [bold orange1]PurrfectData[/bold orange1] is warming up...", border_style="orange1"))
    
    # Simulación (aquí conectaremos Polars pronto)
    console.print(f"[italic grey50]Target acquired: {file_path}[/italic grey50]")
    
    with console.status("[bold green]Sniffing data...[/bold green]", spinner="dots"):
        time.sleep(1) # Simula carga
        
        # Lógica placeholder
        if "bad" in file_path:
            console.print("\n[bold red]😿 Hiss! Found a hairball![/bold red]")
            console.print("   -> The file smells funny (simulated error).")
        else:
            console.print("\n[bold green]😺 Purrfect! The data looks clean.[/bold green]")

# Esto permite correrlo como script directo si quisieras, pero usaremos 'purf'
if __name__ == "__main__":
    app()