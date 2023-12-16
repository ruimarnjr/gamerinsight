from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .models import Game, GameCollectionItem
from .forms import CommentForm, GameCollectionForm 

class Home(generic.TemplateView):
    """This view is used to display the home page"""
    template_name = "index.html"

class GameListView(generic.ListView):
    model = Game
    template_name = 'games.html'
    queryset = Game.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'games'
    paginate_by = 6


class GameDetailView(DetailView):
    model = Game
    template_name = 'game_detail.html'
    context_object_name = 'game'
    paginate_by = 6

    def get(self, request, pk):
        """
        Retrieve the game and related comments from the database
        """
        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        comments = game.comments.order_by("-created_on")

        return render(
            request,
            "game_detail.html",
            {
                "game": game,
                "comments": comments,
                "comment_form": CommentForm(),
                "gamecollection_form": GameCollectionForm(),
            },
        )

    def post(self, request, pk):
        """
        This method is called when a POST request is made to the view
        via the comment form or the game collection form.
        """
        queryset = Game.objects.filter(status=1)
    
    # Then, use 'queryset' to get 'game'
        game = get_object_or_404(queryset, pk=pk)
        comments = game.comments.order_by("-created_on")
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.game = game
            comment.save()
            messages.success(self.request, 'Comment successfully added')
        else:
            comment_form = CommentForm()

        gamecollection_form = GameCollectionForm(data=request.POST)

        if gamecollection_form.is_valid():
            # get existing mpi record for user / stage
            queryset = GameCollectionItem.objects.filter(
                user=request.user, stage=request.POST['stage'])
            gamecollection_item = queryset.first()

            # if the game item already exists for that stage
            if gamecollection_item:
                # over write existing game
                gamecollection_item.game = game
                messages.success(self.request, 'Game successfully updated')
            else:
                gamecollection_item = gamecollection_form.save(commit=False)
                gamecollection_item.user = request.user
                gamecollection_item.game = game
                messages.success(self.request, 'Game added to Game Collection')

            gamecollection_item.save()

            return redirect('game_collection')

        else:
            gamecollection_form = GameCollectionForm()


        return render(
            request, 
            'game_detail.html', 
            {
                'game': game,
                'comments': comments,
                "comment_form": comment_form,
                "gamecollection_form": gamecollection_form
            },
        )


class GameCollection(LoginRequiredMixin, View):
    """This view renders the logged-in user's Game Collection"""

    def get(self, request):
        """
        Filters the GameCollection table by user and creates a dictionary with
        status and game collection item as a key, value pair.
        """
        user_game_collection_items = GameCollectionItem.objects.filter(user=request.user)

        stages = {
            0: 'Playing',
            1: 'Queued',
            2: 'Completed',
            3: 'Interested',
            4: 'Abandoned'        
        }
        gamecollection = {}

        for ind, stage in stages.items():
            stage_game_collection_item = user_game_collection_items.filter(stage=ind).first()
            gamecollection[stage] = stage_game_collection_item or None

        return render(
            request, 'game_collection.html', {'gamecollection': gamecollection})


