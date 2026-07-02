from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

@api_view(["GET"])
def book_list(request):
    book_id = request.query_params.get("id")

    if book_id:
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)