from django.db import models
from django.contrib.auth.models import User  # Si vous utilisez le modèle d'utilisateur intégré de Django

# Modèle de catégorie
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Modèle de question
class Question(models.Model):
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    correct_answer = models.TextField()
    
    def __str__(self):
        return self.text

# Modèle de jeu
class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)  # Utilisez ManyToManyField pour permettre plusieurs catégories
    difficulty = models.CharField(max_length=255)
    score = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Game by {self.user.username} - {', '.join([category.name for category in self.categories.all()])}"

# Modèle de réponse
class Answer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_answer = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Answer to {self.question.text} in Game {self.game.id}"

# Modèle d'entrée du tableau des scores
class ScoreboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisez User si vous utilisez le modèle d'utilisateur intégré
    total_score = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s score in {self.category.name} ({self.difficulty})"
