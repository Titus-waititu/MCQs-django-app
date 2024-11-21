
from django.db import models
import uuid
import random


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    pass1 = models.CharField(max_length=500)
    pass2 = models.CharField(max_length=500)

    def __str__(self):
        return self.username
    

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    
    
    class Meta:
        abstract = True
        
class Types(BaseModel):
    gfg_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.gfg_name
    
    
    
class Question(BaseModel):
    gfg = models.ForeignKey(Types, related_name='gfg',on_delete= models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default = 5)
    
    def __str__(self) -> str:
        return self.question
    
    def get_answers(self):
        answer_objs =  list(Answer.objects.filter(question= self))
        data = []
        random.shuffle(answer_objs)
        
        for  answer_obj in answer_objs:
            data.append({
                'answer' :answer_obj.answer, 
                'is_correct' : answer_obj.is_correct
            })
        return data
    
class Answer(BaseModel):
    question = models.ForeignKey(Question,related_name='question_answer',  on_delete =models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.answer