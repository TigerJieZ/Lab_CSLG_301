from django.contrib import admin,sessions
import lab.models as models
# Register your models here.

admin.site.register(models.Article)
admin.site.register(models.Member)
admin.site.register(models.BlogComment)
admin.site.register(models.Category)
admin.site.register(models.Group)
admin.site.register(models.Suggest)
admin.site.register(models.Tag)
admin.site.register(models.New)
admin.site.register(models.News_image)
admin.site.register(models.Achievement)
admin.site.register(models.Achievement_image)
