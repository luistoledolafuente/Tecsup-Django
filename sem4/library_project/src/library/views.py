from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Author, Book, Category, Publisher

# Vista para la página principal con estadísticas de la biblioteca
def home(request):
    context = {
        'total_books': Book.objects.count(),             # Total de libros
        'total_authors': Author.objects.count(),         # Total de autores
        'total_categories': Category.objects.count(),    # Total de categorías
        'total_publishers': Publisher.objects.count(),   # Total de editoriales
        
        # Obtener las categorías con el conteo de libros (las 5 con más libros)
        'categories': Category.objects.annotate(
            book_count=Count('books')
        ).order_by('-book_count')[:5],
        
        # Obtener los 5 libros más recientes (ordenados por fecha de publicación)
        'recent_books': Book.objects.select_related('author').order_by('-publication_date')[:5],
    }
    return render(request, 'library/home.html', context)

# Vista para listar todos los autores
def author_list(request):
    authors = Author.objects.all().order_by('name')  # Obtener todos los autores ordenados por nombre
    return render(request, 'library/author_list.html', {'authors': authors})

# Vista para mostrar detalles de un autor y sus libros
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)        # Obtener autor por su primary key o 404 si no existe
    books = author.books.all()                        # Obtener todos los libros de ese autor
    return render(request, 'library/author_detail.html', {'author': author, 'books': books})

# Vista para listar todos los libros
def book_list(request):
    books = Book.objects.all().select_related('author').order_by('title')  # Todos los libros con sus autores, ordenados por título
    return render(request, 'library/book_list.html', {'books': books})

# Vista para mostrar detalles de un libro
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)             # Obtener libro por su pk o 404
    categories = book.categories.all()                 # Obtener todas las categorías del libro
    publications = book.publication_set.select_related('publisher').all()  # Obtener todas las publicaciones con editoriales
    
    context = {
        'book': book,
        'categories': categories,
        'publications': publications
    }
    return render(request, 'library/book_detail.html', context)

# Vista para listar todas las categorías
def category_list(request):
    categories = Category.objects.annotate(
        book_count=Count('books')                       # Anotar cada categoría con la cantidad de libros que tiene
    ).order_by('name')                                  # Ordenar por nombre
    return render(request, 'library/category_list.html', {'categories': categories})

# Vista para mostrar detalles de una categoría y los libros que contiene
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)  # Obtener categoría por su slug o 404
    books = category.books.all().select_related('author')  # Obtener libros de esa categoría con sus autores
    return render(request, 'library/category_detail.html', {'category': category, 'books': books})
