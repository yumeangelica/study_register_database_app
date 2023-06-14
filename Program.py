from Database import Database

class Program:
    def __init__(self):
        self.database = Database() #create database object
        self.run() #run the program

    #add completion to the database
    def add_completion(self):
        course_name = None 
        grade = None
        study_points = None

        while course_name is None: #loop until course name is not None
            try:
                course_name = input('give course name: ').lower()
            except:
                print('Give valid input')

        while grade is None: #loop until grade is not None 
            try: #try to convert the input to an integer
                grade = int(input('give grade (0 - 5): '))
                if grade < 0 or grade > 5: #if the grade is not between 0 and 5
                    grade = None
            except ValueError: #if the input is not an integer
                print('Give valid input (0 - 5)')
        
        while study_points is None: #loop until study points is not None
            try: #try to convert the input to an integer
                study_points = int(input('give study points: '))
                if study_points < 0 or study_points > 30: #if the study points is not between 0 and 30
                    study_points = None
            except ValueError: #if the input is not an integer
                print('Give valid input (0 - 30)')
        
        

        if course_name != None and grade != None and study_points != None: #if all the values are not None
            
            result = self.database.add_completion(course_name, grade, study_points) #add completion to the database
            
            return print(f'{course_name} added') if result else print('Completion already exists') #print if the completion was added or not


    def get_completion(self):
        course_name = input('give course name: ').lower() #ask for course name

        try:
            completion = self.database.get_completion(course_name) #get completion from the database
            course_name, grade, study_points = completion #unpack the completion
        
        except:
            return print('Completion does not exist')


        return print(f'{course_name.capitalize() + ":" : <10}  ({study_points}) ects, grade: {grade}\n') if completion != None else print('Completion does not exist') #print the completion if it exists, else print 'completion does not exist'

    def get_all_completions(self):
        completion_data = self.database.get_all_completions() #get all completions from the database

        if len(completion_data) == 0: #if there are no completions
            return print('No completions yet')

        for (course_name, grade, study_points) in completion_data: #loop through the completions
            print(f'{course_name.capitalize() + ":" : <15}  ({study_points}) ects, grade ({grade})') #print the completion. The <10 makes the course name have 10 characters, and the rest is filled with spaces

        print()

    def update_course(self):
        
        course_name_list = [name[0] for name in self.database.get_all_coursenames()] #get all course names from the database

        if len(course_name_list) == 0: #if there are no completions
            return print('No completions yet')
        

        print('Course names: ') #prints all the course names that exist
        for name in course_name_list:
            print(name) #print all the course names
        
        course_name = input('give course name: ').lower() #ask for course name


        if course_name not in course_name_list: #if the course name does not exist
            return print('You inputted invalid course name')
        
        new_course_name = input('Input new course name if you want to update it, leave blank if not: ').lower() #ask if the user wants to update course name
        
        new_grade = input('Input new grade if you want to update it, leave blank if not: ') #ask if the user wants to update grade
        try:
            new_grade = int(new_grade) if new_grade != '' else None #if the user wants to update grade, convert the input to int
        except ValueError:
            print('You inputted invalid grade, grade kept as it was')
            new_grade = None


        new_study_points = input('Input new study points if you want to update it, leave blank if not: ') #ask if the user wants to update study points
        try:
            new_study_points = int(new_study_points) if new_study_points != '' else None #if the user wants to update study points, convert the input to int
        except ValueError:
            print('You inputted invalid study points, study points kept as it was')
            new_study_points = None

        result = self.database.update_course(course_name, new_course_name, new_grade, new_study_points) #update the completion in the database

        return print(f'{course_name} updated') if result else print('Error in updating completion')

    def delete_completion(self):

        course_name_list = [name[0] for name in self.database.get_all_coursenames()] #get all course names from the database

        if len(course_name_list) == 0: #if there are no completions
            return print('No completions yet')
        

        print('Course names: ') #prints all the course names that exist
        for name in course_name_list:
            print(name) #print all the course names
        
        print()

        course_name = input('give course name to delete: ').lower()
        result = self.database.delete_completion(course_name) #delete completion from the database
        return print(f'{course_name} deleted') if result else print('Completion does not exist')

    def print_statistics(self):

        #for grade distribution
        grade_statistics = self.database.get_all_grades_and_count() #fetch all completions from the database and return them as a list of tuples [(grade, count of grade) ...]

        if len(grade_statistics) == 0: #if there are no completions
            return print('No completions yet')

        grade_distribution = { #create a dictionary for the grade distribution
            5: '',
            4: '',
            3: '',
            2: '',
            1: '',
            0: ''
        }


        for grade, count in grade_statistics: #loop through the list of tuples
            grade_distribution[grade] = f'{count * "x"}' #add the count to the dictionary

        print('Grade distribution: ')
        
        for key, val in grade_distribution.items():
            print(f'{key}: {val}')


        print()

        #for average grade
        average_grade = self.database.get_average_grade() #get the average grade from the database
        print(f'Average grade: {round(average_grade, 2)}')


        #for weighted average grade
        grade_x_point_sum, pointsum = self.database.get_weighted_average_grade_details() #get the weighted average grade from the database
        weighted_average_grade = grade_x_point_sum / pointsum

        print(f'Weighted average grade: {round(weighted_average_grade, 2)}')

        print()


    #this function clears the terminal
    def clearTerminal(self):
        from os import system, name
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
        

    def guide(self):

        print()
        print('[0] - quit')
        print('[1] - add completion')
        print('[2] - update course')
        print('[3] - get completion')
        print('[4] - get all completions')
        print('[5] - delete completion')
        print('[6] - print statistics')
        print()

    def run(self): #this is the main program

            while True:
                self.clearTerminal() #clears the terminal
                self.guide() #prints the guide
                
                try: #creating try and except block for the user input to prevent errors when inputting wrong values (like letters)
                    command = int(input('command: ')) #asks for command
                    print()

                    if command == 0: #0 breaks the loop
                        break
                    elif command == 1: #1 adds a completion
                        self.add_completion()
                    elif command == 2: #2 updates a completion
                        self.update_course()
                    elif command == 3: #3 gets a completion
                        self.get_completion()
                    elif command == 4: #4 gets all completions
                        self.get_all_completions()
                    elif command == 5: #5 deletes a completion
                        self.delete_completion()
                    elif command == 6: #6 prints the statistics
                        self.print_statistics()
                    else:
                        print('Give valid command')

                except ValueError: #if input is not number, prints 'give valid input'
                    print('Give valid input')
                
                input('Press enter to continue...') #waits for user input to continue