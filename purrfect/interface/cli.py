import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional

# Internal Imports (Clean Architecture Wiring)
from purrfect.infrastructure.polars_loader import PolarsDataLoader
from purrfect.infrastructure.yaml_parser import YamlParser
from purrfect.infrastructure.profiler import PolarsProfiler
from purrfect.domain.scoring import ScoreCalculator
from purrfect.application.sniffer import DataSniffer
from purrfect.domain.entities import Hairball
from purrfect.application.discovery import DiscoveryService

app = typer.Typer(help="🐱 PurrfectData: The data linter that cleans your messy datasets.")
console = Console()

@app.callback()
def callback():
    """
    Data Quality Tool for Messy Datasets.
    """


@app.command()
def suggest(
    file_path: str = typer.Argument(..., help="Path to the dataset file (CSV, JSON)"),
    output: str = typer.Option("suggested_rules.yaml", "--output", "-o", help="Path to save suggested rules")
):
    """
    🔮 Infers rules from your data and suggests a configuration.
    """
    console.print(Panel("🐱 [bold magenta]PurrfectData[/bold magenta] is smelling your data...", border_style="magenta"))

    try:
        service = DiscoveryService()
        
        with console.status("[bold green]Analyzing patterns...[/bold green]", spinner="dots"):
             rules = service.run(file_path, output)

        console.print(f"\n[bold green]😺 Done! I found {len(rules)} potential rules.[/bold green]")
        
        # Preview
        table = Table(title="Suggested Rules", border_style="magenta")
        table.add_column("Column", style="cyan")
        table.add_column("Rule Type", style="yellow")
        table.add_column("Params", style="dim")

        for r in rules:
            table.add_row(
                r.column_name,
                r.rule_type.name,
                str(r.params) if r.params else ""
            )
        
        console.print(table)
        console.print(f"\n[bold blue]💾 Saved suggestions to {output}[/bold blue]")
        console.print(f"Run [bold white]purf sniff {file_path} --rules {output}[/bold white] to test them!")

    except Exception as e:
        console.print(f"\n[bold red]😿 Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def sniff(
    file_path: str = typer.Argument(..., help="Path to the dataset file (CSV, JSON)"),
    rules_path: str = typer.Option(..., "--rules", "-r", help="Path to the rules.yaml file"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Path to save HTML report"),
):
    """
    👃 Sniffs a file looking for hairballs (data errors) based on the provided rules.
    """
    console.print(Panel("🐱 [bold orange1]PurrfectData[/bold orange1] is starting...", border_style="orange1"))

    # 1. Dependency Injection (Manual)
    loader = PolarsDataLoader()
    parser = YamlParser()
    profiler = PolarsProfiler()
    scorer = ScoreCalculator()
    sniffer = DataSniffer()

    # 2. Execution
    try:
        # Load Rules
        with console.status("[bold green]Reading rules...[/bold green]", spinner="dots"):
            rules = parser.parse(rules_path)
        
        console.print(f"[green]✓ loaded {len(rules)} rules from {rules_path}[/green]")

        # Load Data
        with console.status(f"[bold green]Loading data from {file_path}...[/bold green]", spinner="dots"):
            data = loader.load(file_path)
        
        console.print(f"[green]✓ loaded data with {data.height} rows[/green]")

        # Profile Data
        with console.status("[bold green]Profiling data...[/bold green]", spinner="dots"):
            profile = profiler.profile(data)

        # Sniff
        with console.status("[bold green]Sniffing for hairballs...[/bold green]", spinner="dots"):
            hairballs = sniffer.sniff(data, rules)

        # Calculate Score
        quality_score = scorer.calculate(profile, hairballs)

    except Exception as e:
        console.print(f"\n[bold red]😿 Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    # 3. Present Results
    
    # Display Score
    console.print(f"\n[bold]Quality Score:[/bold] {quality_score.value}/100")
    if quality_score.grade == 'A':
        grade_color = "green"
    elif quality_score.grade == 'B':
        grade_color = "yellow"
    else:
        grade_color = "red"
        
    console.print(f"[bold]Grade:[/bold] [{grade_color}]{quality_score.grade}[/{grade_color}]")

    if output:
        try:
             # Lazy import or just imported at top
            from purrfect.infrastructure.html_reporter import HTMLReporter
            reporter = HTMLReporter()
            reporter.generate_report(hairballs, profile, quality_score, output)
            console.print(f"\n[bold blue]📄 HTML report generated at {output}[/bold blue]")
        except Exception as e:
             console.print(f"[bold red]⚠️ Failed to generate HTML report:[/bold red] {e}")

    if not hairballs:
         console.print("\n[bold green]😺 Purrfect! No hairballs found. The data is clean.[/bold green]")
         return

    console.print(f"\n[bold red]😿 Found {len(hairballs)} hairballs![/bold red]")
    
    table = Table(title="Hairballs Detected", border_style="red")
    table.add_column("Row Index", style="cyan", justify="right")
    table.add_column("Column", style="magenta")
    table.add_column("Issue", style="white")
    table.add_column("Rule", style="dim")

    for h in hairballs:
        table.add_row(
            str(h.row_index),
            h.column,
            h.message,
            h.rule_type.name if h.rule_type else "UNKNOWN"
        )

    console.print(table)
    raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
