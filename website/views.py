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
    """This view is used to display the home page"""
    template_name = "index.html"

class GameListView(generic.ListView):
    model = Game
    template_name = 'games.html'
    queryset = Game.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'games'
    paginate_by = 8


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

class EditComment(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView):

    """
    This view is used to allow logged in users to edit their own comments
    """
    model = Comment
    form_class = CommentForm
    template_name = 'edit_comment.html'
    success_message = "Comment edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the comment.
        """
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        """
        Prevent another user from editing user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def get_success_url(self):
        """ Return to recipe detail view when comment updated sucessfully"""
        game = self.object.game
        return reverse_lazy('game_detail', kwargs={'pk': game.pk})


class DeleteComment(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):

    """
    This view is used to allow logged in users to delete their own comments
    """
    model = Comment
    template_name = 'delete_comment.html'
    success_message = "Comment deleted successfully"

    def test_func(self):
        """
        Prevent another user from deleting user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def delete(self, request, *args, **kwargs):
        """
        This function is used to display success message given
        SuccessMessageMixin cannot be used in generic.DeleteView.
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
        """
        messages.success(self.request, self.success_message)
        return super(DeleteComment, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        """ Return to recipe detail view when comment deleted sucessfully"""
        game = self.object.game
        return reverse_lazy('game_detail', kwargs={'pk': game.pk})

class AddGame(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
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
    """
    This view is used to allow logged in users to edit their own games
    """
    model = Game
    form_class = GameForm  # Make sure to use the correct GameForm
    template_name = 'edit_game.html'
    success_message = "%(title)s was edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed-in user is set as the author of the game.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Prevent another user from updating other's games
        """
        game = self.get_object()
        return game.author == self.request.user

    def get_success_message(self, cleaned_data):
        """
        Override the get_success_message() method to add the game title
        into the success message.
        source: https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        """
        return self.success_message % dict(
            cleaned_data, title=self.object.title
        )


class DeleteGame(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView
        ):
    """
    This view is used to allow logged in users to delete their own games
    """
    model = Game
    template_name = 'delete_game.html'
    success_message = "Game deleted successfully"
    success_url = reverse_lazy('games')

    def test_func(self):
        """
        Prevent another user from deleting other's games
        """
        game = self.get_object()
        return game.author == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        This function is used to display success message given
        SuccessMessageMixin cannot be used in generic.DeleteView.
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
        """
        messages.success(self.request, self.success_message)
        return super(DeleteGame, self).delete(request, *args, **kwargs)