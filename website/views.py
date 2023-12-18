from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic, View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import DetailView
from .models import Game, GameCollectionItem, Comment
from .forms import CommentForm, GameCollectionForm, GameForm


class Home(generic.TemplateView):
    """Home view rendering the index.html template."""
    template_name = "index.html"


class GameListView(generic.ListView):
    """View displaying a list of games."""
    model = Game
    template_name = 'games.html'
    queryset = Game.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'games'
    paginate_by = 8


class GameDetailView(DetailView):
    """View displaying details of a specific game."""
    model = Game
    template_name = 'game_detail.html'
    context_object_name = 'game'
    paginate_by = 6

    """All the code below was taken from
    PP4_My_Meal_Planner by AliOKeeffe and adapted"""

    def get(self, request, pk):
        """Handles GET requests for the game detail page."""
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
        """Handles POST requests for the game detail page."""
        queryset = Game.objects.filter(status=1)

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
            queryset = GameCollectionItem.objects.filter(
                user=request.user, stage=request.POST['stage'])
            gamecollection_item = queryset.first()

            if gamecollection_item:
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
    """View displaying the user's game collection."""
    def get(self, request):
        user_game_collection_items = GameCollectionItem.objects.filter(
            user=request.user
            )

        stages = {
            0: 'Playing',
            1: 'Queued',
            2: 'Completed',
            3: 'Interested',
            4: 'Abandoned',
        }
        gamecollection = {}

        for ind, stage in stages.items():
            stage_game_collection_item = user_game_collection_items.filter(
                stage=ind).first()
            gamecollection[stage] = stage_game_collection_item or None

        return render(
            request,
            'game_collection.html', {'gamecollection': gamecollection})


class EditComment(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView):
    """View for editing a user's comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'edit_comment.html'
    success_message = "Comment edited successfully"

    def form_valid(self, form):
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return comment.name == self.request.user.username

    def get_success_url(self):
        game = self.object.game
        return reverse_lazy('game_detail', kwargs={'pk': game.pk})


class DeleteComment(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """View for deleting a user's comment."""
    model = Comment
    template_name = 'delete_comment.html'
    success_message = "Comment deleted successfully"

    def test_func(self):
        comment = self.get_object()
        return comment.name == self.request.user.username

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteComment, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        game = self.object.game
        return reverse_lazy('game_detail', kwargs={'pk': game.pk})


class AddGame(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """View for adding a new game."""
    model = Game
    form_class = GameForm
    template_name = 'add_game.html'
    success_message = "%(title)s was created successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )


class EditGame(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView
        ):
    """View for editing a user's game."""
    model = Game
    form_class = GameForm
    template_name = 'edit_game.html'
    success_message = "%(title)s was edited successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        game = self.get_object()
        return game.author == self.request.user

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data, title=self.object.title
        )


class DeleteGame(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView
        ):
    """View for deleting a user's game."""
    model = Game
    template_name = 'delete_game.html'
    success_message = "Game deleted successfully"
    success_url = reverse_lazy('games')

    def test_func(self):
        game = self.get_object()
        return game.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteGame, self).delete(request, *args, **kwargs)
