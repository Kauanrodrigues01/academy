from django.db import models
from django.utils import timezone
from django.db.models import Sum, Min, Max, Count

class Member(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    start_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)  # Atualizado dinamicamente
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name}'

    @property
    def last_payment_date(self):
        """Retorna a última data de pagamento do membro ou None se não houver pagamentos."""
        
        last_payment = self.payments.aggregate(last_payment=Max('payment_date'))['last_payment']
        
        return last_payment

    def update_activity_status(self):
        """Atualiza o status de atividade do membro com base na última data de pagamento."""
        now = timezone.now().date()

        if self.last_payment_date and self.last_payment_date < now - timezone.timedelta(days=30):
            self.is_active = False
        else:
            self.is_active = True
            
        self.save()
    

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='payments')
    payment_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    
    def __str__(self):
        if self.member:
            return f'{self.member.full_name} | {self.payment_date} | {self.amount}'
        else:
            return f'Pagamento sem membro associado | {self.payment_date} | {self.amount}'
    
    @classmethod
    def total_paid_in_the_month(cls):
        """Calcula o total de pagamento rebido em um mês"""
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        payments = Payment.objects.filter(
            payment_date__month=current_month,
            payment_date__year=current_year
        )
        
        # Nessa linha agrega um campo chamado total_in_the_month, mas esse campo não existe no modelo Payment, então tem que ser chamado como se fosse uma chave do dicionário
        payments = payments.aggregate(total_in_the_month=Sum('amount'))
        
        return payments['total_in_the_month'] or 0.00
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.member:
            self.member.update_activity_status()

    
    
    
    