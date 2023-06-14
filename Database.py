from sqlite3 import connect

class Database:
    def __init__(self):
        self.database_name = 'db.sqlite' #database name
        self.conn = connect(self.database_name, isolation_level=None) #connect to the database
        self.cursor = self.conn.cursor() #create cursor
        self.unique_id = self.id_generator() #create unique id generator
        self.init_database()

    #Initialize the database if there is no table Course in database
    def init_database(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Course (id INTEGER PRIMARY KEY UNIQUE, course_name TEXT, grade INTEGER, study_points INTEGER)')
        self.conn.commit()
         
    #generates unique id with timestamp
    def id_generator(self):
        last_id = self.cursor.execute('SELECT MAX(id) FROM Course').fetchone()[0] #get the last id from the database
        _id = last_id + 1 #set the id to the number of ids
        while True:
            yield _id
            _id += 1

    #add completion to the database
    def add_completion(self, course_name, grade, study_points):
        
        result = self.cursor.execute('SELECT course_name FROM Course WHERE course_name = ?', [course_name]).fetchone() #checking if course exists

        if result != None or result is not None: #if course exist
            return False
        
        try:
            self.cursor.execute('INSERT INTO Course (id, course_name, grade, study_points) VALUES (?, ?, ?, ?)', [next(self.unique_id), course_name, grade, study_points]) #add completion to the database
            self.conn.commit()
            return True
        except:
            return False


    #updating course
    def update_course(self, course_name, new_course_name=None, new_grade=None, new_study_points=None):

        course_details = self.cursor.execute('SELECT id, grade, study_points FROM Course WHERE course_name = ?', [course_name]).fetchone() #checking if course exists
        id, grade, study_points = course_details #unpacking the course details
        
        if len(course_details) == 0 or course_details == None: #if course does not exist
            return print('Course does not exist')

        try: #try to update the course
            self.cursor.execute(''' UPDATE Course 
                                    SET course_name = ?, 
                                    grade = ?, 
                                    study_points = ? 
                                    WHERE id = ?
                                ''', 
                                [
                                new_course_name if new_course_name else course_name, 
                                new_grade := int(new_grade) if new_grade else grade, 
                                new_study_points := int(new_study_points) if new_study_points else study_points, 
                                id
                                ])
            self.conn.commit()
            return True #return True if course was updated
        except: #if course was not updated
            return False
    
    
    

    #fetches all course names from the database
    def get_all_coursenames(self):
        return self.cursor.execute('SELECT course_name FROM Course').fetchall()


    #get completion from the database by course name
    def get_completion(self, course_name):
        return self.cursor.execute('SELECT course_name, grade, study_points FROM Course WHERE course_name = ?', [course_name]).fetchone()

    #get all completions from the database
    def get_all_completions(self):
        return self.cursor.execute('SELECT course_name, grade, study_points FROM Course').fetchall() #fetch all completions from the database and return them

    #delete completion from the database by course name
    def delete_completion(self, course_name):
        course = self.get_completion(course_name) #checking if course exists


        if course != None: #if course exists
            try: #try to delete the course
                self.cursor.execute('DELETE FROM Course WHERE course_name = ?', [course_name]) #delete course from the database by course name
                self.conn.commit()
                return True #return True if course was deleted
            except: #if course was not deleted
                return False
        

    #For statistics
    #get all grades and grade count from the database
    def get_all_grades_and_count(self): 
        return self.cursor.execute('SELECT grade, COUNT(grade) FROM Course GROUP BY grade').fetchall()


    #get average grade from the database
    def get_average_grade(self):
        return self.cursor.execute('SELECT AVG(grade) FROM Course').fetchone()[0]

    # get weighted average grade from the database
    def get_weighted_average_grade_details(self):
        return self.cursor.execute('SELECT SUM(grade * study_points), SUM(study_points) FROM Course').fetchall()[0]

