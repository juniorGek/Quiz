from django.db import models
from django.contrib.auth.models import User  # Si vous utilisez le modèle d'utilisateur intégré de Django
from django.utils import timezone
# Modèle de catégorie
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Modèle de question
class Question(models.Model):
    question = models.CharField(max_length=255 , null=True, blank=True)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=20 , null=True , blank=True)
    correct_answer = models.TextField()
    
    def __str__(self):
        return self.question

# Modèle de jeu
class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)  # Utilisez ManyToManyField pour permettre plusieurs catégories
    difficulty = models.CharField(max_length=255)
    score = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Game by {self.user.username} - {', '.join([category.name for category in self.categories.all()])}"

# Modèle de réponse
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"reponse de la {self.question.question}"

# Modèle d'entrée du tableau des scores
class ScoreboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisez User si vous utilisez le modèle d'utilisateur intégré
    total_score = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s score in {self.category.name} ({self.difficulty})"
