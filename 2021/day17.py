from aocd import lines
import re

class Probe:
    def __init__(self, spec):
        (x1,x2,y1,y2) = map(int,re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', spec).groups())
        self.targetCoords = ((min(x1,x2),min(y1,y2)),(max(x1,x2),max(y1,y2)))

    def __hits(self, pos, velocity, max_height):
        while True:
            # Are we in the target?
            if (pos[0] >= self.targetCoords[0][0] and pos[0] <= self.targetCoords[1][0] and 
                    pos[1] >= self.targetCoords[0][1] and pos[1] <= self.targetCoords[1][1]):
                return max_height
            # If we're below the target area, this isn't going to work.
            if pos[1] < self.targetCoords[0][1]:
                return -1000
            max_height = max(max_height, pos[1])
            pos = (pos[0] + velocity[0], pos[1] + velocity[1])
            velocity = (0 if velocity[0] == 0 else velocity[0] - 1, 
                        velocity[1] - 1)

    def does_hit(self, velocity):
        pos = (0,0)
        return self.__hits(pos, velocity, 0)

    def dp_check(self):
        # find a value that hits the target, and keep the max height.
        max_height = 0
        best_velocity = (-1,-1)

        # first, fire with y_vel = 0, and find a x_vel that works.
        for x_vel in range(1,500):
            if self.does_hit((x_vel,0)) > -1000:
                break
        # Ok, now we have a baseline x_velocity. 
        max_height = 0
        y_vel = 0
        while True:
            # Raise the y_velocity until probe misses the target area
            y_vel += 1
            height = self.does_hit((x_vel, y_vel))
            if (height == -1000):
                y_vel -= 1
                break
            if height > max_height:
                best_velocity = (x_vel, y_vel)
                max_height = height
        while True:
            # now, we keep the y_velocity the same and lower x until it leaves the target
            x_vel -= 1
            height = self.does_hit((x_vel, y_vel))
            if (height == -1000):
                x_vel += 1
                break
            if height > max_height: 
                best_velocity = (x_vel, y_vel)
                max_height = height
        
        (x_vel, y_vel) = best_velocity
        updated = True
        while updated:
            # perturb the velocity in all directions; move in the best direction.
            # if we've reached a local maximum, then return it.
            updated = False
            for xv in range(x_vel - 1, x_vel + 2):
                for yv in range (y_vel - 1, y_vel +2):
                    height = self.does_hit((xv,yv))
                    if height > max_height:
                        best_velocity = (xv,yv)
                        max_height = height
                        updated = True
            break

        return max_height

    def brute_force(self):
        max_height = 0
        for xv in range(1,200):
            for yv in range(1,200):
                height = self.does_hit((xv,yv))
                if height > max_height:
                    best_velocity = (xv,yv)
                    max_height = height
        print(f'best vel={best_velocity}')
        return max_height

    def find_height(self):
        return self.brute_force()

    def enumerate_all_velocities(self):
        vels = []
        for xv in range(1,self.targetCoords[1][0] + 1):
            for yv in range(self.targetCoords[0][1],400):
                height = self.does_hit((xv,yv))
                if height != -1000:
                    vels.append((xv,yv))
        return len(vels)


test = "target area: x=20..30, y=-10..-5"
assert(Probe(test).brute_force() == 45)
print ('17a: ', Probe(lines[0]).brute_force())

assert(Probe(test).enumerate_all_velocities() == 112)
print ('17b: ', Probe(lines[0]).enumerate_all_velocities())