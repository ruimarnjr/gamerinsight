from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic, View
from django.views.generic.detail import DetailView
from .models import Game
from .forms import CommentForm

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
        comments = game.comments.filter(approved=True).order_by("-created_on")

        return render(
            request,
            "game_detail.html",
            {
                "game": game,
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, pk):
        """
        This method is called when a POST request is made to the view
        via the comment form or the meal plan form.
        """
        queryset = Game.objects.filter(status=1)
    
    # Then, use 'queryset' to get 'game'
        game = get_object_or_404(queryset, pk=pk)
        comments = game.comments.filter(approved=True).order_by("-created_on")
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

        return render(
            request, 
            'game_detail.html', 
            {
                'game': game, 
                'comment_form': comment_form, 
                'commented': True,
                'comments': comments
            },
        )