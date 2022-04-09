#Class-based todo list

This app uses Django's class-based views to implement a simple todo list.

I found the code looks cleaner and is generally shorter using class-based views (rather than function based views) but I had difficulty understanding how to implement even custom code/logic. For example in the UpdateView, I wanted to prevent anyone except the author of the task to see the page, so my thought was to compare the current user to the author and redirect to the main task list page if they were different. Something like: 
```python
task = self.get_object()
if self.request.user == task.user:
    redirect('home')
```

However, I can't see how to get the task itself. There are several class methods that can be overridden, but I am having difficulty figuring out which one to override to impliment the functionality I want. I also don't understand how to write custom methods for the classes and get them to run when the url uri is called. As far as I can tell the get_object() method returns the object (task) but how do I implement a custom method so I can use that? The closest solutions I have found so far use two methods provided by Django. One uses the UserPassesTestMixin and the test_func method:
```python
def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False
```
The issue with this is that it sends the user to a 403 forbidden page, and I don't know how to override that to redirect to where I want it to go. The other way is to overide the get_queryset method to only retreive objects where the user is the author (solution from: https://www.django-antipatterns.com/antipattern/checking-ownership-through-the-userpassestestmixin.html)
```python
def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )
```
This returns a 404 page, which I think is better so I decided to use this for now. 

OK so further reading shows me that implementing custom methods/logic in CBVs is indeed the crux of the problem with CBVs in general. Apparantly, you need to know when each of the built-in mthods of the ViewClasses are called, and call your custom class in that method (solution: https://stackoverflow.com/questions/35406930/create-custom-methods-in-django-class-base-views), also early discussion on issues with CBVs https://lukeplant.me.uk/blog/posts/djangos-cbvs-were-a-mistake/. 

Laravel is starting to look very appealing :)