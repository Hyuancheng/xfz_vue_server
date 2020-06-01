from django.shortcuts import render
from django.views import View


class PayInfoView(View):
    """支付信息"""

    def get(self, request):
        """展示支付页面"""
        return render(request, 'payinfo/payinfo.html')

