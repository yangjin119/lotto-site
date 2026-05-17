import random
from django.contrib import admin
from django.contrib import messages
from .models import LottoRound, LottoTicket

def conduct_lotto_draw(modeladmin, request, queryset):
    """선택된 회차의 로또 추첨을 진행하고 티켓들의 등수를 일괄 판정하는 Admin Action"""
    for lotto_round in queryset:
        # 이미 추첨이 완료된 회차는 건너뜁니다.
        if lotto_round.is_drawn:
            messages.warning(request, f"제 {lotto_round.round_number}회차는 이미 추첨이 완료되었습니다.")
            continue
        
        # 1. 당첨 번호 무작위 생성 (1~45 중 중복 없이 7개 추출)
        # 앞의 6개는 당첨 번호, 마지막 1개는 보너스 번호
        all_numbers = random.sample(range(1, 46), 7)
        winning_numbers = sorted(all_numbers[:6])
        bonus_number = all_numbers[6]
        
        # 2. 회차 데이터에 당첨 번호 업데이트
        lotto_round.num1 = winning_numbers[0]
        lotto_round.num2 = winning_numbers[1]
        lotto_round.num3 = winning_numbers[2]
        lotto_round.num4 = winning_numbers[3]
        lotto_round.num5 = winning_numbers[4]
        lotto_round.num6 = winning_numbers[5]
        lotto_round.bonus_num = bonus_number
        lotto_round.is_drawn = True
        lotto_round.save()
        
        # Set 자료형을 만들어 교집합(&) 연산으로 맞은 개수를 쉽게 구합니다.
        winning_set = set(winning_numbers)
        
        # 3. 해당 회차에 판매된 모든 티켓 가져오기
        tickets = LottoTicket.objects.filter(lotto_round=lotto_round)
        
        updated_count = 0
        for ticket in tickets:
            user_numbers = set(ticket.get_numbers())
            # 당첨 번호 6개와 사용자가 고른 번호 6개의 교집합 개수
            match_count = len(winning_set & user_numbers)
            
            # 등수 판정 알고리즘
            if match_count == 6:
                ticket.rank = 1  # 1등
            elif match_count == 5 and (bonus_number in user_numbers):
                ticket.rank = 2  # 2등 (5개 + 보너스 일치)
            elif match_count == 5:
                ticket.rank = 3  # 3등
            elif match_count == 4:
                ticket.rank = 4  # 4등
            elif match_count == 3:
                ticket.rank = 5  # 5등
            else:
                ticket.rank = 0  # 낙첨
                
            ticket.save()
            updated_count += 1
            
        messages.success(
            request, 
            f"🎉 제 {lotto_round.round_number}회차 추첨 완료! "
            f"당첨번호: {winning_numbers} + 보너스: {bonus_number} "
            f"(총 {updated_count}장의 티켓 판정 완료)"
        )

# 관리자 페이지 상단에 노출될 설명 문구 설정
conduct_lotto_draw.short_description = "선택한 회차 로또 추첨 진행하기"


class LottoRoundAdmin(admin.ModelAdmin):
    # 관리자 목록 화면에서 보여줄 필드들 지정
    list_display = ['round_number', 'get_winning_numbers', 'bonus_num', 'is_drawn', 'draw_date']
    # 우리가 만든 추첨 기능을 액션 메뉴에 추가
    actions = [conduct_lotto_draw]

    def get_winning_numbers(self, obj):
        if obj.is_drawn:
            return f"{obj.num1}, {obj.num2}, {obj.num3}, {obj.num4}, {obj.num5}, {obj.num6}"
        return "추첨 전"
    get_winning_numbers.short_description = "당첨 번호"


class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'lotto_round', 'purchase_type', 'get_ticket_numbers', 'rank', 'purchase_date']
    list_filter = ['lotto_round', 'rank', 'purchase_type'] # 우측 사이드바 필터 기능 제공

    def get_ticket_numbers(self, obj):
        return f"{obj.num1}, {obj.num2}, {obj.num3}, {obj.num4}, {obj.num5}, {obj.num6}"
    get_ticket_numbers.short_description = "선택 번호"


# 커스텀 관리자 클래스 등록
admin.site.register(LottoRound, LottoRoundAdmin)
admin.site.register(LottoTicket, LottoTicketAdmin)