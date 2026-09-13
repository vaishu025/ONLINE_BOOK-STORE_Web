import os
import django
import random
from datetime import datetime, timedelta
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pvrs_book_shop.settings')
django.setup()

from books.models import Category, Book

# Book Cover URL Generator Functions
def get_openlibrary_cover(isbn, size='M'):
    """Get cover image from OpenLibrary"""
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-{size}.jpg"

def get_google_books_cover(isbn):
    """Get cover image from Google Books"""
    return f"https://books.google.com/books/content?id={isbn}&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

def get_placeholder_cover(title, author):
    """Generate a colored placeholder cover with text"""
    import hashlib
    text = f"{title} {author}"
    hash_id = hashlib.md5(text.encode()).hexdigest()[:10]
    return f"https://picsum.photos/seed/{hash_id}/400/600"

# Story Books with Real Cover URLs
STORY_BOOKS = [
    {"title": "The Magic Tree House", "author": "Mary Pope Osborne", "isbn": "9780679824114", "cover": "https://m.media-amazon.com/images/I/51bN5v4mK6L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "isbn": "9780747532699", "cover": "https://m.media-amazon.com/images/I/51U9Tv2nLdL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "isbn": "9780547928227", "cover": "https://m.media-amazon.com/images/I/51s4qF1GY-L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Charlotte's Web", "author": "E.B. White", "isbn": "9780064400558", "cover": "https://m.media-amazon.com/images/I/51YH5xqN5mL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Lion, the Witch and the Wardrobe", "author": "C.S. Lewis", "isbn": "9780064404990", "cover": "https://m.media-amazon.com/images/I/51bYv3xZxVL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Matilda", "author": "Roald Dahl", "isbn": "9780142410370", "cover": "https://m.media-amazon.com/images/I/51iT3jUuBqL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Percy Jackson & The Lightning Thief", "author": "Rick Riordan", "isbn": "9780786856299", "cover": "https://m.media-amazon.com/images/I/51t2sZMfhsL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "isbn": "9780156012195", "cover": "https://m.media-amazon.com/images/I/51s6eXTdMIL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll", "isbn": "9780141439761", "cover": "https://m.media-amazon.com/images/I/51UEnJzVwLL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Peter Pan", "author": "J.M. Barrie", "isbn": "9780142437933", "cover": "https://m.media-amazon.com/images/I/51wJfTVdKjL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Wonderful Wizard of Oz", "author": "L. Frank Baum", "isbn": "9780142437506", "cover": "https://m.media-amazon.com/images/I/51mPQVJ-FwL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Charlie and the Chocolate Factory", "author": "Roald Dahl", "isbn": "9780142410318", "cover": "https://m.media-amazon.com/images/I/51bL4BlbFoL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Secret Garden", "author": "Frances Hodgson Burnett", "isbn": "9780142437100", "cover": "https://m.media-amazon.com/images/I/51zFJJLBVKL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "A Wrinkle in Time", "author": "Madeleine L'Engle", "isbn": "9780312367541", "cover": "https://m.media-amazon.com/images/I/51oLIKWmJWL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Giver", "author": "Lois Lowry", "isbn": "9780440237686", "cover": "https://m.media-amazon.com/images/I/51n55bWgvJL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Bridge to Terabithia", "author": "Katherine Paterson", "isbn": "9780064401845", "cover": "https://m.media-amazon.com/images/I/51CAsQQJNiL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Where the Red Fern Grows", "author": "Wilson Rawls", "isbn": "9780440412670", "cover": "https://m.media-amazon.com/images/I/51t9nnS8emL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The BFG", "author": "Roald Dahl", "isbn": "9780142410387", "cover": "https://m.media-amazon.com/images/I/51p7vLfYk3L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "James and the Giant Peach", "author": "Roald Dahl", "isbn": "9780140374247", "cover": "https://m.media-amazon.com/images/I/51IDRtVS3rL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Fantastic Mr. Fox", "author": "Roald Dahl", "isbn": "9780142410349", "cover": "https://m.media-amazon.com/images/I/51U9+rzG9PL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
]

# Research Books with Real Cover URLs
RESEARCH_BOOKS = [
    {"title": "A Brief History of Time", "author": "Stephen Hawking", "isbn": "9780553380163", "cover": "https://m.media-amazon.com/images/I/51wS0l-7HWL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Selfish Gene", "author": "Richard Dawkins", "isbn": "9780199291151", "cover": "https://m.media-amazon.com/images/I/51LpU0iOMKL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "isbn": "9780062316097", "cover": "https://m.media-amazon.com/images/I/51zA3aehGOL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Homo Deus", "author": "Yuval Noah Harari", "isbn": "9780062464316", "cover": "https://m.media-amazon.com/images/I/51rQh7CkOzL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Origin of Species", "author": "Charles Darwin", "isbn": "9780140439120", "cover": "https://m.media-amazon.com/images/I/51SxJj3TMcL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Cosmos", "author": "Carl Sagan", "isbn": "9780345539434", "cover": "https://m.media-amazon.com/images/I/51vCXJ+1uOL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Elegant Universe", "author": "Brian Greene", "isbn": "9780375708114", "cover": "https://m.media-amazon.com/images/I/51ZZI2UJcnL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Astrophysics for People in a Hurry", "author": "Neil deGrasse Tyson", "isbn": "9780393609394", "cover": "https://m.media-amazon.com/images/I/51J4YVJKfjL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Guns, Germs, and Steel", "author": "Jared Diamond", "isbn": "9780393317558", "cover": "https://m.media-amazon.com/images/I/51yXpPVfPjL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Power of Habit", "author": "Charles Duhigg", "isbn": "9780812981605", "cover": "https://m.media-amazon.com/images/I/51wK-xvjZRL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "isbn": "9780374533557", "cover": "https://m.media-amazon.com/images/I/51pN1fVcqOL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Tipping Point", "author": "Malcolm Gladwell", "isbn": "9780316346627", "cover": "https://m.media-amazon.com/images/I/51kECBTB52L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Outliers", "author": "Malcolm Gladwell", "isbn": "9780316017930", "cover": "https://m.media-amazon.com/images/I/51fsUcAFPuL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Freakonomics", "author": "Steven Levitt", "isbn": "9780060731335", "cover": "https://m.media-amazon.com/images/I/51at9sJjW6L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Art of War", "author": "Sun Tzu", "isbn": "9781590302259", "cover": "https://m.media-amazon.com/images/I/51Q9l2lD5BL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
]

# Fiction Books with Cover URLs
FICTION_BOOKS = [
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "9780061120084", "cover": "https://m.media-amazon.com/images/I/51JfM3bRqML._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "1984", "author": "George Orwell", "isbn": "9780451524935", "cover": "https://m.media-amazon.com/images/I/51Z0FZVGSjL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "isbn": "9780141439518", "cover": "https://m.media-amazon.com/images/I/51h1DMCxwEL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "cover": "https://m.media-amazon.com/images/I/51jQrUxz5JL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Moby-Dick", "author": "Herman Melville", "isbn": "9780142437247", "cover": "https://m.media-amazon.com/images/I/51pEUpSSdLL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "isbn": "9780143039990", "cover": "https://m.media-amazon.com/images/I/51-+S9Lxv1L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "isbn": "9780140449136", "cover": "https://m.media-amazon.com/images/I/51fKSjRrXbL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "isbn": "9780316769488", "cover": "https://m.media-amazon.com/images/I/51cTpE3zq7L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Lord of the Flies", "author": "William Golding", "isbn": "9780399501487", "cover": "https://m.media-amazon.com/images/I/51ZtMZLjMML._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Animal Farm", "author": "George Orwell", "isbn": "9780451526342", "cover": "https://m.media-amazon.com/images/I/51DlqU-TQXL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
]

# Self-Help Books with Cover URLs
SELF_HELP_BOOKS = [
    {"title": "The 7 Habits of Highly Effective People", "author": "Stephen Covey", "isbn": "9780743269513", "cover": "https://m.media-amazon.com/images/I/51zL9mZkAqL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "How to Win Friends and Influence People", "author": "Dale Carnegie", "isbn": "9780671027032", "cover": "https://m.media-amazon.com/images/I/51aKt0wCyWL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Power of Now", "author": "Eckhart Tolle", "isbn": "9781577314806", "cover": "https://m.media-amazon.com/images/I/51lZGLKXwcL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Daring Greatly", "author": "Brené Brown", "isbn": "9781592408412", "cover": "https://m.media-amazon.com/images/I/51vNX8kGggL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The 4-Hour Workweek", "author": "Tim Ferriss", "isbn": "9780307465351", "cover": "https://m.media-amazon.com/images/I/51j15uVhjrL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
]

# Technology Books with Cover URLs
TECH_BOOKS = [
    {"title": "The Innovators", "author": "Walter Isaacson", "isbn": "9781476708690", "cover": "https://m.media-amazon.com/images/I/51hRp6m-y7L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Lean Startup", "author": "Eric Ries", "isbn": "9780307887894", "cover": "https://m.media-amazon.com/images/I/51ctVilBv8L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Zero to One", "author": "Peter Thiel", "isbn": "9780804139298", "cover": "https://m.media-amazon.com/images/I/51KRYwdrO5L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "isbn": "9780201616224", "cover": "https://m.media-amazon.com/images/I/51W1sBPO2JL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "Clean Code", "author": "Robert C. Martin", "isbn": "9780132350884", "cover": "https://m.media-amazon.com/images/I/51E5yZ5k8iL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
]

# Science Books with Cover URLs
SCIENCE_BOOKS = [
    {"title": "The Double Helix", "author": "James Watson", "isbn": "9780743216302", "cover": "https://m.media-amazon.com/images/I/51qZ-EDUp7L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Man Who Mistook His Wife for a Hat", "author": "Oliver Sacks", "isbn": "9780684853949", "cover": "https://m.media-amazon.com/images/I/51nvHpKLnXL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    {"title": "The Emperor of All Maladies", "author": "Siddhartha Mukherjee", "isbn": "9781439170915", "cover": "https://m.media-amazon.com/images/I/51xHdTMd3SL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
]

def get_cover_url(book_data):
    """Get cover URL from book data or generate placeholder"""
    if 'cover' in book_data and book_data['cover']:
        return book_data['cover']
    if 'isbn' in book_data and book_data['isbn']:
        return get_openlibrary_cover(book_data['isbn'])
    import hashlib
    text = f"{book_data.get('title', '')} {book_data.get('author', '')}"
    hash_id = hashlib.md5(text.encode()).hexdigest()[:10]
    return f"https://picsum.photos/seed/{hash_id}/400/600"

def populate_books():
    """Populate database with 1000+ books with cover images"""
    print("Starting to populate books with cover images...")

    categories = {
        'story': Category.objects.get_or_create(name='Story Books', category_type='story', slug='story-books')[0],
        'research': Category.objects.get_or_create(name='Research Books', category_type='research', slug='research-books')[0],
        'fiction': Category.objects.get_or_create(name='Fiction', category_type='fiction', slug='fiction')[0],
        'nonfiction': Category.objects.get_or_create(name='Non-Fiction', category_type='nonfiction', slug='non-fiction')[0],
        'science': Category.objects.get_or_create(name='Science', category_type='science', slug='science')[0],
        'tech': Category.objects.get_or_create(name='Technology', category_type='tech', slug='technology')[0],
        'selfhelp': Category.objects.get_or_create(name='Self-Help', category_type='selfhelp', slug='self-help')[0],
        'education': Category.objects.get_or_create(name='Education', category_type='education', slug='education')[0],
        'history': Category.objects.get_or_create(name='History', category_type='history', slug='history')[0],
        'biography': Category.objects.get_or_create(name='Biography', category_type='biography', slug='biography')[0],
    }

    book_count = 0

    print("Adding Story Books with covers...")
    for i in range(300):
        book_data = random.choice(STORY_BOOKS)
        if i >= len(STORY_BOOKS):
            book_data = {
                "title": f"Adventure Story {i+1}",
                "author": f"Author {i+1}",
                "cover": get_placeholder_cover(f"Adventure Story {i+1}", f"Author {i+1}")
            }

        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            description=f"A captivating story that will inspire and entertain readers of all ages. {book_data['title']} is a wonderful tale of adventure and discovery.",
            price=round(random.uniform(5.99, 24.99), 2),
            category=categories['story'],
            book_type='story',
            cover_image_url=get_cover_url(book_data),
            publisher=random.choice(['Penguin Books', 'HarperCollins', 'Scholastic', 'Oxford University Press']),
            publication_date=datetime.now() - timedelta(days=random.randint(1, 3650)),
            pages=random.randint(100, 400),
            language='English',
            is_bestseller=random.choice([True, False]),
            is_new_arrival=random.choice([True, False]),
            is_audiobook=random.choice([True, False]),
            stock_quantity=random.randint(5, 50),
            rating=round(random.uniform(3.5, 5.0), 2),
            total_reviews=random.randint(10, 500),
        )
        book.save()
        book_count += 1
        print(f"Added story book {book_count}: {book.title} with cover")

    print("Adding Research Books with covers...")
    for i in range(300):
        book_data = random.choice(RESEARCH_BOOKS)
        if i >= len(RESEARCH_BOOKS):
            book_data = {
                "title": f"Research Paper {i+1}",
                "author": f"Researcher {i+1}",
                "cover": get_placeholder_cover(f"Research Paper {i+1}", f"Researcher {i+1}")
            }

        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            description=f"A comprehensive research work exploring important concepts and discoveries. {book_data['title']} presents groundbreaking ideas.",
            price=round(random.uniform(15.99, 49.99), 2),
            category=categories['research'],
            book_type='research',
            cover_image_url=get_cover_url(book_data),
            publisher=random.choice(['Academic Press', 'MIT Press', 'Oxford Academic', 'Cambridge University Press']),
            publication_date=datetime.now() - timedelta(days=random.randint(1, 7300)),
            pages=random.randint(200, 800),
            language=random.choice(['English', 'English']),
            is_bestseller=random.choice([True, False]),
            is_new_arrival=random.choice([True, False]),
            is_featured=random.choice([True, False]),
            stock_quantity=random.randint(3, 30),
            rating=round(random.uniform(3.0, 4.8), 2),
            total_reviews=random.randint(5, 300),
        )
        book.save()
        book_count += 1
        print(f"Added research book {book_count}: {book.title} with cover")

    print("Adding Fiction Books with covers...")
    for i in range(150):
        book_data = random.choice(FICTION_BOOKS) if FICTION_BOOKS else {"title": f"Fiction Book {i+1}", "author": f"Author {i+1}"}
        if i >= len(FICTION_BOOKS):
            book_data = {
                "title": f"Fiction Novel {i+1}",
                "author": f"Author {i+1}",
                "cover": get_placeholder_cover(f"Fiction Novel {i+1}", f"Author {i+1}")
            }

        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            description="An engaging work of fiction that explores the depths of human experience and imagination.",
            price=round(random.uniform(7.99, 29.99), 2),
            category=categories['fiction'],
            book_type='general',
            cover_image_url=get_cover_url(book_data),
            publisher=random.choice(['Penguin Random House', 'Simon & Schuster', 'Hachette', 'Macmillan']),
            publication_date=datetime.now() - timedelta(days=random.randint(1, 5000)),
            pages=random.randint(150, 500),
            language='English',
            is_bestseller=random.choice([True, False]),
            is_new_arrival=random.choice([True, False]),
            stock_quantity=random.randint(10, 60),
            rating=round(random.uniform(3.5, 5.0), 2),
            total_reviews=random.randint(20, 600),
        )
        book.save()
        book_count += 1
        print(f"Added fiction book {book_count}: {book.title} with cover")

    print("Adding Self-Help Books with covers...")
    for i in range(100):
        book_data = random.choice(SELF_HELP_BOOKS) if SELF_HELP_BOOKS else {"title": f"Self-Help {i+1}", "author": f"Author {i+1}"}

        book = Book(
            title=book_data['title'] if i < len(SELF_HELP_BOOKS) else f"Personal Growth {i+1}",
            author=book_data['author'] if i < len(SELF_HELP_BOOKS) else f"Motivator {i+1}",
            description="Transform your life with practical advice and strategies for personal development.",
            price=round(random.uniform(6.99, 19.99), 2),
            category=categories['selfhelp'],
            book_type='general',
            cover_image_url=get_cover_url(book_data),
            publisher=random.choice(['Hay House', 'Simon & Schuster', 'HarperOne']),
            publication_date=datetime.now() - timedelta(days=random.randint(1, 4000)),
            pages=random.randint(100, 350),
            language='English',
            is_bestseller=random.choice([True, False]),
            stock_quantity=random.randint(15, 70),
            rating=round(random.uniform(4.0, 5.0), 2),
            total_reviews=random.randint(30, 800),
        )
        book.save()
        book_count += 1
        print(f"Added self-help book {book_count}: {book.title} with cover")

    print("Adding Technology Books with covers...")
    for i in range(80):
        book_data = random.choice(TECH_BOOKS) if TECH_BOOKS else {"title": f"Tech Book {i+1}", "author": f"Author {i+1}"}

        book = Book(
            title=book_data['title'] if i < len(TECH_BOOKS) else f"Tech Mastery {i+1}",
            author=book_data['author'] if i < len(TECH_BOOKS) else f"Technologist {i+1}",
            description="Essential reading for anyone interested in technology, innovation, and digital transformation.",
            price=round(random.uniform(8.99, 39.99), 2),
            category=categories['tech'],
            book_type='general',
            cover_image_url=get_cover_url(book_data),
            publisher=random.choice(['O\'Reilly Media', 'Manning Publications', 'Wiley']),
            publication_date=datetime.now() - timedelta(days=random.randint(1, 3000)),
            pages=random.randint(150, 500),
            language='English',
            is_new_arrival=random.choice([True, False]),
            stock_quantity=random.randint(10, 50),
            rating=round(random.uniform(3.5, 5.0), 2),
            total_reviews=random.randint(10, 350),
        )
        book.save()
        book_count += 1
        print(f"Added tech book {book_count}: {book.title} with cover")

    print("Adding Science Books with covers...")
    for i in range(80):
        book_data = random.choice(SCIENCE_BOOKS) if SCIENCE_BOOKS else {"title": f"Science Book {i+1}", "author": f"Author {i+1}"}

        book = Book(
            title=book_data['title'] if i < len(SCIENCE_BOOKS) else f"Science Discovery {i+1}",
            author=book_data['author'] if i < len(SCIENCE_BOOKS) else f"Scientist {i+1}",
            description="An exploration of scientific principles and discoveries that shape our understanding of the world.",
            price=round(random.uniform(12.99, 45.99), 2),
            category=categories['science'],
            book_type='research',
            cover_image_url=get_cover_url(book_data),
            publisher=random.choice(['Scientific American', 'MIT Press', 'Nature Publishing']),
            publication_date=datetime.now() - timedelta(days=random.randint(1, 8000)),
            pages=random.randint(200, 700),
            language='English',
            is_featured=random.choice([True, False]),
            stock_quantity=random.randint(5, 25),
            rating=round(random.uniform(3.7, 4.9), 2),
            total_reviews=random.randint(8, 250),
        )
        book.save()
        book_count += 1
        print(f"Added science book {book_count}: {book.title} with cover")

    print("Adding more general books with covers...")
    additional_books = [
        {"title": "The Alchemist", "author": "Paulo Coelho", "cover": "https://m.media-amazon.com/images/I/51iT3jUuBqL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Da Vinci Code", "author": "Dan Brown", "cover": "https://m.media-amazon.com/images/I/51CvB+F4PmL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Hunger Games", "author": "Suzanne Collins", "cover": "https://m.media-amazon.com/images/I/51hM2kS6dVL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Fault in Our Stars", "author": "John Green", "cover": "https://m.media-amazon.com/images/I/51HqfQeij3L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "Gone Girl", "author": "Gillian Flynn", "cover": "https://m.media-amazon.com/images/I/51r38nYK0WL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "cover": "https://m.media-amazon.com/images/I/51Zx6qF5xZL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Book Thief", "author": "Markus Zusak", "cover": "https://m.media-amazon.com/images/I/51W3TvV9l+L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Kite Runner", "author": "Khaled Hosseini", "cover": "https://m.media-amazon.com/images/I/51vT43UtgnL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Help", "author": "Kathryn Stockett", "cover": "https://m.media-amazon.com/images/I/51U0C+mLw8L._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
        {"title": "The Road", "author": "Cormac McCarthy", "cover": "https://m.media-amazon.com/images/I/51wVH2yZ2XL._SY291_BO1,204,203,200_QL40_FMwebp_.jpg"},
    ]

    for i, book_data in enumerate(additional_books):
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            description=f"A compelling book that has captured the hearts of readers worldwide. {book_data['title']} is a must-read.",
            price=round(random.uniform(4.99, 19.99), 2),
            category=random.choice(list(categories.values())),
            book_type=random.choice(['story', 'general']),
            cover_image_url=book_data['cover'],
            publisher=random.choice(['Penguin Books', 'HarperCollins', 'Random House']),
            publication_date=datetime.now() - timedelta(days=random.randint(1, 3000)),
            pages=random.randint(150, 450),
            language='English',
            is_bestseller=True,
            stock_quantity=random.randint(10, 50),
            rating=round(random.uniform(3.8, 5.0), 2),
            total_reviews=random.randint(50, 1000),
        )
        book.save()
        book_count += 1
        print(f"Added popular book {book_count}: {book.title} with cover")

    print(f"\nSuccessfully added {book_count} books with cover images to PVRS BOOK SHOP!")
    print(f"Categories populated: {len(categories)}")
    print("All books have cover images from external sources!")
    return book_count

if __name__ == '__main__':
    populate_books()
