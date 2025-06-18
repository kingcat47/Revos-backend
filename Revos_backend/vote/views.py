import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Question, Choice
from article.models import Article
from django.http import JsonResponse

@csrf_exempt
@require_http_methods(["GET"])
def get_votes_by_article(request, article_id):
    try:
        # 기사가 존재하는지 확인
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'error': '게시글을 찾을 수 없습니다.'}, status=404)

        # 해당 기사의 모든 질문(투표) 가져오기
        questions = Question.objects.filter(article=article)
        
        votes_data = []
        for question in questions:
            # 각 질문의 선택지들 가져오기
            choices = Choice.objects.filter(question=question)
            choices_data = []
            
            for choice in choices:
                choices_data.append({
                    'id': str(choice.id),
                    'text': choice.choice_text,
                    'vote_count': choice.votes
                })
            
            votes_data.append({
                'id': str(question.id),
                'title': question.question_text,
                'choices': choices_data
            })

        return JsonResponse(votes_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': f'투표 조회 중 오류가 발생했습니다: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_votes(request):
    try:
        data = json.loads(request.body.decode())
        article_id = data.get('articleId')
        votes = data.get('votes', [])

        if not article_id or not votes:
            return JsonResponse({'error': 'articleId 또는 votes가 누락되었습니다.'}, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'error': '게시글을 찾을 수 없습니다.'}, status=404)

        created_question_ids = []
        for vote in votes:
            title = vote.get('title')
            choices = vote.get('choices', [])
            if not title or not choices:
                continue
            question = Question.objects.create(
                article=article,
                question_text=title
            )
            for choice in choices:
                Choice.objects.create(
                    question=question,
                    choice_text=choice.get('text', '')
                )
            created_question_ids.append(question.id)

        return JsonResponse({
            'message': 'Questions and choices created successfully',
            'ids': created_question_ids
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': f'투표 생성 중 오류가 발생했습니다: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_vote(request):
    try:
        data = json.loads(request.body.decode())
        vote_id = data.get('voteId')  # Question ID
        choice_id = data.get('choiceId')  # Choice ID

        if not vote_id or not choice_id:
            return JsonResponse({'error': 'voteId 또는 choiceId가 누락되었습니다.'}, status=400)

        try:
            question = Question.objects.get(id=vote_id)
            choice = Choice.objects.get(id=choice_id, question=question)
        except Question.DoesNotExist:
            return JsonResponse({'error': '투표를 찾을 수 없습니다.'}, status=404)
        except Choice.DoesNotExist:
            return JsonResponse({'error': '선택지를 찾을 수 없습니다.'}, status=404)

        # 투표 수 증가
        choice.votes += 1
        choice.save()

        return JsonResponse({
            'message': '투표가 성공적으로 제출되었습니다.',
            'updated_votes': choice.votes
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': f'투표 제출 중 오류가 발생했습니다: {str(e)}'}, status=500)