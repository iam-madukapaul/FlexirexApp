from django.shortcuts import render, redirect
from profiles.models import UserProfile
from .models import Account
from django.contrib import messages
from decimal import Decimal
from .models import Account, DepositHistory, Withdrawal, WithdrawalHistory
from django.utils import timezone
import random
import string
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def account(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        account, created = Account.objects.get_or_create(user_profile=user_profile)

    except UserProfile.DoesNotExist:
        user_profile = None
        account = None
    context = {
        'account': account,
        'user_profile': user_profile
    }
    return render(request, 'account.html', context)


def calculate_interest_earn(selected_plan, total_earning):
    interest_rates = {
        'Basic': Decimal(0.015),
        'Standard': Decimal(0.035),
        'Silver': Decimal(0.005),
        'Premium': Decimal(0.025),
        'Gold': Decimal(0.045),
        'Diamond': Decimal(0.055),
    }
    return total_earning * interest_rates[selected_plan]

@login_required(login_url='login')
def investment(request):
    user_profile = UserProfile.objects.get(user=request.user)
    account, created = Account.objects.get_or_create(user_profile=user_profile)
    plans = [
        {'name':'Basic Plan', 'value':'Basic', 'min_amount':50, 'max_amount':1000},
        {'name':'Standard Plan', 'value':'Standard', 'min_amount':5000, 'max_amount':50000},
        {'name':'Silver Plan', 'value':'Silver', 'min_amount':10000, 'max_amount':100000},
        {'name':'Premium Plan', 'value':'Premium', 'min_amount':1000, 'max_amount':10000},
        {'name':'Gold Plan', 'value':'Gold', 'min_amount':15000, 'max_amount':500000},
        {'name':'Diamond Plan', 'value':'Diamond', 'min_amount':50000, 'max_amount':1000000},
    ]
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        plan = request.POST.get('plan')
        payment_method = request.POST.get('payment_method')
        for p in plans:
            if p['value'] == plan:
                min_amount = p['min_amount']
                max_amount = p['max_amount']

                if amount < min_amount or amount > max_amount:
                    messages.warning(request, f"Invalid investment amount. Please enter an amount between ${min_amount} and ${max_amount}.")
                    return redirect('investment')
                else:
                    messages.success(request, 'Investment submitted... Pending admin approval')

                # Update the pending_amount based on the selected plan and amount
                total_earning = account.total_earning + amount
                account.interest_earn = calculate_interest_earn(plan, total_earning)
                account.total_earning = total_earning
                account.selected_plan = plan
                account.pending_amount = amount
                account.total_deposit += amount
                account.save()

                transaction = DepositHistory.objects.create(
                    user_profile=user_profile,
                    transaction_id=f"TRANS{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    selected_plan=plan,
                    deposit_amount=amount,
                    status='Pending',
                )
                transaction.save()

                # Redirect to the account view after successful form submission
                return redirect('account')
    if account.is_active:
        account.ultimate_balance = (
            account.interest_earn + account.total_earning + account.referral_earnings + account.lifetime_bonus
        )
        account.save()
    context = {
        'account': account,
        'user_profile': user_profile,
        'plans': plans
    }
    return render(request, 'investment.html', context)

def generate_transaction_id():
    letters = string.digits
    return 'TRANS' + ''.join(random.choice(letters) for _ in range(12))

@login_required(login_url='login')
def withdraw(request):
    # Retrieve the user profile associated with the currently logged-in user
    user_profile = UserProfile.objects.get(user=request.user)

    # Retrieve the user's account or create a new one if it doesn't exist
    account, created = Account.objects.get_or_create(user_profile=user_profile)

    if request.method == 'POST':
        # Handle the withdrawal form submission
        withdrawal_amount_str = request.POST.get('withdrawal_amount')

        if withdrawal_amount_str and withdrawal_amount_str.strip(): # Check if the input is not empty
            # Convert the withdrawal_amount to a Decimal
            withdrawal_amount = Decimal(withdrawal_amount_str)

            # Ensure that the withdrawal amount is not greater than the available balance
            if withdrawal_amount > account.ultimate_balance:
                # Display an error message or take appropriate action
                messages.warning(request, "Withdrawal amount cannot exceed the available balance.")
            else:
                transaction_id = generate_transaction_id()

                # Create a new withdrawal history record
                withdrawal_history = WithdrawalHistory.objects.create(
                    transaction_id=transaction_id,
                    user_profile=user_profile,
                    withdraw_amount=withdrawal_amount
                )

                # Create a new withdrawal transaction record
                Withdrawal.objects.create(
                    transaction_id=transaction_id,
                    user_profile=user_profile,
                    withdrawal_history=withdrawal_history
                )

                account.ultimate_balance -= withdrawal_amount
                account.total_earning -= withdrawal_amount
                account.total_payout += withdrawal_amount
                account.save()
                messages.success(request, 'Withdrawal submitted.')

                return redirect('account')

    context = {
        'account': account,
        'user_profile': user_profile,
    }

    return render(request, 'withdraw.html', context)


@login_required(login_url='login')
def history(request):
    user_profile = UserProfile.objects.get(user=request.user)
    account, created = Account.objects.get_or_create(user_profile=user_profile)
    transaction_history = DepositHistory.objects.filter(user_profile=user_profile).order_by('-transaction_date')

    context = {
        'transaction_history': transaction_history,
        'user_profile': user_profile,
        'account': account,
    }
    return render(request, 'history.html', context)

@login_required(login_url='login')
def withdrawal_history(request):
    user_profile = UserProfile.objects.get(user=request.user)
    account, created = Account.objects.get_or_create(user_profile=user_profile)
    withdrawal_history = WithdrawalHistory.objects.filter(user_profile=user_profile).order_by('-withdrawal_date')

    context = {
        'withdrawal_history':withdrawal_history,
        'user_profile': user_profile,
        'account': account,
    }
    return render(request, 'withdrawal_history.html', context)
    


def referral(request, referral_code):
    try:
        referrer_profile = UserProfile.objects.get(referral_code=referral_code)
        referrer_account, created = Account.objects.get_or_create(user_profile=referrer_profile)
        referral_earnings = Decimal('10.00')
        referrer_account.credit_referral_earnings(referral_earnings)
        messages.success(request, f"You've been referred by {referrer_profile.user.username}.")
    except UserProfile.DoesNotExist:
        messages.warning(request, "Invalid referral code.")
    request.session['referral_code'] = referral_code
    return redirect('register')

