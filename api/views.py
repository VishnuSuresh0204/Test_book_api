from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

@api_view(["GET"])
def book_list(request):

    book_id = request.query_params.get("id")
    author = request.query_params.get("author")
    title = request.query_params.get("title")

    # Search by ID
    if book_id:
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

    # Search by Author
    if author:
        books = Book.objects.filter(author__icontains=author)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    # Search by Title
    if title:
        books = Book.objects.filter(title__icontains=title)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    # Return all books
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)