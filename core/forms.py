from django import forms

from .models import Inquiry


class InquiryForm(forms.ModelForm):
    # Honeypot field: real visitors never see or fill this in (hidden via
    # CSS, not `type="hidden"`, so basic bots that skip hidden inputs still
    # get caught). If it arrives non-empty, the submission is spam.
    #
    # NOTE: this field must NOT be named/labelled anything a browser's
    # autofill recognises (e.g. "website", "url", "company") — Chrome/Edge
    # business-profile autofill will silently fill fields with those names
    # even while they're visually hidden, which makes every real visitor's
    # submission look like spam. "new-password" autocomplete is also a much
    # more reliable "don't autofill this" signal than autocomplete="off".
    hp_check = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "new-password", "tabindex": "-1"}),
    )

    class Meta:
        model = Inquiry
        fields = ["name", "email", "phone", "service", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "078X XXX XXX"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Tell us about the space and what you need cleaned.", "rows": 5}
            ),
        }

    def is_spam(self):
        return bool(self.cleaned_data.get("hp_check"))
