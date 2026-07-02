from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def book_list(request):

    # ==========================
    # GET (Public)
    # ==========================
    if request.method == "GET":

        book_id = request.query_params.get("id")
        author = request.query_params.get("author")
        title = request.query_params.get("title")

        if book_id:
            try:
                book = Book.objects.get(id=book_id)
                serializer = BookSerializer(book)
                return Response(serializer.data)
            except Book.DoesNotExist:
                return Response({"error": "Book not found"}, status=404)

        if author:
            books = Book.objects.filter(author__icontains=author)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

        if title:
            books = Book.objects.filter(title__icontains=title)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


    # =====================================
    # API KEY REQUIRED
    # POST, PUT, PATCH, DELETE
    # =====================================
    api_key = request.headers.get("x-api-key")

    if api_key != settings.API_KEY:
        return Response(
            {"error": "Invalid API Key"},
            status=401
        )


    # ==========================
    # POST
    # ==========================
    if request.method == "POST":

        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


    # ==========================
    # PUT
    # ==========================
    if request.method == "PUT":

        book_id = request.query_params.get("id")

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    # ==========================
    # PATCH
    # ==========================
    if request.method == "PATCH":

        book_id = request.query_params.get("id")

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    # ==========================
    # DELETE
    # ==========================
    if request.method == "DELETE":

        book_id = request.query_params.get("id")

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        book.delete()

        return Response(
            {"message": "Book deleted successfully"},
            status=204
        )