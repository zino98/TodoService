from django.views import View
# CSRF 설정을 위한 import
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# 데이터 모델을 가져오기 위한 import
from .models import Todo

# 날짜와 시간을 위한 import
from datetime import datetime

# JSON으로 응답을 하기 위한 import
from django.http import JsonResponse

# 클라이언트의 정보를 JSON 문자열로 만들기 위한 import
import json

# Todo 클래스의 인스턴스를 딕셔너리로 변환해주는 함수, dict는 JSON 문자열과 표현 방법이 같다.
# 매개변수에 자료형을 기재하고 return type을 기재하는 형태로 만들어주는 것이 좋다.
def todoToDictionary(todo:Todo) -> dict:
    result = {
        "id" : todo.id,
        "userid" : todo.userid,
        "title" : todo.title,
        "done" : todo.done,
        "regdate" : todo.regdate,
        "moddate" : todo.moddate
    }


# CSRF 설정으로 클라이언트 어플리케이션을 별도로 구현하는 경우에 필수
@method_decorator(csrf_exempt, name='dispatch')
class TodoView(View):
    def post(self, request):
        # 클라이언트 데이터 가져오기
        request = json.loads(request.body)

        # userid 와 title 매개변수 값 읽어서 저장
        userid = request["userid"]
        title = request["title"]

        # 모델 인스턴스 생성
        todo = Todo()
        todo.userid = userid
        todo.title = title

        todo.save()

        # userid와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userid=userid)

        # 결과 리턴
        return JsonResponse({"list": list(todos.values())})
    
    def get(self, request):
        userid = request.GET["userid"]
        todos = Todo.objects.filter(userid=userid)
        return JsonResponse({"list": list(todos.values())}) # 목록을 리턴할 때는 None이 아닌 빈 리스트
    
    def put(self, request):
        # 클라이언트 데이터 읽어오기
        request = json.loads(request.body)

        id = request["id"]
        userid = request["userid"]
        done = request["done"]

        # 수정할 때, 인스턴스를 생성하는 것이 아니라 id 값으로 가져온다.
        todo = Todo.objects.get(id=id)
        todo.id = id
        todo.userid = userid
        todo.done = done

        todo.save()

        todos = Todo.objects.filter(id=id)
        return JsonResponse({"list": list(todos.values())})
    
    def delete(self, request):

        request = json.loads(request.body)

        userid = request["userid"]
        id = request["id"]

        # 삭제할 데이터를 찾아온다.
        todo = Todo.objects.get(id=id)

        if userid == todo.userid:
            todo.delete()

        todos = Todo.objects.filter(userid=userid)
        return JsonResponse({"list": list(todos.values())})
