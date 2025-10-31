import requests
from bs4 import BeautifulSoup
import csv
import time

# URL base do site
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def scrape_books():
    """Função principal que faz o scraping de todos os livros"""
    all_books = []  # Lista para guardar todos os livros
    page = 1  # Começa na página 1

    print("Iniciando scraping...")

    while True:
        # Monta a URL da página atual
        url = BASE_URL.format(page)
        print(f"Scraping página {page}...")

        # Faz requisição HTTP
        response = requests.get(url)

        # Se deu erro 404, acabaram as páginas
        if response.status_code == 404:
            break

        # Transforma HTML em objeto BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontra todos os livros na página
        books = soup.find_all('article', class_='product_pod')

        # Para cada livro, extrai os dados
        for book in books:
            # Extrai título
            title = book.h3.a['title']

            # Extrai preço (remove o símbolo £)
            price = book.find('p', class_='price_color').text.strip('£')

            # Extrai rating (converte texto para número)
            rating_class = book.find('p', class_='star-rating')['class'][1]
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = rating_map.get(rating_class, 0)

            # Extrai disponibilidade
            availability = book.find('p', class_='instock availability').text.strip()

            # Extrai URL da imagem
            image_url = "https://books.toscrape.com/" + book.find('img')['src'].replace('../', '')

            # Cria um dicionário com todos os dados
            book_data = {
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability,
                'image_url': image_url
            }

            # Adiciona à lista
            all_books.append(book_data)

        page += 1  # Vai para próxima página
        time.sleep(0.5)  # Espera meio segundo para não sobrecarregar o servidor

    print(f"\nTotal de livros coletados: {len(all_books)}")
    return all_books


def save_to_csv(books, filename='data/books.csv'):
    """Salva os livros em um arquivo CSV"""
    if not books:
        print("Nenhum livro para salvar!")
        return

    # Abre arquivo CSV para escrita
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        # Define as colunas
        fieldnames = ['title', 'price', 'rating', 'availability', 'image_url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Escreve cabeçalho
        writer.writeheader()
        # Escreve todos os livros
        writer.writerows(books)

    print(f"Dados salvos em {filename}")


if __name__ == "__main__":
    # Executa o scraping
    books = scrape_books()
    # Salva no CSV
    save_to_csv(books)
