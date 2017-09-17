# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import PDFFile, Link
from .pdf_parser import pdf_parse
from .link_validator import validate


def home(request):
    return render(request, 'home.html')

    
def add_file(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    #if not request.POST['file_name'] or not request.POST['links'] or 'file' not in request.FILES:
    #    return JsonResponse({'error': 'No file specified'}, status=400)
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file specified'}, status=400)

    if request.FILES['file'].content_type != 'application/pdf':
        return JsonResponse({'error': 'Invalid file type'}, status=400)
 
    # get file urls
    #urls = set(request.POST['links'].splitlines())
    urls = pdf_parse(request.FILES['file'].file)
    if urls is None:
        return JsonResponse({'error': 'Cannot parse pdf file'}, status=400)
    urls = set(urls)
    
    # create new file
    pdf_file = PDFFile(name=request.FILES['file'].name)
    pdf_file.save()
    
    # get links which already exist
    existing_links = list(Link.objects.filter(url__in=urls))
    existing_urls = set(l.url for l in existing_links)
    
    pdf_file.link_set.add(*existing_links)
    pdf_file.save()
    
    # create new links
    new_urls = urls - existing_urls
    validated_urls = validate(new_urls)
    Link.objects.bulk_create([
        Link(url=url, is_alive=is_alive) for url, is_alive in validated_urls.iteritems()
    ])
    
    # get new links
    new_links = list(Link.objects.filter(url__in=new_urls))

    pdf_file.link_set.add(*new_links)
    pdf_file.save()
    
    response = {
        'id': pdf_file.id,
        'name': pdf_file.name,
        'links': [
            {'id': link.id, 'url': link.url} 
                for link in pdf_file.link_set.all()
        ]
    }

    return JsonResponse(response)

    

def files(request, file_id=None):
    if request.method != 'GET':
        return HttpResponse(status=405)
    
    if file_id:
        try:
            file_id = int(file_id)
        except ValueError:
            return HttpResponse(status=404)
        
        pdf_file = get_object_or_404(PDFFile, id=file_id)

        response = {
            'id':pdf_file.id,
            'name': pdf_file.name,
            'links': [
                {'id': link.id, 'url': link.url} 
                    for link in pdf_file.link_set.all()
            ]
        }
    else:
        pdf_files = PDFFile.objects.all()
        response = {
            'files': [
                {'id': pdf_file.id, 'name': pdf_file.name, 'num_links': len(pdf_file.link_set.all())}
                    for pdf_file in pdf_files
            ]
        }
    return JsonResponse(response)


def links(request):
    if request.method != 'GET':
        return HttpResponse(status=405)
    
    links = Link.objects.all()

    response = {
        'links': [
            {'id': link.id, 'url': link.url, 'num_files': len(link.pdf_file.all())}
                for link in links
        ]
    }
    return JsonResponse(response)
