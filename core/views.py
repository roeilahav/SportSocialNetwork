from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Event, Feedback, Notification, Feedback2
from itertools import chain
import random
import math 
from .myUtils import getMatchingProfiles
from .nlpModule import getRating
# Create your views here.

@login_required(login_url='signin')
def index(request):
    
    user = request.user 


    my_profile = Profile.objects.get(user=user) 
    event = Event.objects.filter(is_active=True ,sport = my_profile.sport , lavel = my_profile.level ).order_by('-id')
    my_level = my_profile.level 
    my_sport = my_profile.sport 
    
    print(my_profile,my_level,my_sport)
    # ---------------------------------------------------------------------------------------
    similer_profile = Profile.objects.filter(sport=my_sport , level=my_level)
    print(similer_profile) 
    for x in similer_profile:
        print(x.user)
        print(x.level) 
        print(x.sport) 

    similar_profile_without_me = [profile for profile in similer_profile if (profile != my_profile)] 
    #sort user by rating 
    matchingProfiles = getMatchingProfiles(similar_profile_without_me,my_profile)

    print(similar_profile_without_me) 
    notifications = Notification.objects.filter(notification_of=user).order_by('-pk')

    context = {
        'my_profile': my_profile,
        'event': event,
        'similar_profile': matchingProfiles,
        'notifications': notifications
    }
    return render(request,'index.html',context) 

@login_required(login_url='signin')
def join_event_Y(request,id):
    event = Event.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    event.join_event(profile) 

    event.participant_left = event.participant_left + 1
    
    
    event.save()
    n = Notification()
    n.notification_of = event.user
    n.noti_text = f'{request.user} has joined your event {event.event_name}'
    n.who_contacted = request.user
    n.save()
    ev_profile = Profile.objects.get(user=event.user)
    ev_profile.number_of_new = ev_profile.number_of_new + 1
    ev_profile.save()

    return redirect('/')
@login_required(login_url='signin')
def view_event(request,id):
    event = Event.objects.get(id=id)
    participant_list = [player for player in event.participants.all()] 
    print(participant_list) 
    context = {
        'event':event,
        'participant_list':participant_list,
    }
    return render(request,'event_details.html',context)

def complete_event(request,id):
    
    event = Event.objects.get(id=id)  
    if event.user == request.user:
        for participant in event.participants.all():
            usr = participant.user
            n = Notification()
            n.notification_of = usr
            n.event_id = event.pk
            n.noti_text = f'Please Send your feedback regarding the event "{event.event_name}"'
            n.save()
            participant.number_of_new = participant.number_of_new + 1
            participant.save()
        event.is_active = False
        event.save()
    return redirect('/')

