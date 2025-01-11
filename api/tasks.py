from .models import ContentLanguage
from api.enums import ContentLanguageStatus

def process_content_language(content_language_id):
    try:
        content_language = ContentLanguage.objects.get(id=content_language_id)
        content_language.status = ContentLanguageStatus.PROCESSING
        content_language.save()
        return f"Content language {content_language_id} processed successfully"
    except ContentLanguage.DoesNotExist:
        return f"Content language {content_language_id} not found" 