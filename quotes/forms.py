from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")

        if source:
            quote_count = Quote.objects.filter(source=source).count()
            if quote_count >= 3:
                raise forms.ValidationError("Нельзя добавить больше 3 цитат от одного источника.")
        return cleaned_data
