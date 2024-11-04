# Install and Usage

## pip install


```
pip install django-commands2
```


## add django_commands to INSTALLED_APPS, and logging

```
INSTALLED_APPS = [
    ...
    'django_commands',
]
LOGGING = {
    "loggers": {
        "django_commands": {
            ...your custom level, handles config...
        }
    }
}
DJANGO_COMMANDS_ALLOW_REMOTE_CALL = [
    "slow_command",  # add slow_command if you want to run unittest
    <your command>
]
```

## add url config like:

```
path('api/django-commands/', include("django_commands.urls")),
```

## Call Command from url

```
import requests
requests.post("/api/django-commands/call-command", {"command": "slow_command"})
```
