from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class PublicOrUsersOwnMixin(LoginRequiredMixin):
    '''Intended as a mixin to DetailView classes, 
    this allows a user to view a page under any of the following conditions:
      1. The object "belongs" to the user
      2. The object is marked public (ignored if public_field_name is None)
      3. The user is a superuser (can be turned off)
    In any other case, the user sees a 404 page.
    '''
    user_field_name = 'user'
    public_field_name = None
    allow_superuser = True

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.allow_superuser and user.is_superuser:
            return queryset
        filt = {self.user_field_name: user}
        q = Q(**filt)
        if self.public_field_name is not None:
            filt = {self.public_field_name : True}
            q = q | Q(**filt)
        return queryset.filter(q)
