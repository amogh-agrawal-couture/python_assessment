from faker import Faker
import pandas as pd
import random

fake = Faker()

categories = ["Electronics", "Laptops", "Shoes", "Clothing", "Home", "Books"]

data = []

for i in range(1, 1001):   # 1000 products
    category = random.choice(categories)

    data.append({
        "product_id": i,
        "product_name": fake.word().title() + " " + fake.word().title(),
        "category": category,
        "price": round(random.uniform(10, 2000), 2),
        "quantity_sold": random.randint(0, 500),
        "rating": round(random.uniform(1, 5), 1),
        "review_count": random.randint(0, 1000)
    })

df = pd.DataFrame(data)

# Introduce some missing values (for cleaning task)
for col in ["price", "quantity_sold", "rating"]:
    df.loc[df.sample(frac=0.05).index, col] = None

df.to_csv("products_raw.csv", index=False)
print("products_raw.csv generated")
