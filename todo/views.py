from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from todo.models import Task
from todo.serializers import TaskSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/task-list?title=''&completed=0&page=1&page_size=5',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def task_list(request):
    completed = request.query_params.get('completed')
    title = request.query_params.get('title')

    query = Task.object.all()
    if completed is not None:
        if completed == "0":
            query = query.filter(completed=False)
        elif completed == "1":
            query = query.filter(completed=True)
    if title:
        query = query.filter(title__contains=title)

    paginator = StandardResultsSetPagination()
    paginated_query = paginator.paginate_queryset(query, request)
    serializer = TaskSerializer(paginated_query, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def task_detail(request, pk):
    task = Task.object.get(id=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
def task_create(request):
    print(request.data)
    for i in range(100):
        d = request.data
        d['title'] = f"Task {i}"
        serializer = TaskSerializer(data=d)
        if serializer.is_valid():
            serializer.save()
    # return Response(serializer.data)
    return Response("added")


@api_view(['PUT'])
def task_update(request, pk):
    task = Task.object.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def task_delete(request, pk):
    task = Task.object.get(id=pk)
    task.delete()
    return Response("Task deleted successfully.")
