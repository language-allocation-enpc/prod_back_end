import random as rd


class course():
    def __init__(self, id=-1, name='', language='', creneaux =[], min_students=0, max_students=0):
        self.min_students = min_students
        self.max_students = max_students
        self.id = id
        self.language = language
        self.name = name
        self.creneaux = creneaux
    def __eq__(self, other):
        return self.id == other.id
    def to_dict(self):
        dic = {}
        dic['id'] = self.id
        dic['min_students'] = self.min_students
        dic['language'] = self.language
        dic['creneaux'] = self.creneaux
        dic['name'] = self.name
        dic['max_students'] = self.max_students
        return dic
    def from_dict(self, dic):
        self.id = dic['id']
        self.min_students = dic['min_students']
        self.language = dic['language']
        self.creneaux = dic['creneaux']
        self.name = dic['name']
        self.max_students = dic['max_students']


class vow():
    def __init__(self):
        self.courses = []
        self.weight = 1
    def __eq__(self, other):
        if len(self.courses) == len(other.courses):
            other_courses_ids = [c.id for c in other.courses]
            for i_course in range(len(self.courses)):
                if self.courses[i_course].id in other_courses_ids:
                    return False
            return True
        return False
    def __hash__(self):
        return hash(c.id for c in self.courses)
    def to_dict(self):
        dic={}
        dic["courses"] = self.courses
        dic["weight"] = self.weight
        return dic
    def from_dict(self, dic):
        for course_in_dic in dic["list"]:
            current_course = course()
            current_course.from_dict(course_in_dic)
            self.courses.append(current_course)
        self.weight = dic["weight"]



class student():
    def __init__(self, id = 0):
        self.id = id
        self.name = ''
        self.vows = []
        self.courses = []
