from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import F, Count
from .models import Quote, Source
from .forms import QuoteForm, SourceForm


def random_quote(request):
    quote = Quote.get_random()
    if quote:
        # Используем атомарное обновление с F()
        Quote.objects.filter(id=quote.id).update(views=F('views') + 1)
        # Обновляем объект quote из базы данных
        quote.refresh_from_db()

    return render(request, 'quotes/random_quote.html', {'quote': quote})


def like_quote(request, quote_id):
    if request.method == 'POST':
        quote = get_object_or_404(Quote, id=quote_id)
        # Используем атомарное обновление с F()
        Quote.objects.filter(id=quote_id).update(likes=F('likes') + 1)
        # Обновляем объект quote из базы данных
        quote.refresh_from_db()
        return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def dislike_quote(request, quote_id):
    if request.method == 'POST':
        quote = get_object_or_404(Quote, id=quote_id)
        # Используем атомарное обновление с F()
        Quote.objects.filter(id=quote_id).update(dislikes=F('dislikes') + 1)
        # Обновляем объект quote из базы данных
        quote.refresh_from_db()
        return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})


def add_source(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_quote')
    else:
        form = SourceForm()

    return render(request, 'quotes/add_source.html', {'form': form})


def top_quotes(request):
    quotes = Quote.objects.all().order_by('-likes')[:10]
    return render(request, 'quotes/top_quotes.html', {'quotes': quotes})