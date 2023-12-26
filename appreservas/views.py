from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Reserva
from .forms import ReservaForm

# Create your views here.
