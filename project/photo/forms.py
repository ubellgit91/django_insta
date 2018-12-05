from __future__ import unicode_literals

from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post # 연동시킬 model 지정
        fields = ('image', 'content') # form과 맵핑될 필드 지정.


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'content',
                    'placeholder': '댓글 달기...',
                }
            )
        }
    # content항목의 값을 검사하는 메소드.
    def clean_content(self):
        data = self.cleaned_data['content']
        errors =[]
        if data == '':
            errors.append(forms.ValidationError('댓글 내용을 입력해주세요'))
        elif len(data) > 50:
            errors.append(forms.ValidationError('댓글은 50자 미만으로 작성해주세요'))
        if errors:
            raise forms.ValidationError(errors)
        return data