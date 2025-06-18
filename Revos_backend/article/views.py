from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Article
from django.http import HttpResponse, JsonResponse
import logging
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

# 게시글 생성
@csrf_exempt
@require_http_methods(["POST"])
def create_article(request):
    try:
        # POST 요청에서 데이터 추출
        title = request.POST.get('title')
        text = request.POST.get('text')
        category = request.POST.get('category')
        img = request.FILES.get('img')

        # 필수 필드 검증
        if not all([title, text, category]):
            missing_fields = []
            if not title: missing_fields.append('title')
            if not text: missing_fields.append('text')
            if not category: missing_fields.append('category')
            return JsonResponse({
                'error': f'필수 필드가 누락되었습니다: {", ".join(missing_fields)}'
            }, status=400)

        # 새 게시글 생성
        article = Article.objects.create(
            title=title,
            text=text,
            category=category,
        )

        # 이미지가 있는 경우 게시글에 이미지 추가
        if img:
            article.img = img
            article.save()

        # 생성 성공 응답 반환
        return JsonResponse({
            'message': 'Article created successfully',
            'id': article.id
        }, status=201)

    except Exception as e:
        # 상세한 에러 로깅
        logger.error(f"Error creating article: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f'게시글 생성 중 오류가 발생했습니다: {str(e)}'
        }, status=500)

# 전체 게시글 목록 조회
def get_all_articles(request):
    try:
        articles = Article.objects.all().order_by('-created_at')
        article_list = []
        for article in articles:
            article_data = {
                'id': article.id,
                'title': article.title,
                'text': article.text,
                'category': article.category,
                'created_at': article.created_at.isoformat(),
            }
            
            # 이미지가 있는 경우에만 URL 추가
            if article.img:
                try:
                    article_data['img'] = article.img.url
                except:
                    article_data['img'] = None
            else:
                article_data['img'] = None
                
            article_list.append(article_data)

        return JsonResponse(article_list, safe=False)
    except Exception as e:
        logger.error(f"Error getting articles: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f'게시글 목록 조회 중 오류가 발생했습니다: {str(e)}'
        }, status=500)

# 단일 게시글 조회
def get_article_by_id(request):
    try:
        article_id = request.GET.get('id')
        article = get_object_or_404(Article, id=article_id)
        article_data = {
            'id': article.id,
            'title': article.title,
            'text': article.text,
            'category': article.category,
            'created_at': article.created_at.isoformat(),
        }
        
        # 이미지가 있는 경우에만 URL 추가
        if article.img:
            try:
                article_data['img'] = article.img.url
            except:
                article_data['img'] = None
        else:
            article_data['img'] = None
            
        return JsonResponse(article_data)
    except Exception as e:
        logger.error(f"Error getting article by id: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f'게시글 조회 중 오류가 발생했습니다: {str(e)}'
        }, status=500) 