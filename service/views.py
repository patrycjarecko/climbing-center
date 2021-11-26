from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'service/index.html', context={
        # 'error': True,
        # 'statusCode': 500,
        # 'message': 'test message'
    })