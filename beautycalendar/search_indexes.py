from haystack import indexes
from beautycalendar.models import Users,BeautySalons,ContentUsers,WorkItems

'''
class NoticiaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    fecha = indexes.DateTimeField(model_attr='fecha')

    def get_model(self):
        return Noticia

    def index_queryset(self, using=None):
        """Queremos que se indexen todas las noticias que tengan archivada=False"""
        return self.get_model().objects.filter(archivada=False)
'''

# class workItems(indexes.SearchIndex, indexes.Indexable):
#     text= indexes.CharField(document=True, use_template=True)
#     content_auto= indexes.EdgeNgramField(model_attr='item')
#     def get_model(self):
#         return WorkItems
    

class beautySalonsIndex(indexes.SearchIndex, indexes.Indexable):
    #Lo que quiero que me devuelva
    text= indexes.CharField(document=True, use_template=True)
    title=indexes.CharField(model_attr='items')
    owner=indexes.CharField(model_attr='owner')
    content_auto= indexes.EdgeNgramField(model_attr='items')
    salon_name= indexes.CharField()
    full_name=indexes.CharField()
    
    def get_model(self):
        return BeautySalons
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_salon_name(self, obj):
        return obj.owner.name_salon
    
    def prepare_full_name(self,obj):
        #full= obj.owner.first_name + obj.owner.last_name
        return obj.owner.get_full_name()
    
class UsersIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    email= indexes.CharField(model_attr='email')
    title= indexes.CharField(model_attr='get_full_name')
    last_name = indexes.CharField(model_attr='last_name')
    kind= indexes.IntegerField(model_attr='kind',null=True)
    name_salon= indexes.CharField(model_attr='name_salon', null=True)    
    
    content_auto = indexes.EdgeNgramField(model_attr='get_full_name')
    
#    content_auto= indexes.EdgeNgramField(model_attr='email')
#    content_auto= indexes.EdgeNgramField(model_attr='last_name')
#    content_auto=indexes.EdgeNgramField(model_attr='name_salon',null=True)
    
    def get_model(self):
        return Users

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(state=1).exclude(kind=3)


class ContentsIndex(indexes.SearchIndex,indexes.Indexable):
    text=indexes.CharField(document=True,use_template=True)
    title=indexes.CharField(model_attr='title')
    price=indexes.CharField(model_attr='price',null=True)
    user=indexes.CharField(model_attr='user')
    category=indexes.CharField(model_attr='category')
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return ContentUsers

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(state=1)