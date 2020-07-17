from django.views.generic import TemplateView
from home.forms import HomeForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from home.models import Post, Friend, Comment
from django.contrib.auth.models import User
from django.views import generic
import random
from django.core.paginator import Paginator
from django.db.models import Q

class HomeView(TemplateView):
    template_name = 'home/home.html'




    def get(self, request):



        # try:
        #     friend = Friend.objects.get(current_user=request.user)
        #     friends = friend.users.all()
        # except:
        #     friends = None

        form = HomeForm()

        users = User.objects.exclude(id=request.user.id)


        try:
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()

        #Khai báo đối tượng Friend có thuộc tính current_user = request.user
        # Lúc này current User taats đang khóa ngoại với User
        except Friend.DoesNotExist:
            friends = None

        # c = Comment.objects.count(post = )
        # user_post = [users, friends]
        posts = Post.objects.filter(Q(user__id__in=[request.user.id])|Q(user__id__in=[request.user.id]))
        # posts = Post.objects.all()
        print(request.user.id)
        pageSize = 5
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))

        #Lấy ra tất cả bản ghi của đối tượng friend
        context = {'form': form, 'posts': posts, 'users': users, 'friends': friends}
        return render(request, self.template_name, context)


    def post(self, request):


        form = HomeForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            text = form.cleaned_data['post']
            form = HomeForm() #Đặt lại form về trạng thái ban đầu
            return redirect('home')


        context = {'form': form, 'text': text}
        return render(request, self.template_name, context)


def change_friend(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, new_friend)
    return redirect(request.META.get('HTTP_REFERER'))

# class PostDetail(generic.DeleteView):
#     model = Post
#     template_name = 'home/detail_post.html'
#     #tạo 1 class để hiển thị chỉ mình bài viết đó giống facebook
#     # tạo 1 class PostDetail kế thừa từ generic truyền vào 1 model là post
#     #template là 'detail_post.html'
#     #path('<int:pk>/', views.PostDetail.as_view(), name = 'detail_post')
#     #<a href="{% url 'detail_post' post.id %}">More</a>

def post_detail(request, id):
    post = Post.objects.get(id=id)
    form_comment = CommentForm()
    if request.method == 'POST':
        form_comment = CommentForm(request.POST, author=request.user, post = post)
        if form_comment.is_valid():
            form_comment.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'home/detail_post.html', {'post': post, 'form_comment':form_comment})
    #Khi click vào #<a href="{% url 'detail_post' post.id %}">More</a>
    #Thì post.id sẽ nhảy vào tham id trong hàm
