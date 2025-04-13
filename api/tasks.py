from .models import ContentLanguage, PromptHistory, ContentVersion
from api.enums import PromptHistoryStatus
from openai import OpenAI

# Configure OpenAI API
client = OpenAI()

def process_prompt_history(prompt_history_id):
    prompt_history = PromptHistory.objects.get(id=prompt_history_id)
    prompt_history.status = PromptHistoryStatus.PROCESSING
    prompt_history.save()

    try:

        # Read prompt template from file
        with open('data/prompt.txt', 'r') as f:
            prompt_template = f.read()

        # Send request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_template},
                {"role": "user", "content": f"{{ 'language': '{prompt_history.language.name}', 'topic': '{prompt_history.content.title}', 'content': '{prompt_history.prompt}', 'keywords': '{prompt_history.content.keywords}' }}"},
            ],
            max_tokens=5_000,
            temperature=0,
            response_format={"type": "json_object"},
        )

        # Get OpenAI response
        ai_response = response.choices[0].message.content

        print("TASK -----")
        print({"role": "user", "content": f"{{ 'language': '{prompt_history.language.name}', 'topic': '{prompt_history.content.title}', 'content': '{prompt_history.prompt}', 'keywords': '{prompt_history.content.keywords}' }}"})
        print(ai_response)
        print("<<<< -----")

        # Validate JSON format and required keys
        try:
            import json
            response_data = json.loads(ai_response)
            
            required_keys = [
                'slug', 'title_tag', 'meta_description', 'meta_keywords',
                'og_title', 'og_description', 'twitter_title',
                'twitter_description', 'content'
            ]
            
            # Check if all required keys exist
            missing_keys = [key for key in required_keys if key not in response_data]
            if missing_keys:
                raise ValueError(f"Missing required keys in response: {', '.join(missing_keys)}")

            # Get latest version number for this content and language
            latest_version = ContentVersion.objects.filter(
                content=prompt_history.content,
                language=prompt_history.contentLanguage.language
            ).order_by('-version').first()

            version_number = 1
            if latest_version:
                version_number = latest_version.version + 1

            # Create and save ContentVersion
            content_version = ContentVersion.objects.create(
                generated_text=response_data['content'],
                slug=response_data['slug'],
                title_tag=response_data['title_tag'],
                meta_description=response_data['meta_description'],
                meta_keywords=response_data['meta_keywords'],
                og_title=response_data['og_title'],
                og_description=response_data['og_description'],
                twitter_title=response_data['twitter_title'],
                twitter_description=response_data['twitter_description'],
                content=prompt_history.content,
                language=prompt_history.contentLanguage.language,
                prompt=prompt_history,
                version=version_number,
            )
            
            prompt_history.status = PromptHistoryStatus.COMPLETED
            prompt_history.contentVersion = content_version
            prompt_history.save()

        except json.JSONDecodeError:
            prompt_history.status = PromptHistoryStatus.FAILED
            prompt_history.status_reason = "Invalid JSON response from OpenAI"
            prompt_history.save()
            raise ValueError("Invalid JSON response from OpenAI")

        return f"Prompt {prompt_history_id} processed successfully"
    except PromptHistory.DoesNotExist:
        prompt_history.status = PromptHistoryStatus.FAILED
        prompt_history.save()
        print(f"Prompt {prompt_history_id} not found")
        return f"Prompt {prompt_history_id} not found"
    except Exception as e:
        # Mark PromptHistory as failed in case of error
        prompt_history.status = PromptHistoryStatus.FAILED
        prompt_history.save()
        print(f"Error processing prompt {prompt_history_id}: {str(e)}")
        return f"Error processing prompt {prompt_history_id}: {str(e)}"