from django.shortcuts import render, get_object_or_404, redirect
from .models import Document
from .forms import DocumentForm


def document_list(request):
    documents = Document.objects.all().order_by('-created_at')

    search_query = request.GET.get('q')
    status_filter = request.GET.get('status')

    if search_query:
        documents = documents.filter(title__icontains=search_query)

    if status_filter:
        documents = documents.filter(status=status_filter)

    context = {
        'documents': documents,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Document.STATUS_CHOICES,
    }

    return render(request, 'documents/document_list.html', context)


def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})


def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()

    return render(request, 'documents/document_form.html', {'form': form})