#CW2
# The undergoing worldwide pandemic has greatly affected people's daily life and future plans.
# Thus,for CW2, I decide to conduct my project by connecting the pandemic and the knowledge we learned after week 6.
# As mentioned in my email, my project will mainly use the Markov model to simulate the infection progress of a virus not limited to Covid-19.
# The code I written below will be able to draw the infected progress in three different ages in scatter plots using markov model.
# Also, this program will be able to draw the line graph of three ages of people which enables us to compare the distribution of health state
# at the Markov equilibrium more intuitively.
# Some analysis and discussions will also be processed based on the result we get.


#We import the necessary package to use in our project.
import turtle
import random
import pandas as pd
import matplotlib.pyplot as plt

# Here, we innitialize the parameters needed for our graphing.
HEIGHT = 800
WIDTH = 1000
INIT_INFECTED = 0.1
TURTLE = False
PEOPLE_SIZE = 200
INFECTED_DISTANCE = 50
SIM_LOOPS = 30

# Here, to draw a dynamic scatter plot of the infection condition, we define a Class person.
class Person:
    # Here, we innitialize the beginning state of the infection.
    def __init__(self, age='kid'):
        # Here, for age, I decide to devide people into three different age: "kid", "Young Adults", and "Senior".
        # And for the infection states, I decide to divide into four states: "healthy", "asympotomatic_infected", "severe_infected"
        # and "Recovery"
        # The initial infection target will be at the original point 0,0.
        # The initial state will be healthy.
        # We define the variable probs as the infection probability.
        # And the healthy people will be marked as green color.
        self.age = age
        self.target = [0, 0]
        self.state = "healthy"
        self.probs = {}
        self.color = "green"
        # innitialize the probability from healthy to asymptomatic_infected
        if random.random() < INIT_INFECTED:
            self.state = "asymptomatic_infected"
        # Innitialize the probability from asymptomatic_infected to severe_infected
        elif random.random() < INIT_INFECTED:
            self.state = "severe_infected"
        # We customize the probability of transferring between the health states, detailed description of probability will be shown below.
        probs = [0.3, 0.8, 0.5, 0.2, 0.3, 0.2, 0.8, 0.3, 0.7]
        # Alse, we customize the infection radius for different ages, ie. when a healthy person and an infected person are inside that 
        # specific radius, the system will begin to apply a probability for the virus from infected person to infect the healthy person.
        # We also customize the step_size for different ages, ie. the person as a point will move at random inside a circle region.
        # for my program, I assume the kid has lower infected possibility with infection radius to be lower in relevant.
        # and also the kids are more active than other ages with a higher step size in relevant.
        if self.age == "kid":
            self.radius = 4
            self.step_size = 6
            probs = [0.5, 0.5, 0.2, 0.7, 0.1, 0.8, 0.2, 0.2, 0.8]
        elif self.age == "young":
            self.radius = 7
            self.step_size = 4
            probs = [0.7, 0.3, 0.3, 0.5, 0.2, 0.8, 0.2, 0.2, 0.8]
        else:
            self.radius = 10
            self.step_size = 2
        # Here we define the detailed meaning of probability inside the list prob, some transfer probability is not included because
        # they are 0 in commonsense, eg. there is no probability from severe_infected to healthy, it can only get to recovery.
        self.probs["healthy_asymptomatic"] = probs[0]
        self.probs["healthy_severe"] = probs[1]
        self.probs["asymptomatic_severe"] = probs[2]
        self.probs["asymptomatic_recovery"] = probs[3]
        self.probs["asymptomatic_asymptomatic"] = probs[4]
        self.probs["severe_recovery"] = probs[5]
        self.probs["severe_severe"] = probs[6]
        self.probs["recovery_asymptomatic"] = probs[7]
        self.probs["recovery_severe"] = probs[8]
        # Here we set the initial position of start point and destination.
        self.destination = self.get_random_position()
        self.position = self.get_random_position()
        self.update(0.0)

    def get_random_position(self):
        # Here, we define a function to return a random position x and y of destination based on the center of circle inside the x-y
        # coordinate system of the plane we set at the beginning.
        # Here, width is for the randomized x
        width = random.randint(-int(WIDTH / 2) + self.radius,
                               int(WIDTH / 2) - self.radius)
        # And height is for the randomized y
        height = random.randint(-int(HEIGHT / 2) + self.radius,
                                int(HEIGHT / 2) - self.radius) 
        return [width, height]

    def reach_destination(self):
        # Here we define another function to check if the scatters reach the destination where we use the Eucclidean distance formula to
        # calcualte the distance between the scatter and its destination.
        dis = (self.destination[1]-self.position[1])**2
        dis += (self.destination[0]-self.position[0])**2
        dis = dis**0.5
        if dis <= 10:
            return True
        else:
            return False

    def update_state(self, virus_rate):
        # To decide if we should update the infection state of people, we applied the percentage of infection inside the infection radious
        # to judge if we should update the state of infection. eg, if we have the infection pobability from healthy to asympotomatic_infected
        # for children to be 0.6 and there are 70% of people inside the infection radius of children who have been asympotomatic_infected,
        # then we will need to update the state of that child from healthy to asympotomatic_infected.
        # Here, we have 0 < virus_rate <= 1.
        if self.state == "healthy" or self.state == "recovery":
            infection_rate = random.random()
            type_rate = random.random()
            if self.state == "recovery":
                # We assume a lower infection rate for people who already recovered once.
                virus_rate = virus_rate * 0.8
                if infection_rate < virus_rate:
                    # Such condition means the person was infected
                    if type_rate < self.probs["recovery_asymptomatic"]:
                        self.state = "asymptomatic_infected"
            else:
                if infection_rate < virus_rate:
                    if type_rate < self.probs["healthy_asymptomatic"]:
                        self.state = "asymptomatic_infected"
        elif self.state == "asymptomatic_infected":
            # Considering the condition for the people who are asymptomatic_infected.
            change_rate = random.random()
            if change_rate < self.probs["asymptomatic_severe"]:
                self.state = "severe_infected"
            elif change_rate < self.probs["asymptomatic_severe"] + self.probs["asymptomatic_recovery"]:
                self.state = "recovery"
            else:
                self.state = "asymptomatic_infected"
        else:
            # Considering the condition for the people who are severe_infected.
            change_rate = random.random()
            if change_rate < self.probs["severe_recovery"]:
                self.state = "recovery"

    def update_positions(self):
        # Here we define a function to update the position of every person every day, where different ages have different step length.
        if self.reach_destination():
            self.destination = self.get_random_position()
        # Again, we calculate the distance moved by using the Eucclidean distance formula.
        dis = (self.destination[1] - self.position[1]) ** 2  
        dis += (self.destination[0] - self.position[0]) ** 2
        dis = dis ** 0.5
        x, y = self.position
        # And we update the position by adding the moved distance we calcualted
        x += self.step_size * (self.destination[0] - self.position[0])/dis
        y += self.step_size * (self.destination[1] - self.position[1]) / dis
        self.position = [x, y]

    def update(self, virus_rate):
        # Here, we define a function to update the infection state and change the color of scatter point based on that change.
        # We set the scatter point of healthy state to be black.
        # We set the scatter point of recovery state to be yellow.
        # We set the scatter point of asymptomatic_infected state to be purple.
        # We set the scatter point of severe_infected state to be red.
        self.update_positions()
        self.update_state(virus_rate)
        if self.state == "healthy":
            self.color = "black"
            self.spread = 0
        elif self.state == "recovery":
            self.color = "yellow"
            self.spread = 0
        elif self.state == "asymptomatic_infected":
            self.color = "purple"
            self.spread = 10
        else:
            self.color = "red"
            self.spread = 20

    def get_distance(self, other):
        # Here, we define a function to calculate the distance using the Eucclidean distance formula.
        dis = (other.position[1] - self.position[1]) ** 2  
        dis += (other.position[0] - self.position[0]) ** 2
        dis = dis ** 0.5
        return dis

