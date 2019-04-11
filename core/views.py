from django.shortcuts import render
from .models import Player, Comment

# Create your views here.
def index(request):
    """View function for home page of site"""

    players = Player.objects.all()

    context = {
        'players': players
    }

    return render(request, 'index.html', context=context)