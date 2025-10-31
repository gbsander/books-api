import requests
from bs4 import BeautifulSoup
import csv
import time

# URL base do site
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
SITE_BASE = "https://books.toscrape.com/catalogue/"

def get_book_category(book_url):
    """Busca a categoria de um livro específico"""
    try:
        response = requests.get(book_url)
        if response.status_code != 200:
            return "Unknown"

        soup = BeautifulSoup(response.content, 'html.parser')
        # A categoria está no breadcrumb
        breadcrumb = soup.find('ul', class_='breadcrumb')
        if breadcrumb:
            # Pega o penúltimo item (último é o título do livro)
            category_link = breadcrumb.find_all('a')
            if len(category_link) >= 3:
                return category_link[2].text.strip()
        return "Unknown"
    except:
        return "Unknown"

def scrape_books():
    """Função principal que faz o scraping de todos os livros"""
    all_books = []  # Lista para guardar todos os livros
    page = 1  # Começa na página 1

    print("Iniciando scraping com categorias...")
    print("ATENÇÃO: Isso vai demorar ~10 minutos para processar 1000 livros")

    while True:
        # Monta a URL da página atual
        url = BASE_URL.format(page)
        print(f"\nScraping página {page}...")

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
        for idx, book in enumerate(books, 1):
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

            # Extrai URL do livro para buscar categoria
            book_link = book.h3.a['href']
            book_url = SITE_BASE + book_link

            # Busca a categoria (isso adiciona uma requisição extra por livro)
            category = get_book_category(book_url)

            print(f"  [{idx}/{len(books)}] {title[:40]}... - {category}")

            # Cria um dicionário com todos os dados
            book_data = {
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability,
                'category': category,
                'image_url': image_url
            }

            # Adiciona à lista
            all_books.append(book_data)

            # Pequeno delay para não sobrecarregar
            time.sleep(0.1)

        page += 1  # Vai para próxima página
        time.sleep(0.5)  # Espera meio segundo entre páginas

    print(f"\nTotal de livros coletados: {len(all_books)}")
    return all_books


def save_to_csv(books, filename='data/books.csv'):
    """Salva os livros em um arquivo CSV"""
    if not books:
        print("Nenhum livro para salvar!")
        return

    # Abre arquivo CSV para escrita
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        # Define as colunas (agora com category)
        fieldnames = ['title', 'price', 'rating', 'availability', 'category', 'image_url']
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
