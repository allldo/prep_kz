from django.shortcuts import render


def main_forum(request):
    return render(request, 'forum/forum_main.html')
