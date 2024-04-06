from django import forms
from .models import NewsPost, Category


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ["title", "content", "image_link", "category", "tag"]


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100)


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Choose a category"

    class Meta:
        model = NewsPost
        fields = ["title", "content", "category", "image_link"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image_link": forms.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),
        }

    def clean_image_link(self):
        image = self.cleaned_data.get("image_link", False)
        if image:
            if not image.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                raise forms.ValidationError("Only image files are allowed.")
        return image


class NewsFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="All Categories", required=False
    )
