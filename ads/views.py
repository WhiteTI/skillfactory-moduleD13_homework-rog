from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from .forms import AdForm, ReviewForm
from .models import Ad, Review, Profile


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


@login_required
def edit_ad(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})


@login_required
def create_review(request, ad_id):
    ad = Ad.objects.get(id=ad_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ad = ad
            review.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = ReviewForm()
    return render(request, 'ads/create_review.html', {'form': form, 'ad': ad})


@login_required
def user_profile(request):
    user = request.user
    ads = Ad.objects.filter(user=user)
    reviews = Review.objects.filter(ad__in=ads)
    return render(request, 'ads/user_profile.html', {'ads': ads, 'reviews': reviews})


def accept_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.accepted = True
    review.save()
    send_mail(
        'Ваш отзыв был принят',
        'Ваш отзыв был принят и опубликован на сайте.',
        'noreply@example.com',
        [review.user.email],
        fail_silently=False,
    )
    return render(request, 'ads/accept_review.html')


@login_required
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    reviews = Review.objects.filter(ad=ad)
    return render(request, 'ads/ad_detail.html', {'ad': ad, 'reviews': reviews})


def ad_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ad_list.html', {'ads': ads})


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        confirmation_code = get_random_string(length=20)
        profile = Profile(user=user, confirmation_code=confirmation_code)
        profile.save()
        subject = render_to_string('ads/registration_email_subject.txt')
        body = render_to_string('ads/registration_email_body.txt', {'confirmation_code': confirmation_code})
        send_mail(subject, body, settings.EMAIL_HOST_USER, [email])
        return redirect('registration_confirmation')
    return render(request, 'ads/register.html')
