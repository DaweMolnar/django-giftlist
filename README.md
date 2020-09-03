[![<SemaphoreCI>](https://dawemolnar.semaphoreci.com/badges/django-giftlist.svg?style=shields)](https://dawemolnar.semaphoreci.com/projects/django-giftlist)
# django-giftlist
Wedding gift list creation site in django.

## How to start the django site
Pull down the newest docker image with
```
docker pull dawemolnar/django-giftlist
```
Run the docker image with
```
docker run -p 8020:8020 dawemolnar/django-giftlist 
```
If you want to set up a django admin user set the following environment variables:
| Variable name              | Value     |
| :------------------------- | :-------: |
| DJANGO_SUPERUSER_USERNAME  | user name |
| DJANGO_SUPERUSER_PASSWORD  | password  |
| DJANGO_SUPERUSER_EMAIL     | email     |

## How to use the site

After starting the docker image, you can reach the site on port 8020 with http://localhost:8020

You can buy gifts from the gift list without logging in, but for other features, you have to authenticate first.

Currently there is no multiple user support, the username and password are the following (can be also found in the populate.py script):
| Username     | Password   |
| :----------- | :--------: |
| testCouple   | password   |

## Possible improvements
* Multiple user support
* Multiple gift list support
* New user registration
* Creating new gift lists
* New user type for guests: Can only be registered with an invitation from a couple, and can only see the inviting couple's gift lists
* Fix security issues
* Use persistent database instead of local SQLite
