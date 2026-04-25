from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.http import FileResponse

from .models import Document, Client, ClientCase, RequiredDocument
from .forms import DocumentForm, StaffClientCaseForm


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required
def after_login_redirect(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')

    return redirect('document_list')


@login_required
def document_list(request):
    if request.user.is_staff:
        required_documents = RequiredDocument.objects.all().select_related(
            'client_case',
            'client_case__client',
            'client_case__service_type',
            'document_type'
        )
    else:
        required_documents = RequiredDocument.objects.filter(
            client_case__client__user=request.user
        ).select_related(
            'client_case',
            'client_case__client',
            'client_case__service_type',
            'document_type'
        )

    search_query = request.GET.get('q')

    if search_query:
        required_documents = required_documents.filter(
            Q(client_case__client__full_name__icontains=search_query) |
            Q(client_case__client__inn__icontains=search_query) |
            Q(document_type__name__icontains=search_query) |
            Q(client_case__service_type__name__icontains=search_query)
        )

    context = {
        'required_documents': required_documents,
        'search_query': search_query,
        'status_choices': RequiredDocument.STATUS_CHOICES,
    }

    return render(request, 'documents/document_list.html', context)


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if not request.user.is_staff and document.required_document.client_case.client.user != request.user:
        return redirect('document_list')

    return render(request, 'documents/document_detail.html', {
        'document': document
    })


@login_required
def document_create(request):
    required_document_id = request.GET.get('required_document')
    required_document = get_object_or_404(RequiredDocument, pk=required_document_id)

    if not request.user.is_staff and required_document.client_case.client.user != request.user:
        return redirect('document_list')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.required_document = required_document
            document.save()

            required_document.status = 'uploaded'
            required_document.save()

            return redirect('document_list')
    else:
        form = DocumentForm()

    return render(request, 'documents/document_form.html', {
        'form': form,
        'required_document': required_document,
    })


@login_required
def document_file(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if not request.user.is_staff and document.required_document.client_case.client.user != request.user:
        return redirect('document_list')

    download = request.GET.get('download') == '1'

    return FileResponse(
        document.file.open('rb'),
        as_attachment=download,
        filename=document.file.name.split('/')[-1]
    )


@login_required
@require_POST
def required_document_status_update(request, pk):
    if not request.user.is_staff:
        return redirect('document_list')

    required_document = get_object_or_404(RequiredDocument, pk=pk)
    new_status = request.POST.get('status')

    allowed_statuses = [
        'brought_personally',
        'not_required',
        'verified',
        'rejected',
        'waiting',
    ]

    if new_status in allowed_statuses:
        required_document.status = new_status
        required_document.save()

    return redirect('document_list')


@login_required
@user_passes_test(is_staff_user)
def staff_dashboard(request):
    search_query = request.GET.get('q')

    cases = ClientCase.objects.all().select_related(
        'client',
        'service_type'
    ).annotate(
        total_documents=Count('required_documents'),
        completed_documents=Count(
            'required_documents',
            filter=Q(required_documents__status__in=[
                'uploaded',
                'verified',
                'brought_personally',
                'not_required',
            ])
        ),
        waiting_documents=Count(
            'required_documents',
            filter=Q(required_documents__status='waiting')
        )
    ).order_by('-created_at')

    if search_query:
        cases = cases.filter(
            Q(client__full_name__icontains=search_query) |
            Q(client__inn__icontains=search_query) |
            Q(service_type__name__icontains=search_query)
        )

    context = {
        'cases': cases,
        'search_query': search_query,
    }

    return render(request, 'documents/staff_dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def staff_client_case_create(request):
    if request.method == 'POST':
        form = StaffClientCaseForm(request.POST)

        if form.is_valid():
            inn = form.cleaned_data['inn']
            full_name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            service_type = form.cleaned_data['service_type']

            client = Client.objects.filter(inn=inn).first()

            if client is None:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )

                client = Client.objects.create(
                    user=user,
                    full_name=full_name,
                    inn=inn
                )

            ClientCase.objects.create(
                client=client,
                service_type=service_type
            )

            return redirect('staff_dashboard')
    else:
        form = StaffClientCaseForm()

    return render(request, 'documents/staff_client_case_create.html', {
        'form': form
    })