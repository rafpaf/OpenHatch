import django.contrib.auth.forms
from django.contrib.auth.models import User
import django.forms

class UserCreationFormWithEmail(django.contrib.auth.forms.UserCreationForm):
    username = django.forms.RegexField(label="Username", max_length=30, regex=r'^\w+$',
        help_text = "Please pick a username, of 30 characters or fewer. Stick to letters, digits and underscores.",
        error_messages = {'invalid': "Stick to letters, digits and underscores.", 'required': "Gotta pick a username!"})
    email = django.forms.EmailField(error_messages={
        'required': "Your email address is required. We promise to use it respectfully.",
        'invalid': "This email address looks fishy. Real, or malarkey?"})
    class Meta:
        model = django.contrib.auth.models.User
        fields = ('username', 'email', 'password1')

    def __init__(self, *args, **kw):
        super(django.contrib.auth.forms.UserCreationForm,
                self).__init__(*args, **kw)
        custom_error_messages = {}
        custom_error_messages_dict = {
                "A user with that username already exists.": "Oops, we've already got a user in our database with that username. Pick another one!",
                "A user with that email already exists.": "We've already got a user in our database with that email address. Have you signed up before? (We'll have a password reset thinger shortly.)",
                }

        for fieldname in self.errors:
            for index, error_text in enumerate(self.errors[fieldname]):
                uet = unicode(error_text)
                self.errors[fieldname][index] = custom_error_messages_dict.get(uet, uet)

    def clean_email(self):
        """Verify that their email is unique."""
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise django.forms.ValidationError(
            "A user with that email already exists.")

class ShowEmailForm(django.forms.Form):
    show_email = django.forms.BooleanField(required=False)