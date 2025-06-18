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

        if not article_id:
            return JsonResponse({'error': 'articleId가 누락되었습니다.'}, status=400)

        # 투표 개수 제한 검사 (최소 1개, 최대 3개)
        if len(votes) < 1:
            return JsonResponse({'error': '최소 1개의 투표가 필요합니다.'}, status=400)
        
        if len(votes) > 3:
            return JsonResponse({'error': '최대 3개의 투표만 생성할 수 있습니다.'}, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return JsonResponse({'error': '게시글을 찾을 수 없습니다.'}, status=404)

        created_question_ids = []
        for vote in votes:
            title = vote.get('title')
            choices = vote.get('choices', [])
            
            # 투표 제목 검사
            if not title or not title.strip():
                return JsonResponse({'error': '투표 제목을 입력해주세요.'}, status=400)
            
            # 선택지 개수 제한 검사 (최대 5개)
            if len(choices) > 5:
                return JsonResponse({'error': '선택지는 최대 5개까지 가능합니다.'}, status=400)
            
            # 선택지 내용 검사
            if len(choices) < 1:
                return JsonResponse({'error': '최소 1개의 선택지가 필요합니다.'}, status=400)
            
            for choice in choices:
                if not choice.get('text') or not choice.get('text').strip():
                    return JsonResponse({'error': '모든 선택지에 내용을 입력해주세요.'}, status=400)
            
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
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': f'투표 생성 중 오류가 발생했습니다: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_vote(request):
    try:
        data = json.loads(request.body.decode())
        
        # 단일 투표인지 여러 투표인지 확인
        if isinstance(data, list):
            # 여러 투표 처리
            results = []
            for vote_data in data:
                vote_id = vote_data.get('voteId')
                choice_id = vote_data.get('choiceId')

                if not vote_id or not choice_id:
                    continue

                try:
                    question = Question.objects.get(id=vote_id)
                    choice = Choice.objects.get(id=choice_id, question=question)
                    
                    # 투표 수 증가
                    choice.votes += 1
                    choice.save()
                    
                    results.append({
                        'voteId': vote_id,
                        'choiceId': choice_id,
                        'updated_votes': choice.votes
                    })
                except (Question.DoesNotExist, Choice.DoesNotExist):
                    continue

            return JsonResponse({
                'message': f'{len(results)}개의 투표가 성공적으로 제출되었습니다.',
                'results': results
            }, status=200)
        else:
            # 단일 투표 처리 (기존 로직)
            vote_id = data.get('voteId')
            choice_id = data.get('choiceId')

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