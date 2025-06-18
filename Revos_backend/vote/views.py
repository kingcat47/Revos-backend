from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Vote
from article.models import Article
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

# 투표 생성
@csrf_exempt
@require_http_methods(["POST"])
def create_votes(request):
    try:
        # POST 요청에서 데이터 추출
        article_id = request.POST.get('articleId')
        title = request.POST.get('title')
        description = request.POST.get('description')

        # 필수 필드 검증
        if not all([article_id, title, description]):
            missing_fields = []
            if not article_id: missing_fields.append('articleId')
            if not title: missing_fields.append('title')
            if not description: missing_fields.append('description')
            return JsonResponse({
                'error': f'필수 필드가 누락되었습니다: {", ".join(missing_fields)}'
            }, status=400)

        # 게시글 조회
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'error': '게시글을 찾을 수 없습니다.'}, status=404)

        # 투표 생성
        vote = Vote.objects.create(
            article=article,
            title=title,
            description=description
        )

        return JsonResponse({
            'message': 'Vote created successfully',
            'id': vote.id
        }, status=201)

    except Exception as e:
        logger.error(f"Error creating vote: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f'투표 생성 중 오류가 발생했습니다: {str(e)}'
        }, status=500) 