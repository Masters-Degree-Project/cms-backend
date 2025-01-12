from rest_framework.views import APIView
from rest_framework.response import Response

from .enums import PromptHistoryStatus
from .models import Content, ContentLanguage, Language, PromptHistory, ContentVersion
from .queue import add_to_queue

class ContentView(APIView):
    def get(self, request):
        content = Content.objects.all().prefetch_related('content_language')

        response = []
        for c in content:
            languages = [{ "id": cl.id, "language": cl.language.name, "iso_code": cl.language.iso_code } for cl in c.get_languages()]
            response.append({
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "keywords": c.keywords,
                "languages": languages,
            })
        
        return Response(response, status=200)

    def post(self, request):
        content = Content.objects.create(
            title=request.data.get('title'),
            description=request.data.get('description'),
            keywords=request.data.get('keywords'),
        )
        
        languages = request.data.get('languages')
        unique_languages = set(languages)
        languages_response = []
        
        for language_id in unique_languages:
            language = Language.objects.get(id=language_id)
            contentLang = ContentLanguage.objects.create(
                content=content,
                language=language,
            )

            prompt = PromptHistory.objects.create(
                content=content,
                language=language,
                contentLanguage=contentLang,
                prompt=content.description,
                status=PromptHistoryStatus.WAITING,
            )

            # Add to queue
            add_to_queue('prompt_queue', prompt.id)

            languages_response.append({
                "id": contentLang.id,
                "language": contentLang.language.name,
                "iso_code": contentLang.language.iso_code,
            })

        return Response({
            "id": content.id,
            "title": content.title,
            "description": content.description,
            "keywords": content.keywords,
            "languages": languages_response,
        }, status=201)

class ContentDetailView(APIView):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id, deleted_at=None)
        except Content.DoesNotExist:
            return Response({"message": "Content not found"}, status=404)

        languages = [{ "id": cl.id, "language": cl.language.name, "iso_code": cl.language.iso_code } for cl in content.content_language.all()]

        return Response({
            "id": content.id,
            "title": content.title,
            "description": content.description,
            "keywords": content.keywords,
            "languages": languages,
        }, status=200)

    # def post(self, request, content_id):
    #     try:
    #         content = Content.objects.get(id=content_id, deleted_at=None)
    #     except Content.DoesNotExist:
    #         return Response({"message": "Content not found"}, status=404)
    #
    #     content_languages = content.get_languages()
    #     for lang in content_languages:
    #         prompt = PromptHistory.objects.create(
    #             content=content,
    #             language=lang.language,
    #             contentLanguage=lang,
    #             prompt=request.data.get('prompt'),
    #             status=PromptHistoryStatus.WAITING,
    #         )
    #
    #         add_to_queue('prompt_queue', prompt.id)
    #
    #     return Response({
    #         "message": "Content added to queue",
    #     })

class ContentVersionView(APIView):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id, deleted_at=None)
        except Content.DoesNotExist:
            return Response({"message": "Content not found"}, status=404)

        try:
            content_versions = ContentVersion.objects.filter(content_id=content_id)
        except ContentVersion.DoesNotExist:
            return Response({"message": "Content not found"}, status=404)

        response = []
        for v in content_versions:
            response.append({
                "id": v.id,
            })

        return Response(response)

class ContentLanguageDetailView(APIView):
    def get(self, request, content_id, content_language_id):
        try:
            content = Content.objects.get(id=content_id, deleted_at=None)
        except Content.DoesNotExist:
            return Response({"message": "Content not found"}, status=404)

        try:
            content_language = ContentLanguage.objects.get(id=content_language_id, content_id=content_id)
        except ContentLanguage.DoesNotExist:
            return Response({"message": "Content Language not found"}, status=404)

        try:
            content_version = ContentVersion.objects.filter(content_id=content_id, language_id=content_language.language_id).order_by('-version').first()
        except ContentVersion.DoesNotExist:
            return Response({"message": "Content Version not found"}, status=404)

        if content_version is None:
            return Response({"message": "Content Version not found"}, status=404)

        return Response({
            "slug": content_version.slug,
            "title_tag": content_version.title_tag,
            "meta_description": content_version.meta_description,
            "meta_keywords": content_version.meta_keywords,
            "og_title": content_version.og_title,
            "og_description": content_version.og_description,
            "twitter_title": content_version.twitter_title,
            "twitter_description": content_version.twitter_description,
            "content": content_version.generated_text,
            "version": content_version.version,
        })

class LanguageView(APIView):
    def get(self, request):
        languages = Language.objects.all().prefetch_related('content_language')
        response = []
        for lang in languages:
            response.append({
                "id": lang.id,
                "name": lang.name,
            })

        return Response(response, status=200)