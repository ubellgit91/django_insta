# Add or change a related_name argument to the definition for 'Post.author' or 'Post.author'.

## 설명

"If a model has a ForeignKey, instances of the foreign-key model will have access to a Manager that returns all instances of the first model. By default, this Manager is named FOO_set, where FOO is the source model name, lowercased."

But if you have more than one foreign key in a model, django is unable to generate unique names for foreign-key manager.
 You can help out by adding "related_name" arguments to the foreignkey field definitions in your models.

See here: <https://docs.djangoproject.com/en/dev/topics/db/queries/#following-relationships-backward>

## 예제

Example:

  

```
class Article(models.Model):
    author = models.ForeignKey('accounts.User')
    editor = models.ForeignKey('accounts.User')
```

  

This will cause the error, because Django tries to automatically create a backwards relation for instances of `accounts.User` for each foreign key relation to user like `user.article_set`.  This default method is ambiguous.  Would `user.article_set.all()` refer to the user's articles related by the author field, or by the editor field?

  

Solution:

  

```
class Article(models.Model):
    author = models.ForeignKey('accounts.User', related_name='author_article_set')
    editor = models.ForeignKey('accounts.User', related_name='editor_article_set')
```

  

Now, for an instance of user `user`, there are two different manager methods:  

  

1. `user.author_article_set` -- `user.author_article_set.all()` will return a Queryset of all Article objects that have author == user
2. `user.editor_article_set` -- `user.editor_article_set.all()` will return a Queryset of all Article objects that have editor == user