from django.core.checks import Tags
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from blogApp.models import Post, Comment
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from blogApp.forms import EmailSendForm, CommentForm


# Create your views here.
class PostListView(ListView):
    model = Post
    paginate_by = 1


def post_list_view(request, tag_slug=None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)  # get tag object by using tag slug
        post_list = post_list.filter(tags__in=[tag])  # filter posts using tag object
    paginator = Paginator(post_list, 1)  # paginate the list page with 2 poste per page
    page_number = request.GET.get('page')  # get page number
    try:
        post_list = paginator.page(page_number)  # page list for given page number
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blogApp/post_list.html', {'post_list': post_list, 'tag': tag})


def post_detail_view(request, state, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status=state, publish__year=year, publish__month=month,
                             publish__day=day, )
    comments = post.comments.filter(active=True)
    csubmit = False
    form = CommentForm()
    if request.method == "POST":
        form1 = CommentForm(request.POST)
        if form1.is_valid():
            new_comment = form1.save(commit=False)
            new_comment.post = post  # adding post details to comment
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()

    return render(request, 'blogApp/post_detail.html',
                  {'post': post, 'form': form, 'csubmit': csubmit, 'comments': comments})


def mail_send_view(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you to read "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read post at: "{}" \n \n{}\'s comments: \n{}'.format(post_url, cd['name'], cd['comments'])
            email = cd['email']
            print(post_url)
            # send_mail(subject, message, email, [cd['to']])
            print('inside email block')
            sent = True
    else:
        form = EmailSendForm()
    return render(request, 'blogApp/sharebyemail.html', {'form': form, 'post': post, 'sent': sent})
