from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Content, ContentLanguage, Language
from .queue import add_to_queue

class ContentView(APIView):
    def get(self, request):
        content = Content.objects.all().prefetch_related('content_language')

        response = []
        for c in content:
            languages = [{ "language": cl.language.name, "iso_code": cl.language.iso_code, "status": cl.status } for cl in c.content_language.all()]
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
            lang = ContentLanguage.objects.create(
                content=content,
                language=Language.objects.get(id=language_id),
            )
            
            # Add to queue
            add_to_queue('content_language_queue', lang.id)

            languages_response.append({
                "language": lang.language.name,
                "iso_code": lang.language.iso_code,
                "status": lang.status,
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

        languages = [{ "language": cl.language.name, "iso_code": cl.language.iso_code, "status": cl.status } for cl in content.content_language.all()]

        return Response({
            "id": content.id,
            "title": content.title,
            "description": content.description,
            "keywords": content.keywords,
            "languages": languages,
        }, status=200)