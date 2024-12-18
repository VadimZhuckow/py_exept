import logging
from dataclasses import dataclass, field


logging.basicConfig(
    filename='app.log',  
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class SchoolException(Exception):
    @property
    def message(self):
        return 'в приложении ошибка'

@dataclass
class AgeException(SchoolException):
    age: int

    @property
    def message(self):
        return f'нельзя вкатится в школу в возрасте {self.age}! Можно если больше 7 лет'

class InSchoolException(SchoolException):
    @property
    def message(self):
        return 'Нельзя вкатится в школу если чел уже учится в школе'

@dataclass
class Student:
    name: str
    age: int
    is_in_school: bool = field(default=False)

@dataclass
class School:
    name: str
    students: list[Student] = field(default_factory=list)

    def validate_student(self, student: Student) -> None:
        if student.age < 7:
            logging.error(AgeException(student.age).message)
            raise AgeException(student.age)
        elif student.is_in_school:
            logging.error(InSchoolException().message)
            raise InSchoolException()

    def add_school(self, student: Student) -> None:
        self.validate_student(student)
        student.is_in_school = True
        self.students.append(student)
    
    def expel_school(self, student: Student) -> None:
        if student in self.students:
            student.is_in_school = False
            self.students.remove(student)
        else:
            logging.error(f'Попытка исключить студента {student.name}, который не учится в школе {self.name}.')

def main():
    vasek = Student('vasek', 9)
    petya = Student('pet', 1)
    school = School('1')
    school2 = School('2')

    try:
        school.add_school(vasek)
        print(f"Добавлен студент: {vasek}")
        print(f"Студенты в школе {school.name}: {school.students}")
        
        # Попытка добавить ученика с недопустимым возрастом
        school.add_school(petya)
    except SchoolException as error:
        print(error.message)

    try:
        # Попытка добавить ученика, который уже учится в другой школе
        school2.add_school(vasek)
    except SchoolException as error:
        print(error.message)

    # Исключаем студента из школы
    try:
        school.expel_school(vasek)
        print(f"Исключен студент: {vasek}")
        print(f"Студенты в школе {school.name}: {school.students}")
    except Exception as e:
        logging.error(f'Ошибка при исключении студента: {str(e)}')

if __name__ == '__main__':
    main()
