from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


class ContentsView(View):
    """显示首页信息"""
    def get(self,request):
        """
        返回首页
        :param request:
        :return:
        """

        return render(request,'index.html')