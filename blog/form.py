from django import forms
from django.core.exceptions import ValidationError
from blog.models import UserProfile


def words_validator(comment):
    if len(comment) < 1:
        raise ValidationError('一个字都不说不太好吧！')


def comment_validator(comment):
    INVALID_WORDS = ['傻b', '傻逼', '脑残', 'sb', '尼玛', '妈']
    if any(comment.__contains__(word) for word in INVALID_WORDS):
        raise ValidationError('艹，想骂人是不是！')


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(),
                              error_messages={
                                  'required': '一个字都不说不太好吧！'
                                  },
                              validators=[words_validator, comment_validator]
                              )


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserProfileForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 'gender'
        ]

        labels = {
            'profile_image': 'Image',
            'gender': 'Gender',
        }

        widgets = {
            'profile_image': forms.FileInput(
                attrs={'class': 'ui input'},
            )
        }
