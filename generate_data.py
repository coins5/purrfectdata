import csv
import random

def generate_csv(filename, is_clean=True, rows=150):
    products = ["Catnip", "Laser Pointer", "Scratcher", "Wool Ball", "Tuna Can", "Mouse Toy"]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "product_name", "price"]) # Header
        
        for i in range(1, rows + 1):
            # Lógica base
            prod = random.choice(products)
            price = round(random.uniform(5.0, 50.0), 2)
            
            if not is_clean:
                # Inyectar "Hairballs" (Errores) aleatoriamente
                dice = random.random()
                
                if dice < 0.10:  # 10% probabilidad de nombre vacío
                    prod = "" 
                elif dice < 0.20: # 10% probabilidad de precio negativo
                    price = round(price * -1, 2)
                elif dice < 0.25: # 5% probabilidad de precio cero
                    price = 0
            
            writer.writerow([i, prod, price])

    print(f"✅ Generado: {filename} ({rows} filas)")

if __name__ == "__main__":
    generate_csv("good_data.csv", is_clean=True)
    generate_csv("bad_data.csv", is_clean=False)