# In order to update and show the state of infection for the scatter points everyday, I choose to use Turtle package to achieve this function.
# And I used matplotlib package again to draw the line graph.
# I set up a class Graphical to achieve both drawings.
class Graphical:
    def __init__(self):
        # Here, we initialize the necessary parameters.
        self.title = "Spread"
        self.people_size = PEOPLE_SIZE
        self.width = WIDTH
        self.height = HEIGHT
        self.people = []
        self.records = []
        for _ in range(self.people_size):
            # We add each person as scatter point inside the plane.
            self.people.append(Person('kid'))
            self.people.append(Person('young'))
            self.people.append(Person('old'))
        self.delay = 1000  # We update the delay for dispaly.
        if TURTLE:
            turtle.title(self.title)  # Title of turtle
            turtle.speed(0)
            turtle.setup(self.width+50, self.height+50)  # The size of display interface.
            turtle.hideturtle()  # Hide the turtle
            turtle.tracer(0, 0)  # prevent the drawing of movement trace.
            turtle.listen()
            turtle.mode('logo')  # Set the direction.
            turtle.penup()  # Hold the pen without drawing.
        self.infected_distance = INFECTED_DISTANCE
        self.hours = 0  # Add the time(hour)
        self.loop()

    def tick(self):
        # Here, we define a function tick to draw thru turtle.
        self.update()
        if TURTLE:
            self.draw()
        self.summary()

    def write(self):
        # Here we define a function write to draw the line graph.
        data = pd.DataFrame(self.records, columns=[
                            'Age', 'Healthy', 'Asymptomatic', 'Severe', 'recovery'])
        for name in ['Healthy', 'Asymptomatic', 'Severe', 'recovery']:
            data[name] = data[name]/self.people_size
        # Create and add the data to a csv file.
        data.to_csv('result.csv')
        
        # Here, we define a for loop to draw a summary table to see the distribution of probability at Markov Equilibrium state more claerly.
        for name in ['kids', 'youngs', 'olds']:
            plt.figure()
            x = range(len(data[data['Age'] == name]))
            ys = []
            for kind in ['Healthy', 'Asymptomatic', 'Severe', 'recovery']:
                y = data[data['Age'] == name][kind].values[-1]
                ys.append(y)
            plt.plot(x, data[data['Age'] == name]['Healthy'],
                     label='Healthy:' + str(ys[0]))
            plt.plot(x, data[data['Age'] == name]
                     ['Asymptomatic'], label='Asymptomatic: ' + str(ys[1]))
            plt.plot(x, data[data['Age'] == name]['Severe'],
                     label='Severe:' + str(ys[2]))
            plt.plot(x, data[data['Age'] == name]
                     ['recovery'], label='Recovery:' + str(ys[3]))
            plt.xlabel('Days')
            plt.ylabel('Probs')

            plt.legend()
            plt.title(name)

    def summary(self):
        # Here, we define a function summary to record the final condition of infection state for the three ages.
        kids = [0, 0, 0, 0]
        youngs = [0, 0, 0, 0]
        olds = [0, 0, 0, 0]
        for people in self.people:
            if people.age == 'kid':
                if people.state == 'healthy':
                    kids[0] += 1
                elif people.state == 'asymptomatic_infected':
                    kids[1] += 1
                elif people.state == 'severe_infected':
                    kids[2] += 1
                else:
                    kids[3] += 1
            elif people.age == 'young':
                if people.state == 'healthy':
                    youngs[0] += 1
                elif people.state == 'asymptomatic_infected':
                    youngs[1] += 1
                elif people.state == 'severe_infected':
                    youngs[2] += 1
                else:
                    youngs[3] += 1
            else:
                if people.state == 'healthy':
                    olds[0] += 1
                elif people.state == 'asymptomatic_infected':
                    olds[1] += 1
                elif people.state == 'severe_infected':
                    olds[2] += 1
                else:
                    olds[3] += 1
        self.records.append(['kids']+kids)
        self.records.append(['youngs']+youngs)
        self.records.append(['olds']+olds)
        print("Days: ", self.hours)
        # print("Kids ", kids)
        # print("Youngs ", youngs)
        # print("Olds ", olds)

    def update(self):
        # Here, we define a function update to update the infection state of people.
        self.hours += 1
        for people in self.people:
            infected = 0
            for people_2 in self.people:
                if people != people_2 and people.get_distance(people_2) < self.infected_distance:
                    infected += people_2.spread
            infected = min(1, infected/100)
            people.update(infected)

    def draw_people(self, people):
        # We defeine a function draw_people to draw the position of people day by day.
        # Here, we move the pen to the original point.
        turtle.penup() 
        # Here, we set our turtle to the origin point.
        turtle.goto(people.position[0], people.position[1])  
        turtle.pendown()
        turtle.dot(people.radius, people.color)

    def draw(self):
        # We define a function to draw trace thru turtle.
        turtle.clear()  # Clear the map.
        turtle.tracer(50)

        width, height = self.width, self.height
        turtle.penup()  # Hold up the pen.
        turtle.goto(-width/2, height/2)  # Draw the rectangle of interface.
        turtle.pendown()
        turtle.setheading(90)
        for x in range(2):
            turtle.forward(width)
            turtle.right(90)
            turtle.forward(height)
            turtle.right(90)

        turtle.write('Days:{0}'.format(self.hours), font=(10))
        for people in self.people:
            self.draw_people(people)

    def loop(self):
        if TURTLE:
            try:
                # Try to update.
                self.tick()
                turtle.ontimer(self.loop, self.delay)  # Update the motion.
            except turtle.Terminator:
                pass
        self.tick()

# Here, we call for the class Graphical to start.
g = Graphical()
# Here, the system will check if we require the turtle drawing function to go. If we set the TURTLE value to be True at the beginning,
# the turtle drawing will work.
if TURTLE:
    turtle.mainloop()
# If the TURTLE was set to be False, the line graph drawing function will be called and start to draw the line graph.
else:
    for i in range(SIM_LOOPS - 1):
        g.loop()
    g.write()
    plt.show()
    
# The project for CW2 is finished. Thank you!
