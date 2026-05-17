from django.db import models
from django.contrib.auth.models import User

class LottoRound(models.Model):
    """추첨 회차 정보 테이블 (관리자가 생성)"""
    round_number = models.PositiveIntegerField(unique=True, primary_key=True, verbose_name="회차")
    draw_date = models.DateTimeField(auto_now_add=True, verbose_name="추첨 일시")
    
    # 당첨 번호 6개 + 보너스 번호
    num1 = models.PositiveSmallIntegerField(verbose_name="번호 1", null=True, blank=True)
    num2 = models.PositiveSmallIntegerField(verbose_name="번호 2", null=True, blank=True)
    num3 = models.PositiveSmallIntegerField(verbose_name="번호 3", null=True, blank=True)
    num4 = models.PositiveSmallIntegerField(verbose_name="번호 4", null=True, blank=True)
    num5 = models.PositiveSmallIntegerField(verbose_name="번호 5", null=True, blank=True)
    num6 = models.PositiveSmallIntegerField(verbose_name="번호 6", null=True, blank=True)
    bonus_num = models.PositiveSmallIntegerField(verbose_name="보너스 번호", null=True, blank=True)
    
    is_drawn = models.BooleanField(default=False, verbose_name="추첨 완료 여부")

    def __str__(self):
        return f"제 {self.round_number}회 로또 추첨"


class LottoTicket(models.Model):
    """사용자가 구매한 복권 내역 테이블"""
    SELECTION_CHOICES = [
        ('AUTO', '자동'),
        ('MANUAL', '수동'),
    ]
    
    RANK_CHOICES = [
        (0, '미추첨/낙첨'),
        (1, '1등 (6개 일치)'),
        (2, '2등 (5개+보너스 일치)'),
        (3, '3등 (5개 일치)'),
        (4, '4등 (4개 일치)'),
        (5, '5등 (3개 일치)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="구매자")
    lotto_round = models.ForeignKey(LottoRound, on_delete=models.CASCADE, verbose_name="해당 회차")
    purchase_type = models.CharField(max_length=6, choices=SELECTION_CHOICES, verbose_name="구매 방식")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="구매 일시")

    # 선택한 번호 6개
    num1 = models.PositiveSmallIntegerField(verbose_name="번호 1")
    num2 = models.PositiveSmallIntegerField(verbose_name="번호 2")
    num3 = models.PositiveSmallIntegerField(verbose_name="번호 3")
    num4 = models.PositiveSmallIntegerField(verbose_name="번호 4")
    num5 = models.PositiveSmallIntegerField(verbose_name="번호 5")
    num6 = models.PositiveSmallIntegerField(verbose_name="번호 6")

    rank = models.PositiveSmallIntegerField(choices=RANK_CHOICES, default=0, verbose_name="당첨 결과")

    def __str__(self):
        return f"{self.user.username} - {self.lotto_round.round_number}회차 ({self.purchase_type})"
    def get_numbers(self):
        """6개의 로또 번호를 파이썬 리스트로 묶어서 반환해주는 함수"""
        return [self.num1, self.num2, self.num3, self.num4, self.num5, self.num6]