from django.db import models

class DeclareResult(models.Model):
    # Define fields for your model
    student_name = models.CharField(max_length=100)
    student_roll = models.IntegerField()
    # Add more fields as needed

    def __str__(self):
        return self.student_name  # Return a meaningful representation of the model instance
