from django.shortcuts import render, redirect
from .forms import QuoteForm

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})
