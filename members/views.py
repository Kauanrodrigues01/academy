from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberEditForm, MemberPaymentForm, PaymentForm
from .models import Member
from django.shortcuts import render, get_object_or_404



        