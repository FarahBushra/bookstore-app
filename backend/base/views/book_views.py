import imp
from urllib import response
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Book, Review
# from .books import books
from base.serializers import BookSerializer

from rest_framework import status

@api_view(["GET"])
def getBooks(request):
    query = request.query_params.get("keyword")
    print("query:", query)
    if query == None:
        query = ""

    books = Book.objects.filter(name__icontains=query)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getBook(request, pk):
    book = Book.objects.get(_id=pk)
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def createBook(request):

    user = request.user

    book = Book.objects.create(
        user=user,
        title = "Sample Name",
        author = "Sample Author Name",
        publisher = "Sample Publisher Name",
        edition = "",
        year = 0,
        price = 0,
        
    )


    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateBook(request, pk):
    data = request.data
    book = Book.objects.get(_id=pk)

    book.title = data["title"]
    book.author = data["author"]
    book.publisher = data["publisher"]
    book.edition = data["edition"]
    book.year = data["year"]
    book.price = data["price"]
    book.format = data["format"]
    book.genre = data["genre"]
    book.image = data["image"]
    book.description = data["description"]
    book.rating = data["rating"]
    book.numReviews = data["numReviews"]
    book.language = data["language"]
    book.countInStock = data["countInStock"]


    book.save()

    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteBook(request, pk):
    book = Book.objects.get(_id=pk)
    book.delete()
    return Response("Book Deleted")


@api_view(["POST"])
@permission_classes([IsAdminUser])
def uploadImage(request):
    data = request.data

    book_id = data["book_id"]
    book = Book.objects.get(_id=book_id)

    book.image = request.FILES.get("image")
    book.save()

    return Response("Image Uploaded")



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createBookReview(request, pk):
    user = request.user
    book = Book.objects.get(_id=pk)
    data = request.data

    # Review exists

    alreadyExists = book.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {"detail":"Book already reviewed"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # no rating
    elif data["rating"] == 0:
        content = {"detail":"Please give rating"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


    # create rev
    else:
        review = Review.objects.create(
            user=user,
            book=book,
            name=user.first_name,
            rating=data["rating"],
            comment=data["comment"],
        )

        reviews = book.review_set.all()
        book.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        book.rating = total / len(reviews)
        book.save()

        return Response("Review Added")
