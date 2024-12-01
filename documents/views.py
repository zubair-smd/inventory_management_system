from django.shortcuts import render

def document_list(request):
    # Logic for displaying documents
    return render(request, 'documents/document_list.html')
