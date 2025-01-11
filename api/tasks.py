from .models import ContentLanguage, PromptHistory
from api.enums import PromptHistoryStatus

def process_prompt(prompt_history_id):
    try:
        promptHistory = PromptHistory.objects.get(id=prompt_history_id)
        promptHistory.status = PromptHistoryStatus.PROCESSING
        promptHistory.save()

        ## TODO: call openai here!!

        ## TODO: create new content language

        return f"Prompt {prompt_history_id} processed successfully"
    except ContentLanguage.DoesNotExist:
        return f"Prompt {prompt_history_id} not found"