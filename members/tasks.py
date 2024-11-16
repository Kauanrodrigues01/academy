from celery import shared_task
from django.utils import timezone
from .models import Member

@shared_task
def update_members_activity_status():
    """Verifica se o pagamento do membro foi feito há mais de 1 mês e atualiza o status."""
    members = Member.objects.filter(is_active=True)

    for member in members:
        member.update_activity_status()
