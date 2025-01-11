from .models import ContentLanguage, PromptHistory, ContentVersion
from api.enums import PromptHistoryStatus
from openai import OpenAI

# Configure OpenAI API
client = OpenAI()

def process_prompt_history(prompt_history_id):
    try:
        prompt_history = PromptHistory.objects.get(id=prompt_history_id)
        prompt_history.status = PromptHistoryStatus.PROCESSING
        prompt_history.save()

        # Send request to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_history.prompt},
            ]
        )

        # Get OpenAI response
        ai_response = response.choices[0].message.content

        print("Task Worker!!!")
        print(ai_response)
        print("<<<<<")

        # Create and save ContentVersion
        # content_version = ContentVersion.objects.create(
        #      prompt_history=prompt_history,
        #      content=ai_response,
        #      version=1  # Set first version as 1
        # )
        #
        # # Mark PromptHistory as completed
        # prompt_history.status = PromptHistoryStatus.COMPLETED
        # prompt_history.save()

        return f"Prompt {prompt_history_id} processed successfully"
    except PromptHistory.DoesNotExist:
        return f"Prompt {prompt_history_id} not found"
    except Exception as e:
        # Mark PromptHistory as failed in case of error
        prompt_history.status = PromptHistoryStatus.FAILED
        prompt_history.save()
        return f"Error processing prompt {prompt_history_id}: {str(e)}"