from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Comment
from vote.models import Question

# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
def get_comments(request, vote_id):
    try:
        # 투표가 존재하는지 확인
        try:
            question = Question.objects.get(id=vote_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': '투표를 찾을 수 없습니다.'}, status=404)

        # 해당 투표의 모든 댓글 가져오기
        comments = Comment.objects.filter(question=question)
        
        comments_data = []
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'user': comment.user,
                'text': comment.text,
                'created_at': comment.created_at.isoformat()
            })

        return JsonResponse({
            'vote_id': vote_id,
            'comments': comments_data
        })

    except Exception as e:
        return JsonResponse({'error': f'댓글 조회 중 오류가 발생했습니다: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_comment(request):
    try:
        data = json.loads(request.body.decode())
        vote_id = data.get('vote_id')
        user = data.get('user')
        text = data.get('text')

        print(f"Received data: {data}")  # 디버깅용 로그

        if not vote_id or not user or not text:
            return JsonResponse({'error': 'vote_id, user, text가 모두 필요합니다.'}, status=400)

        # 투표가 존재하는지 확인
        try:
            question = Question.objects.get(id=vote_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': f'투표를 찾을 수 없습니다. vote_id: {vote_id}'}, status=404)

        # 댓글 생성
        comment = Comment.objects.create(
            question=question,
            user=user,
            text=text
        )

        return JsonResponse({
            'id': comment.id,
            'vote_id': vote_id,
            'user': comment.user,
            'text': comment.text,
            'created_at': comment.created_at.isoformat()
        }, status=201)

    except Exception as e:
        print(f"Error in create_comment: {str(e)}")  # 디버깅용 로그
        return JsonResponse({'error': f'댓글 생성 중 오류가 발생했습니다: {str(e)}'}, status=500)
