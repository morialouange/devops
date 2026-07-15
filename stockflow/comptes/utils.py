def enregistrer_action(utilisateur, action, objet='', details=''):
    from .models import JournalActivite
    JournalActivite.objects.create(utilisateur=utilisateur, action=action, objet=objet, details=details)
