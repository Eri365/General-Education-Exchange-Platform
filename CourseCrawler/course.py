from dataclasses import dataclass, field
from typing import Optional

@dataclass(order=True)
class Course:
    # 第 4、10、11、12 項為 int
    domain: str
    academic_cluster: str
    id: str
    name: str
    credits: int
    time: str
    week_of_classes: str
    classroom: str
    instructor: str
    course_department: str
    capacity: int
    enrolled_students: int
    available_seats: int
    language: str
    remarks: str = None
    
    def __str__(self):
        return ','.join([str(value) for value in self.__dict__.values()])
    
    def __repr__(self):
        return ','.join([str(value) for value in self.__dict__.values()])
        