from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from beautycalendar.models import Users, ContentUsers, Empleoyees, WorkItems, BeautySalons, WorkingHoursSalons, UserDates, Publications,Reports, LikesPublications,CommentsPublications, Draws,DrawsList

#admin.site.register(ContentUsers)
#admin.site.register(Empleoyees)
admin.site.register(WorkItems)

#admin.site.register(Users)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = Users
        fields = ('email', 'first_name','last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Users
        fields = ('email', 'password', 'first_name', 'last_name', 'state', 'kind','description', 'imageAvatar','imageFront','score')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name','state','kind','name_salon','is_admin')
    list_filter = ('is_admin','state','kind')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','description','name_salon')}),
        ('State', {'fields': ('state',)}),
        ('Kind',{'fields':('kind',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Images',{'fields':('imageAvatar','imageFront')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
           'fields': ('email', 'password1', 'password2')}
       ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class AdminSalons(admin.ModelAdmin):
    list_display=('owner','items')

class AdminContent(admin.ModelAdmin):
    list_display=('user','category','title','price','state','attention_time')

    list_filter = ('user','category','state')

class AdminEmpleoyees(admin.ModelAdmin):
    list_display=('boss','first_name','last_name','state')
    list_filter = ('boss','state')

class AdminWorkingHours(admin.ModelAdmin):
   list_display=('salon','init_date','finish_date','init_time','finish_time')


class AdminUserDater(admin.ModelAdmin):
    list_display=('client','date','service','empleoyee','state','salon','init_time','finish_time')

class AdminPublications(admin.ModelAdmin):
    list_display=('owner','publish_date','description','score','state')
   
class AdminReports(admin.ModelAdmin):
    list_display=('informer','informed','options','other')

class AdminLikes(admin.ModelAdmin):
    list_display=('user','publication','value')

class AdminDraws(admin.ModelAdmin):
    list_display=('name','owner','finish_day','state')

class AdminListDraws(admin.ModelAdmin):
    list_display=('draw','client')
    list_filter=('draw',)

# Now register the new UserAdmin...
admin.site.register(Users, UserAdmin)
admin.site.register(BeautySalons,AdminSalons)
admin.site.register(ContentUsers,AdminContent)
admin.site.register(Empleoyees,AdminEmpleoyees)
admin.site.register(WorkingHoursSalons,AdminWorkingHours)
admin.site.register(UserDates, AdminUserDater)
admin.site.register(Publications,AdminPublications)
admin.site.register(Reports, AdminReports)
admin.site.register(LikesPublications,AdminLikes)
admin.site.register(Draws,AdminDraws)
admin.site.register(DrawsList,AdminListDraws)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)