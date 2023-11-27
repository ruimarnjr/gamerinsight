from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.views.generic.detail import DetailView
from .models import Game
from .forms import CommentForm

class GameListView(generic.ListView):
    model = Game
    template_name = 'index.html'
    context_object_name = 'games'

class GameDetailView(DetailView):
    model = Game
    template_name = 'game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        game = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.game = game
            comment.save()
            # Optionally, you can add a success message here
        else:
            # Optionally, you can add an error message here
            pass

        return render(request, 'game_detail.html', {'game': game, 'comment_form': comment_form})

class UserReviewsView(View):
    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        reviews = Review.objects.filter(game=game)
        return render(request, 'review_game.html', {'game': game, 'reviews': reviews})

# class UserProfileView(View):
#     def get(self, request, user_id):
#         user_profile = get_object_or_404(UserProfile, user_id=user_id)
#         return render(request, 'user_profile.html', {'user_profile': user_profile})

# class SubmitReviewView(View):
#     def get(self, request, game_id):
#         game = get_object_or_404(Game, pk=game_id)
#         form = ReviewForm()
#         return render(request, 'submit_review.html', {'form': form, 'game': game})

#     def post(self, request, game_id):
#         game = get_object_or_404(Game, pk=game_id)

#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.game = game
#             review.user = request.user
#             review.save()
#             return redirect('user_reviews', game_id=game_id)

#         return render(request, 'submit_review.html', {'form': form, 'game': game})

# class EditReviewView(View):
#     def get(self, request, review_id):
#         review = get_object_or_404(Review, pk=review_id, user=request.user)
#         form = ReviewForm(instance=review)
#         return render(request, 'edit_review.html', {'form': form, 'review': review})

#     def post(self, request, review_id):
#         review = get_object_or_404(Review, pk=review_id, user=request.user)

#         form = ReviewForm(request.POST, instance=review)
#         if form.is_valid():
#             form.save()
#             return redirect('user_reviews', game_id=review.game.pk)

#         return render(request, 'edit_review.html', {'form': form, 'review': review})

# class DeleteReviewView(View):
#     def post(self, request, review_id):
#         review = get_object_or_404(Review, pk=review_id, user=request.user)
#         game_id = review.game.pk
#         review.delete()
#         return redirect('user_reviews', game_id=game_id)

# class UserActivityFeedView(View):
#     def get(self, request, user_id):
#         activities = AdminActivity.objects.filter(user_id=user_id)
#         return render(request, 'user_activity_feed.html', {'activities': activities})
