from celery import shared_task
from django.utils import timezone
from .models import Member

@shared_task
def update_members_activity_status():
    """Verifica se o pagamento do membro foi feito há mais de 1 mês e atualiza o status."""
    now = timezone.now().date()
    members = Member.objects.all()

    for member in members:
        # Verifica se passou 1 mês desde o pagamento
        if member.payment_date <= now - timezone.timedelta(days=30):
            # Se sim, desativa o membro
            member.is_active = False
            member.save()