@login_required(login_url='signin')
def index2(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    # all_users = User.objects.all()
    all_users = Profile.objects.filter(sport=user_profile.sport,level=user_profile.level) 
    for x in all_users:
        print(x.level)
        print(x.user.username)
        print(x.sport) 

    # newUser = print(all_users)
    # print(newUser)

    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    print('---',new_suggestions_list)
    # current_user = User.objects.filter(username=request.user.username)
    current_user = request.user
    print('current user:', current_user)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x != current_user)]
    print('final suggestions:', final_suggestions_list)
    # random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users)

    # for ids in username_profile:
    #     profile_lists = Profile.objects.filter(id_user=ids)
    #     username_profile_list.append(profile_lists)

    # suggestions_username_profile_list = list(chain(*username_profile))

    print("Suggestions username ", username_profile)

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': username_profile[:4]})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list, 'notifications': Notification.objects.filter(notification_of=request.user).order_by('-pk')})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    event_list = Event.objects.filter(user=user_object).order_by('-pk')
    
    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    print('rating' , user_profile.rating , user_object.id)
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'event_list':event_list,
        'requesting_profile': Profile.objects.get(user=request.user),
        'rating': user_profile.rating
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            # newly added 
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            age = request.POST['age']
            # print(sport)
            sport = request.POST['sport']
            print(sport)
            gender = request.POST['gender']
            level = request.POST['level'] 
            phone = request.POST['phone'] 

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            # newly added 
            user_profile.user.first_name = first_name 
            print("-------------")
            print(user_profile.user.first_name)
            user_profile.user.last_name = last_name 
            user_profile.user.save()
            user_profile.age = age 
            user_profile.sport = sport 
            user_profile.gender = gender 
            user_profile.level = level 
            user_profile.phone = phone
            #getting the user preferences 
            lstPrefernces = []
            for i in range(1, 6):
                if request.POST.get('preference'+str(i)) != None:
                    lstPrefernces.append(request.POST.get('preference'+str(i)))
            user_profile.preferences = lstPrefernces

            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            # newly added 
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            age = request.POST['age']
            # print(sport) 
            sport = request.POST['sport']
            print(sport)
            gender = request.POST['gender']
            level = request.POST['level']
            phone = request.POST['phone']


            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            # newly added
            user_profile.user.first_name = first_name
            user_profile.user.last_name = last_name
            user_profile.age = age
            user_profile.sport = sport
            user_profile.gender = gender
            user_profile.level = level
            user_profile.phone = phone

            user_profile.save()
        
        return redirect('/')
    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def set_preferences(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        lstPrefernces = []
        
        for i in range(1, 7):
            if request.POST.get('preference'+str(i)) != None:
                tempLst = []
                tempLst.append(request.POST.get('preference'+str(i)))
                tempLst.append(request.POST.get('pweight'+str(i)))

                lstPrefernces.append(tempLst)


        user_profile.setPreferences(lstPrefernces)
        user_profile.save()
        print(user_profile.getPreferences())
       
        return redirect('/')
    return render(request, 'preferences.html', {'user_profile': user_profile})


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def event(request):
    if request.method == 'POST':
        user = request.user 
        event_name = request.POST.get('name')
        sport = request.POST.get('type')
        level = request.POST.get('level') 
        location = request.POST.get('location')
        no_of_participents = request.POST.get('total_player') 
        date = request.POST.get('date')
        time = request.POST.get('time') 
        image = request.FILES.get('image')

        # print(user,event_name,sport,location,level,no_of_participents,date,time,image) 
        event = Event(
            user = user,
            event_name = event_name,
            sport = sport,
            lavel = level,
            location = location,
            no_of_participents = no_of_participents,
            participant_left = 1 ,
            date = date,
            time = time,
            image = image,

        )
        event.save() 
        event.participants.add(Profile.objects.get(user=user))
        event.save()

        return redirect('/')

def feedback(request, id):
   
    if request.method == 'POST':
        a1 = request.POST.get('a1')
        a2 = request.POST.get('a2')
        a3 = request.POST.get('a3')
        a4 = request.POST.get('a4')
        a5 = request.POST.get('a5')
        msg = request.POST.get('msg')
        print("msg-value--------------------------------------------------------" , msg)
        print(a1,a2,a3,a4,a5)
        feedback = Feedback()
        
        feedback.a1 = a1
        feedback.a2 = a2
        feedback.a3 = a3
        feedback.a4 = a4
        feedback.a5 = a5
        feedback.msg = msg
        feedback.save() 
        
        #find user with id 
       
        #add feedback to user
        user = User.objects.get(pk=id)
        ratingValue = getRating([a1 , a2 , a3 , a4 , a5] , msg)
        #add +1 in rating of profile 
        profile = Profile.objects.get(user=user)
        print(profile.user.first_name , profile.rating)
        ratingValue = round(ratingValue)
        print("retunr value of getRating" , ratingValue)
        ratingValue = ratingValue * 5        
        new_rating = math.ceil(profile.rating + ratingValue)
        profile.rating = math.ceil(new_rating/2)
        print(profile.user.first_name , profile.rating)
        profile.save()

        # try:
        #     event = Event.objects.get(pk=event_id)
        #     event.feedbacks.add(feedback)
        # except:
        #     event = Event.objects.all()[0]
        #     event.feedbacks.add(feedback)
    
        return redirect('/')
        
        
    return render(request,'feedback.html',{'id':id})


def feedback2(request, notification_id , noti = None):
    if request.method == 'POST':
        a1 = request.POST.get('a1')
        
        print(request.body)
        

        if a1 == 'Yes':
            # feedback = Feedback2()
            # feedback.a1 = a1
            # feedback.save() 
            n = Notification.objects.get(pk=notification_id)
            
            n.delete()
            return redirect(f'/feedback/{n.who_contacted.id}')
        else:
            pass
    
        return redirect('/')
        
    n = Notification.objects.get(pk=notification_id)

    return render(request,'feedback2.html',{'noti':n , 'notification_id': notification_id})


from django.http import JsonResponse

def my_view(request, by, to):
    user_to = User.objects.get(pk=to)
    user_by = User.objects.get(pk=by)

    n = Notification()
    n.notification_of = user_to
    n.noti_text = f"{user_by} contacted you, have you trained together?"
    n.who_contacted = user_by
    n.save()

    participant = Profile.objects.get(user=user_to)
    participant.number_of_new = participant.number_of_new + 1
    participant.save()


    n = Notification()
    n.notification_of = user_by
    n.noti_text = f"You have contaced {user_to}, have you trained together?"
    n.who_contacted = user_to
    n.save()

    participant = Profile.objects.get(user=user_by)
    participant.number_of_new = participant.number_of_new + 1
    participant.save()

    data = {'name': 'John', 'age': 30}
    return JsonResponse(data)


def clear_notifications(request, of_whom):
    of_whom = User.objects.get(pk=of_whom)

    

    participant = Profile.objects.get(user=of_whom)
    participant.number_of_new = 0
    participant.save()
    data = {'name': 'John', 'age': 30}
    return JsonResponse(data)
