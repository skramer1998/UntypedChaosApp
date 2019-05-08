from django.db import models
from FSA.accountmodel.account import Account


class Lab(models.Model):
    parentSection = models.CharField(max_length=60)
    number = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    ta = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    """
    create lab to be added to a section
    needs parent course name, parent section number, lab number and ta(can be null) 
    """
    @classmethod
    def create(cls, parentCourse, parentSection, labNumber, ta):
        try:
            lab = Lab.search(parentCourse, parentSection, labNumber)
            if lab is False:
                foundTA = Account.get(ta)
                lab = cls(parentSection=parentCourse, number=labNumber, ta=foundTA)
                lab.save()
                section = Section.get(parentCourse, parentSection)
                section.labs.add(lab)
                section.save()
                course = Course.get(parentCourse)
                course.save()
                return True
            return False
        except Exception as e:
            print(e)
            return False

    @classmethod
    def changeta(cls, parentCourse, sectionNum, labNum, newTA):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.ta = newTA
            lab.save()
            return True
        return False

    @classmethod
    def changenumber(cls, parentCourse, sectionNum, labNum, newNum):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.number = newNum
            lab.save()
            return True
        return False

    @classmethod
    def changeplace(cls, parentCourse, sectionNum, labNum, newPlace):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.place = newPlace
            lab.save()
            return True
        return False

    @classmethod
    def changedays(cls, parentCourse, sectionNum, labNum, newDays):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.days = newDays
            lab.save()
            return True
        return False

    @classmethod
    def changetime(cls, parentCourse, sectionNum, labNum, newTime):
        lab = Lab.get(parentCourse, sectionNum, labNum)
        if lab is not None:
            lab.time = newTime
            lab.save()
            return True
        return False

    """
    returns the lab of a section given course name and section number and lab number
    """
    @classmethod
    def get(cls, currentCourse, currentSection, currentLab):
        try:
            section = Section.get(currentCourse, currentSection)
            return section.labs.all().filter(number=currentLab).first()
        except:
            return None

    """
    looks for lab in a section
    takes name of course and section number, and lab number
    returns true if lab exist, else otherwise
    """
    @classmethod
    def search(self, currentCourse, currentSection, newLab):
        check = Lab.get(currentCourse, currentSection, newLab)
        if check is not None:
            return True
        else:
            return False

    def __str__(self):
        return str(self.parentSection) + " Lab: " + str(self.number) + " TA: " + str(self.ta)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(Course, self).save(*args, **kwargs)
        except:
            print("Error saving model")

class Section(models.Model):
    parentCourse = models.CharField(max_length=60)
    number = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    days = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    instructor = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    labs = models.ManyToManyField(Lab, blank=True)

    """
    Create a section for a course
    """

    @classmethod
    def create(cls, parentCourse, number, instructor):
        try:
            # check if section exist
            section = Section.search(parentCourse, number)
            if section is False:
                # section does not exist so create course
                # get instructor (can be null)
                foundInstructor = Account.get(instructor)
                # create section object
                section = cls(parentCourse=parentCourse, number=number, instructor=foundInstructor)
                # save section object in database
                section.save()
                # get course
                course = Course.get(parentCourse)
                # add section to course
                course.sections.add(section)
                # save course to database
                course.save()
                return True
            # if section exist, return False
            return False
        except Exception as e:
            # helps with figuring out the error
            print(e)
            return e

    @classmethod
    def changein(cls, parentCourse, sectionNum, newProf):
        section = Section.get(parentCourse, sectionNum)
        if section is not None:
            section.instructor = newProf
            section.save()
            return True
        return False

    @classmethod
    def changeplace(cls, currentCourse, currentSectionNum, newPlace):
        section = Section.get(currentCourse, currentSectionNum)
        if section is not None:
            section.place = newPlace
            section.save()
            return True
        return False

    @classmethod
    def changedays(cls, currentCourse, currentSectionNum, newDays):
        section = Section.get(currentCourse, currentSectionNum)
        if section is not None:
            section.days = newDays
            section.save()
            return True
        return False

    @classmethod
    def changetime(cls, currentCourse, currentSectionNum, newTime):
        section = Section.get(currentCourse, currentSectionNum)
        if section is not None:
            section.time = newTime
            section.save()
            return True
        return False

    """
    creates a lab and adds it to the current section
    takes the course name, section number of course, new lab number and lab TA(can be null)
    """

    @classmethod
    def addlab(cls, currentCourse, currentSection, labNum, labTA):
        return Lab.create(currentCourse, currentSection, labNum, labTA)

    """
    returns the section of a course given course name and section number of the course
    """

    @classmethod
    def get(cls, nameofCourse, numofSection):
        try:
            course = Course.get(nameofCourse)
            return course.sections.all().filter(number=numofSection).first()
        except:
            return None

    """
    looks for section in a course
    takes name of course and section number in course
    returns true if section exist, else otherwise
    """

    @classmethod
    def search(cls, currentCourse, newNum):
        check = Section.get(currentCourse, newNum)
        if check is not None:
            return True
        else:
            return False

    def __str__(self):
        return str(self.parentCourse) + ": " + str(self.number) + " Instructor: " + str(self.instructor)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(Course, self).save(*args, **kwargs)
        except:
            print("Error saving model")


class Course(models.Model):
    """
    Courses Class: The class used to store course objects / edit / create them
    """

    name = models.CharField(max_length=30)
    number = models.IntegerField(default=0)
    semester = models.CharField(max_length=30)
    sections = models.ManyToManyField(Section, blank=True)

    """
    Create a Course
    """

    @classmethod
    def create(cls, name, number, semester):
        has_course = Course()
        has_course = has_course.search(name)
        if has_course:
            return "That course already exists."
        else:
            course = cls(name=name, number=number, semester=semester)
            course.save()
            return course

    @classmethod
    def changename(cls, currentCourse, newName):
        course = Course.get(currentCourse)
        if course is not None:
            course.name = newName
            course.save()
            return True
        return False

    @classmethod
    def changenumber(cls, currentCourse, newNum):
        course = Course.get(currentCourse)
        if course is not None:
            course.number = newNum
            course.save()
            return True
        return False

    @classmethod
    def changesemester(cls, currentCourse, newSemester):
        course = Course.get(currentCourse)
        if course is not None:
            course.name = newSemester
            course.save()
            return True
        return False

    """
    Give the course name, section number, and the instructor(can be null)
    """

    @classmethod
    def addsection(cls, currentCourse, sectionNum, sectionInstructor):
        return Section.create(currentCourse, sectionNum, sectionInstructor)

    """
        Give the course name, returns true if there is one in the database, returns false otherwise
    """

    @classmethod
    def search(cls, name):
        try:
            check = Course.get(name)
        except Course.DoesNotExist:
            check = None

        if check is not None:
            return True
        else:
            return False

    """
            Give the course name, returns the course, otherwise returns None
    """

    @classmethod
    def get(cls, nameofCourse):
        try:
            course = Course.objects.all().filter(name=nameofCourse).first()
            return course
        except:
            return None

    # call Course.objects.all() to get all courses to string
    def __str__(self):
        return str(self.name) + " " + str(self.number) + " " + str(self.semester)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super(Course, self).save(*args, **kwargs)
        except:
            print("Error saving model")