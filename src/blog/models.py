from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
def upload_to(instance,filename):
    return '%s/%s/%s'%('posts',instance.name,filename)

class Post(models.Model):
    name = models.CharField(max_length=191)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to = upload_to,default='',null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return "%s posted by %s" % (self.name, self.author.username)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'
        ordering = ['-created_at']

    def unique_slug(self, new_slug, original_slug, index):
        if Post.objects.filter(slug=new_slug):
            new_slug = '%s-%s' % (original_slug, index)
            index += 1
            return self.unique_slug(new_slug=new_slug, original_slug=original_slug, index=index)
        return new_slug

    def save(self, *args, **kwargs):
        index = 1
        new_slug = slugify(self.name)
        self.slug = self.unique_slug(new_slug=new_slug, original_slug=new_slug, index=index)
        return super(Post, self).save(*args, **kwargs)

    def snipped_body(self):
        return self.body[:150] + "..."

    def total_likes(self):
        return self.likes.count()
