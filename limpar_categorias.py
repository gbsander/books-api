import csv

# Categorias válidas de livros
VALID_CATEGORIES = {
    'Fiction', 'Nonfiction', 'Fantasy', 'Mystery', 'Romance', 'Thriller',
    'Science Fiction', 'Historical Fiction', 'Young Adult', 'Childrens',
    'Poetry', 'Classics', 'Horror', 'Sequential Art', 'History',
    'Biography', 'Autobiography', 'Business', 'Self Help', 'Religion',
    'Spirituality', 'Philosophy', 'Psychology', 'Science', 'Music',
    'Art', 'Travel', 'Food and Drink', 'Health', 'Sports and Games',
    'Humor', 'Parenting', 'Politics', 'Contemporary', 'Christian',
    'Christian Fiction', 'Womens Fiction', 'New Adult', 'Crime',
    'Suspense', 'Erotica', 'Academic', 'Cultural', 'Novels',
    'Short Stories', 'Adult Fiction', 'Historical', 'Default'
}

def clean_csv():
    """Limpa categorias inválidas do CSV"""
    books = []

    # Ler CSV
    with open('data/books.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Limpar categoria
            category = row['category'].strip()

            # Se não é válida, marcar como Unknown
            if category not in VALID_CATEGORIES:
                row['category'] = 'Unknown'

            books.append(row)

    # Escrever CSV limpo
    with open('data/books.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'price', 'rating', 'availability', 'category', 'image_url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    # Estatísticas
    categories = {}
    for book in books:
        cat = book['category']
        categories[cat] = categories.get(cat, 0) + 1

    print(f"✅ CSV limpo!")
    print(f"Total de livros: {len(books)}")
    print(f"\nCategorias encontradas ({len(categories)}):")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    clean_csv()
