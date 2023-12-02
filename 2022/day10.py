from aocd import data
import queue

def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start + n]

class Processor:
    def __init__(self, data):
        self.all_instructions = data.splitlines()
        self.cycle_start = 20
        self.cycle_period = 40
        self.cycle_end = 220
    
    def run(self):
        self.sum_strength = 0
        self.reg_x = 1
        self.cur_cycle = 1
        self.next_process_cycle = 1
        self.finish_add_cycle = -1
        self.pending_add = 0
        self.instructions = queue.SimpleQueue()
        for i in self.all_instructions:
            self.instructions.put(i)

        while self.cur_cycle <= self.cycle_end:
            self.next_cycle(self.add_strength)
        return self.sum_strength
    
    def add_strength(self):
        if (self.cur_cycle - self.cycle_start) % self.cycle_period == 0:
                # print('--> Add strength of {} for cycle {}'.format(self.reg_x, self.cur_cycle))
                self.sum_strength += self.reg_x * self.cur_cycle
    
    def render(self):
        self.reg_x = 1
        self.cur_cycle = 1
        self.next_process_cycle = self.cur_cycle
        self.finish_add_cycle = -1
        self.pending_add = 0
        self.instructions = queue.SimpleQueue()
        self.end_cycle = 240
        
        self.lines = []
        self.cur_line = ''
        for i in self.all_instructions:
            self.instructions.put(i)

        while self.cur_cycle <= self.end_cycle:
            self.next_cycle(self.render_sprite)
        
        return "\n".join(self.lines)
    
    def render_sprite(self):
        curpos = len(self.cur_line)
        # print('During cycle {0:3} CRT draws pixel in position {1}'.format(self.cur_cycle, curpos))
        self.cur_line += ('#' if abs(curpos - self.reg_x) <= 1 else '.')
        # print('Current CRT row: ', self.cur_line)
        if (len(self.cur_line) == 40):
            self.lines.append(self.cur_line)
            self.cur_line = ''
        
    def next_cycle(self, callback=None):
        if self.cur_cycle == self.next_process_cycle:
            # Fetch next instruction
            if self.instructions.empty():
                self.cur_cycle += 1
                return
            inst = self.instructions.get()
            
            # print('Start cycle  {0:3} begin executing {1}'.format(self.cur_cycle, inst))
        # Render if needed
        if callback:
            callback()
        
        # Finish cycle processing
        if self.finish_add_cycle == self.cur_cycle:
            self.reg_x += self.pending_add
            # print('End of cycle {0:3} finish executing addx {1} (register now at {2})'.format(self.cur_cycle, self.pending_add, self.reg_x))
            # print('Sprite position: ' + ('.' * (self.reg_x - 1)) + '###')

        if self.cur_cycle == self.next_process_cycle:
            # Set up processing of next instruction
            if inst == 'noop':
                self.next_process_cycle = self.cur_cycle + 1
                self.pending_add = 0
                self.finish_add_cycle = -1
            else:
                self.pending_add = int(inst[5:])
                self.next_process_cycle = self.cur_cycle + 2    
                self.finish_add_cycle = self.cur_cycle + 1
        # next cycle
        self.cur_cycle += 1            

ex1="""addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

assert Processor(ex1).run() == 13140
print('10a: ', Processor(data).run())

assert Processor(ex1).render() == """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
print('10b: '); print(Processor(data).render()