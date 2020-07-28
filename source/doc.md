# Photos App
This document contains a short explanation of the features in the Photos app.

## List of functionalities and their reviews...

- Post a photo.
- Edit photo captions.
- Delete photos.
- List photos (all, my photos, my drafts) 

Those are actually simple CRUD which is stands for Create, Read, Update and Delete.

So the class `PhotoViewSet` by inheriting from bult-in `viewsets`. Viewsets does the CRUD job me and I do not need to
create 4 different views with 4 different endpoints just for CRUD.  This is the advantage of using Viewsets`.

- Save photos as draft.

For this functionality, I used the choice argument in the `status` parameter of the model `Photo`. By default, the status
parameter has a "Publish" value.  Users have options to save images as a draft and later
they can edit and publish it, for example. 

- Filter photos by user.

So basically, I used method called `get_queryset` which is returns list of objects in list.
In my case this method `get_queryset` returns only all the photos that user created
but before it method check user credentials.

- ASC/DESC Sort photos on publishing date

If you check the `models.py` file in directory `source/photos/` then at the end you should see the `Class Meta`
There is parameter `created_at` in the model `Photo`.  Created at - parameter saves time
when the object is first created (yes, I have argument `auto_now_add=True`, for that)
In order to show on publishing date I just wrote with minus sign `-created_at` which means the newer objects will be
on top of the list.  So `class Meta` acts as configuration and keeps configuration in one place.

- Limit the uploaded photo size to a certain maximum dimensions and bytes.

The directory `source/photos/models.py`. Inside the file `models.py`, I override the method `save`.
In this case, the method saves only image in specific settings.

- JWT authentication

Now these days JSON Web Tokens are getting popular.  JWT is used for authorization.  Which is means that the current
user has access to see the website.  Very good advantage of using JWT is JWT is not saves tokens in database.  Instead,
JSON Web Token lives in the client side(chrome, firefox etc.).

As you can see here, there is an endpoints for register. After when users registers they get JSON Web Token.

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

The next functionality is...

- Support #tags in captions, and filtering on the same

For this task, I override the method `create` inside the class `PhotoViewSet`. The main idea of `create` method is
when the `Photo` object created after that with the help of regular expression, I get all the tags from the caption and
save it to the other model Tag.  For creating tags, I used `get_or_create`, 
for the reason not saving the same tag again and again.

- Implement batch upload, edit, delete, publish API for photos

For now only upload feature works for photos. By sending a post request to the
<a href="http://localhost:8000/api/v1/add/photos/">endpoint</a>  users can send multiple images.