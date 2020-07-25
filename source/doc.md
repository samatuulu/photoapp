# Photos App
This document contains a short explanation of the features in the Photos app. You can also see the pieces of code
where I explain what it does. I also explain the core idea of the specific tasks below.

## List of functionalities and their reviews...

- Post a photo.
- Edit photo captions.
- Delete photos.
- List photos (all, my photos, my drafts) 

So, those are actually simple CRUD which is stands for Create, Read, Update and Delete.

Here is the actual code:

```cython
class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = Photo.objects.filter(author=self.request.user)
        return queryset
```

So the class `ModelViewSet` does the CRUD job me and I do not need to create 4 different views with 4 different
endpoints just for CRUD.  This is the advantage of using `ModelViewSet`.

- Save photos as draft.

```cython
STATUS_CHOICES = (
    ('publish', 'Publish'),
    ('unpublish', 'Unpublish')
)


class Photo(models.Model):
    ....
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    ...
```

For this functionality, I used the choice argument in the `status` parameter of the model `Photo`. By default, the status
parameter has a "Publish" value. So, users have options to save images as a draft and later
they can edit and publish it, for example. 

- Filter photos by user.

So basically, I used method called `get_queryset` which is returns list of objects in list.
In my case this method `get_queryset` returns only all the photos that user created.

- ASC/DESC Sort photos on publishing date

For this functionality, if you check the `models.py` file in directory `source/photos/` then 
at the end you should the class meta

```cython
    class Meta:
        ordering = ('-created_at',)
```
There is parameter in the model `Photo` that is called `created_at` this means that saves time when the object was created.
In order to show on publishing date I just wrote with minus sign `-created_at` which means the newer objects will be
on top of the list.  So `class Meta` acts as configuration and keeps configuration in one place.

- Limit the uploaded photo size to a certain maximum dimensions and bytes.

The directory `source/photos/models.py`. Inside the file `models.py`, I override the method `save`.

```cython
    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.photo.path)

        if image.height > 1000 or image.width > 1000:
            output_size = (1000, 1000)
            image.thumbnail(output_size)
            image.save(self.photo.path)
```

In this case, the method saves only saves images in specific settings. If the image size (height, width)
is more then 1000 height and width then the image will be saved as given parameter in variable `output_size`.
In this way, I can limit the image size.


- JWT authentication
Now these days JSON Web Tokens are getting popular.  JWT is used for authorization.  Which is means that the current
user has access to see the website.  Very good advantage of using JWT is JWT is not saves tokens in database.  Instead
JSON Web Token saves in the client side(chrome, firefox etc.).

As you can see here, there is an endpoints for register. After when users registers they get jwt token.

Local endpoint:

```cython
    http://localhost:8000/api/accounts/register/
```

and I need to send post request to that url with the parameters below:

```json
{
  "username": "test3",
  "password": "admin",
  "password_confirm" : "admin",
  "email": "test3@gmail.com"
}
```

after sending a post request, I get jwt token.
```json
{
"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU5NTc2MTY0MSwianRpIjoiN2Q3YTk3MzFlYmYzNDYwYmI2YzYyZjYzYTIzZmY2ZTkiLCJ1c2VyX2lkIjozfQ.-nqaQwucaBn_Ya8LZNmq4RRVwSJ1EfXk8Qmn1PK4Ctw",
"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk1Njc1NTQxLCJqdGkiOiJlMTNkOTBiZjBhZWI0OTYyOWEyZmM0Y2Y2ZGNhYjU0NyIsInVzZXJfaWQiOjN9.5SysmQA43-ShQrR1HQ_AVGrJAZhy9Nex-RbkPbbgU8k"
}
```
In response there are two parameters actually.  Because, the "access" token is used to authorize to certain page
and actions.  There is also "refresh" token.  A refresh token is a special token to generate an additional access tokens.
As you might already notes in response tokens are encrypted.  This is because of the security reason.

JSON Web Tokens consist of three parts separated by dots.
- Header
- Payload
- Signature
