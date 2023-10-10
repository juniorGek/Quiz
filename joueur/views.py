from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import json
import random
from django.http import JsonResponse

from .models import *


def home(request):
    return render(request, 'home.html')



def Login(request):
    
    if request.user.is_authenticated:
        return redirect('/game_home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authentification de l'utilisateur
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Connexion de l'utilisateur
            login(request, user)
            # Rediriger vers une page de succès ou la page d'accueil
            return redirect('/game_home')  # Remplacez 'success_view_name' par le nom de votre vue de succès
        else:
            # Afficher un message d'erreur en cas d'échec de l'authentification
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'Login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['cpw']
        
        # Vérifier que le nom d'utilisateur n'est pas déjà utilisé
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur est déjà utiliser.')
            return redirect('/login/')  # Remplacez 'registration/register.html' par votre propre modèle de formulaire d'inscription
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email deja utiliser.')
            return redirect('/login/')
        
          # Créer un nouvel utilisateur avec un mot de passe crypté
        user = User(username=username, email=email)
        user.set_password(password)  # Crypter le mot de passe
        user.save()
        
        messages.success(request, 'Compte creer avec succes.')
        return redirect('/login/')  # Remplacez 'registration/register.html' par votre propre modèle de formulaire d'inscription
        
        
    return render(request, 'Login.html')


def Logout(request):
    logout(request)
    return redirect('/')




@login_required(login_url=reverse_lazy('login'))
def game_home(request):
    category = Category.objects.all()
    return render(request, 'game_home.html', context={"category": category})


@login_required(login_url=reverse_lazy('login'))
def start(request):
    if request.method == 'POST':
        niveau = request.POST['niveau']
        category = request.POST['categorie']
        
        cat = Category.objects.filter(name=category).first() 
        questions = Question.objects.filter(category=cat, niveau=niveau)   
        if questions.count() <= 4:
            selected_questions = questions
        else:
            # Si le nombre total de questions est supérieur à 4, sélectionnez aléatoirement 4 questions
            selected_questions = random.sample(list(questions), 4)
            print(selected_questions)
        question_answer_dict = {}
        for question in selected_questions:
            question_answers = Answer.objects.filter(question=question)
            correct_answer = question_answers.filter(is_correct=True).first()
            question_answer_dict[question.pk] = {
                'question_text': question.text,
                'answers': [{'answer_text': answer.chosen_answer, 'is_correct': answer.is_correct} for answer in question_answers],
                'correct_answer': correct_answer.chosen_answer if correct_answer else None
            }
           
       # Triez le dictionnaire par les clés (identifiants des questions)
        sorted_question_answer_dict = dict(sorted(question_answer_dict.items()))
        print(category)
        context_data = {
            'question_answer_dict': sorted_question_answer_dict,
        }
        
        context_json = json.dumps(context_data)
        
        return render(request, 'start.html', context={'context_json': context_json, "niveau": niveau, "category": category})
    
    return render(request, 'game_home.html')


def score_enr(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score')
        level = data.get('level')

        # Enregistrez le score dans votre base de données
        # Votre logique d'enregistrement ici...
        print(score, level)
         
        # Réponse JSON
        response_data = {
            'message': 'Score enregistré avec succès.'
        }
        return JsonResponse(response_data)
    else:
        # Requête invalide
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def profile(request):
    return render(request, 'profile.html')