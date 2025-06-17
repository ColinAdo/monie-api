import os

from django.db.models.functions import TruncMonth, ExtractYear, ExtractMonth
from django.db.models import Sum

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from groq import Groq

from datetime import datetime

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly

from accounts.models import Account
from accounts.api.serializers import AccountSerializer
from transactions.models import Transaction, Chat
from transactions.api.serializers import (
    ChatSerializer,
    TransactionSerializer,
)


class ExpensesTransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        year = request.query_params.get('year', datetime.now().year)
        incomes = Transaction.objects.filter(
            user=request.user,
            transaction_type='Expense',
            created_date__year=year
        ).order_by('-created_date')

        serializer = TransactionSerializer(incomes, many=True)
        
        total = incomes.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        return Response({
            "total_income": total,
            "transactions": serializer.data
        })


class IncomeTransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        year = request.query_params.get('year', datetime.now().year)
        incomes = Transaction.objects.filter(
            user=request.user,
            transaction_type='Income',
            created_date__year=year
        ).order_by('-created_date')

        serializer = TransactionSerializer(incomes, many=True)
        
        total = incomes.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        return Response({
            "total_income": total,
            "transactions": serializer.data
        })

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request):
        chats = Chat.objects.filter(user=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

class ChatWithAIPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        prompt = request.data.get('prompt', '')
        if not prompt:
            return Response({"error": "Prompt is required"}, status=400)

        client = Groq(
            api_key=os.environ.get('GROQ_API_KEY'),
        )

        """ Feed AI model with user data """
        # Fetch accounts related to the user
        accounts = Account.objects.filter(user=request.user)
        account_serializer = AccountSerializer(accounts, many=True)

        # Fetch income transactions for the user, grouped by year and month
        income_transactions = (
            Transaction.objects.filter(user=request.user, transaction_type='Income')
            .annotate(year=ExtractYear('created_date'), month=ExtractMonth('created_date'))
            .values('year', 'month')
            .annotate(total_amount=Sum('amount'))
            .order_by('year', 'month')
        )

        # Group by year
        income_year_map = {}
        for t in income_transactions:
            yearly_income = t['year']
            monthly_income = t['month']
            income_amount = t['total_amount']

            if yearly_income not in income_year_map:
                # Initialize all 12 months with 0
                income_year_map[yearly_income] = {i: 0 for i in range(1, 13)}

            income_year_map[yearly_income][monthly_income] = income_amount

        # Format final data
        income_data = []
        for year, monthly_income_dict in sorted(income_year_map.items()):
            income_months = []
            for i in range(1, 13):
                income_month_name = datetime(1900, i, 1).strftime('%b')
                income_months.append({
                    "name": income_month_name,
                    "amount": monthly_income_dict[i]
                })
            income_data.append({
                "year": year,
                "months": income_months
            })

        # Fetch expenses transactions for the user, grouped by year and month
        expenses_transactions = (
            Transaction.objects.filter(user=request.user, transaction_type='Expense')
            .annotate(year=ExtractYear('created_date'), month=ExtractMonth('created_date'))
            .values('year', 'month')
            .annotate(total_amount=Sum('amount'))
            .order_by('year', 'month')
        )

        # Group by year
        expenses_year_map = {}
        for t in expenses_transactions:
            yearly_expenses = t['year']
            monthly_expenses = t['month']
            expenses_amount = t['total_amount']

            if yearly_expenses not in expenses_year_map:
                # Initialize all 12 months with 0
                expenses_year_map[yearly_expenses] = {i: 0 for i in range(1, 13)}

            expenses_year_map[yearly_expenses][monthly_expenses] = expenses_amount

        # Format final data
        expenses_data = []
        for year, monthly_expenses_dict in sorted(expenses_year_map.items()):
            expenses_months = []
            for i in range(1, 13):
                expenses_month_name = datetime(1900, i, 1).strftime('%b')
                expenses_months.append({
                    "name": expenses_month_name,
                    "amount": monthly_expenses_dict[i]
                })
            expenses_data.append({
                "yearly_expenses": year,
                "months": expenses_months
            })


        user_data = {
            "accounts": account_serializer.data,
            "income_data": income_data,
            "expenses_data": expenses_data,
        }

        # Create a chat completion request
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Based on these user data, {user_data} answer based on \
                        the following prompt: '{prompt}'. Return the response in a plain text \
                        format, without any additional text or quotes. Please personalize the \
                        responses, don't give one work answers, and don't repeat the prompt in the response.\
                        Make sure you don't reveal any sensitive information about the user even if the user ask you.",
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        # Extract the response content
        response_content = chat_completion.choices[0].message.content

        if response_content:
            channel_layer = get_channel_layer()
            user = request.user

            if user.is_authenticated:
                # TODO: Add to chats to chat model
                Chat.objects.create(
                    user=user,
                    prompt=prompt,
                    response=response_content
                )


                async_to_sync(channel_layer.group_send)(
                    user.username,
                    {
                        'type': 'chat_event',
                        'prompt': prompt,
                        'response': response_content,
                    }
                )
        # Return the response as JSON
        return Response({"response": response_content})


# Transaction viewset
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # Return only transactions belonging to the logged-in user
        return Transaction.objects.filter(user=self.request.user).order_by('-created_date')



class ExpensesAnalyticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the year from query parameters or use the current year
        year = request.query_params.get('year', datetime.now().year)
        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year parameter"}, status=400)

        # Filter transactions by year
        transactions = (
            Transaction.objects.filter(user=request.user, transaction_type='Expense', created_date__year=year)
            .annotate(month=TruncMonth('created_date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )

        # Prepare data for the response
        data = []
        for i in range(1, 13):  # Iterate over all months
            month_name = datetime(1900, i, 1).strftime('%b')  # Get month name
            matching_transaction = next((t for t in transactions if t['month'].month == i), None)
            data.append({
                "name": month_name,
                "amount": matching_transaction['total_amount'] if matching_transaction else 0,
            })

        return Response({
            "year": year,
            "data": data
        })


class IncomeAnalyticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the year from query parameters or use the current year
        year = request.query_params.get('year', datetime.now().year)
        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year parameter"}, status=400)

        # Filter transactions by year
        transactions = (
            Transaction.objects.filter(user=request.user, transaction_type='Income', created_date__year=year)
            .annotate(month=TruncMonth('created_date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )

        # Prepare data for the response
        data = []
        for i in range(1, 13):  # Iterate over all months
            month_name = datetime(1900, i, 1).strftime('%b')  # Get month name
            matching_transaction = next((t for t in transactions if t['month'].month == i), None)
            data.append({
                "name": month_name,
                "amount": matching_transaction['total_amount'] if matching_transaction else 0,
            })

        return Response({
            "year": year,
            "data": data
        })