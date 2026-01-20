import polars as pl
from rich.console import Console
from rich.table import Table

console = Console()

# 1. Datos falsos
data = {"producto": ["Laptop", "Mouse", None], "precio": [1200, -5, 50]}
df = pl.DataFrame(data)

# 2. Simular validación
table = Table(title="Purr Reporte de Calidad")
table.add_column("Fila", style="cyan")
table.add_column("Error", style="magenta")

# Regla: Precio no puede ser negativo
errors = df.filter(pl.col("precio") < 0)

for row in errors.rows(named=True):
    # Aquí iría lógica real, esto es visualización
    table.add_row("1", f"Precio negativo detectado: {row['precio']}")

console.print(table)