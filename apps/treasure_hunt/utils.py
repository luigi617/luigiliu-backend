from django.core.mail import send_mail
def notification_treasure_processing():
    send_mail(
        "Treasure hunt",
        "Someone found a treasure or want to activate an hint",
        "limsevy@gmail.com",
        ["luigiliu617@gmail.com"],
        fail_silently=False,
    )
