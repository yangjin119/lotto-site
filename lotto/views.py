import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import LottoRound, LottoTicket

@login_required
def buy_lotto(request):
    if request.method == "POST":
        purchase_type = request.POST.get('purchase_type') # 'AUTO' 또는 'MANUAL'
        
        # 현재 진행 중인 최신 회차 가져오기 (추첨이 아직 안 된 회차)
        current_round = LottoRound.objects.filter(is_drawn=False).order_by('-round_number').first()
        
        if not current_round:
            return JsonResponse({'error': '현재 진행 중인 로또 회차가 없습니다. 관리자 페이지에서 회차를 먼저 생성해주세요.'}, status=400)

        if purchase_type == 'AUTO':
            # 1~45 중 6개 랜덤 추출 후 정렬
            numbers = sorted(random.sample(range(1, 46), 6))
            
        elif purchase_type == 'MANUAL':
            try:
                raw_numbers = [
                    int(request.POST.get('num1')),
                    int(request.POST.get('num2')),
                    int(request.POST.get('num3')),
                    int(request.POST.get('num4')),
                    int(request.POST.get('num5')),
                    int(request.POST.get('num6')),
                ]
                numbers = sorted(raw_numbers)
                
                # 유효성 검증 1: 1~45 범위 확인
                if any(n < 1 or n > 45 for n in numbers):
                    return JsonResponse({'error': '숫자는 1에서 45 사이여야 합니다.'}, status=400)
                
                # 유효성 검증 2: 중복 번호 확인
                if len(set(numbers)) != 6:
                    return JsonResponse({'error': '중복된 숫자가 있습니다.'}, status=400)
                    
            except (TypeError, ValueError):
                return JsonResponse({'error': '올바른 숫자 6개를 입력해주세요.'}, status=400)
        else:
            return JsonResponse({'error': '잘못된 구매 방식입니다.'}, status=400)

        # 티켓 저장
        ticket = LottoTicket.objects.create(
            user=request.user,
            lotto_round=current_round,
            purchase_type=purchase_type,
            num1=numbers[0],
            num2=numbers[1],
            num3=numbers[2],
            num4=numbers[3],
            num5=numbers[4],
            num6=numbers[5],
        )

        return JsonResponse({
            'message': '복권 구매가 완료되었습니다!',
            'round': current_round.round_number,
            'type': ticket.get_purchase_type_display(),
            'numbers': numbers
        })

    # GET 요청 시 구매 페이지 반환
    return render(request, 'lotto/buy.html')