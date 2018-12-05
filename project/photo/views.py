from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
#
from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.


class PostListView(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'photo/post_list.html', context)


class DetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk) # model 클래스의 객체를 pk에 맞춰서 get하고, 없으면 404 에러 페이지를 보냄.
        comment_form = CommentForm()
        context = {
            'post': post,
            'comment_form': comment_form,
        }

        return render(request, 'photo/post_detail.html', context)


class PostCreateView(View):
    # get방식으로 접근했을 때,
    def get(self, request):
        form = PostForm()
        ctx = {
            'form': form,
        }
        return render(request, 'photo/post_create.html', ctx)
    # post방식으로 접근했을 때.
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        ctx = {
            'form': form,
        }
        if form.is_valid(): # 유효성 검사.
            post = form.save(commit=False)
            post.author = request.user
            post.save()   # PhotoForm 폼의 인스턴스 객체에 상속받은 메서드. 폼 정보를 연결된 모델을 이용해 DB저장

            messages.success(request, '사진이 등록되었습니다.')
            return redirect('photo:list')
        return render(request, 'photo/post_create.html', ctx)


class CreateCommentView(View):
    def get(self, request):
        next_path = request.GET.get('next')
        if next_path:
            return redirect(next_path)
        return redirect('photo:list')

    def post(self, request, pk):
        # Post모델의 인스턴스를 pk로 검색해 가져오거나 없으면 404에러
        post = get_object_or_404(Post, pk=pk)
        # request.POST 데이터를 이용해 Bounded Form 객체를 생성함.
        comment_form = CommentForm(request.POST)
        # 올바른 데이터가 form에 바인딩 되어있는지 유효성 검사
        if comment_form.is_valid():
            # 유효성 검사에 통과하면 ModelForm의 save()호출로 인스턴스 생성
            # DB에 저장하지 않고 인스턴스만 생성하기 위해서 commit=False 필드옵션 지정
            comment = comment_form.save(commit=False)
            # CommentForm에 지정되지 않았으나 필수요소인 author와 post속성을 지정
            comment.post = post
            comment.author = request.user
            # DB에 저장
            comment.save()

            # 성공 메세지를 다음 request의 결과물로 전달
            messages.success(request, '댓글이 등록되었습니다.')
            
        else:
            # 유효성 검사에 실패한 경우
            # 에러 목록을 순회하며 에러메세지를 작성, messages의 error레벨로 추가
            error_msg = '댓글 등록에 실패했습니다.\n{}'.format(
                '\n'.join(
                    [f'- {error}'
                     for key, value in comment_form.errors.items()
                     for error in value]))
            messages.error(request,  error_msg)
            # comment_form이 valid하건 하지않건
            # 'post'네임스페이스를 가진 url의 post_list 이름에 해당하는 뷰에 이동
            
        return redirect('photo:list')