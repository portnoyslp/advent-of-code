from aocd import data
from math import lcm

class Component:
    def __init__(self, name, harness, outputs) -> None:
        self.incoming = []
        self.outputs = outputs
        self.harness = harness
        self.name = name

    def set_outputs(self, new_outputs):
        self.outputs = new_outputs

    def add_incoming_wire(self, component_in):
        self.incoming.append(component_in)

    def process_signal(self, value, component_in):
        pass

class FlipFlop(Component):
    def __init__(self, name, harness, outputs) -> None:
        super().__init__(name, harness, outputs)
        self.state = False # off
    
    def process_signal(self, value, component_in):
        if not value:
            self.state = not self.state
            for output in self.outputs:
                self.harness.queue_signal(self.name, self.state, output)
        return super().process_signal(value, component_in)

class Broadcaster(Component):
    def __init__(self, name, harness, outputs) -> None:
        super().__init__(name, harness, outputs)
    
    def process_signal(self, value, component_in):
        for output in self.outputs:
            self.harness.queue_signal(self.name, value, output)
        return super().process_signal(value, component_in)

class Conjunction(Component):
    def __init__(self, name, harness, outputs) -> None:
        self.input_memory = {}
        super().__init__(name, harness, outputs)

    def add_incoming_wire(self, component_in):
        self.input_memory[component_in] = False
        return super().add_incoming_wire(component_in)

    def process_signal(self, value, component_in):
        self.input_memory[component_in] = value
        num_lows = sum([1 for x in self.input_memory.values() if not x])
        output_pulse = num_lows > 0
        for output in self.outputs:
            self.harness.queue_signal(self.name, output_pulse, output)
        return super().process_signal(value, component_in)

class Harness:
    def __init__(self, data):
        self.pulse_count = {True: 0, False: 0}
        self.pulse_queue = []
        self.components = {}

        for line in data.splitlines():
            label,dest_str = line.split(' -> ')
            outputs = dest_str.split(', ')
            if label.startswith('%'):
                self.components[label[1:]] = FlipFlop(label[1:], self, outputs)
            elif label.startswith('&'):
                self.components[label[1:]] = Conjunction(label[1:], self, outputs)
            elif label == 'broadcaster':
                self.components[label] = Broadcaster(label, self, outputs)
            else:
                print(f'Unexpected component {label}')
        # wire inputs for each
        for label, component in self.components.items():
            for output in component.outputs:
                if output in self.components:
                    self.components[output].add_incoming_wire(label)

    def push_button(self):
        self.queue_signal('button', False, 'broadcaster')
        self.run_queue()
            
    def queue_signal(self, from_component, signal, to_component):
        self.pulse_queue.append( (from_component, signal, to_component) )

    def run_queue(self):
        while len(self.pulse_queue) > 0:
            signal = self.pulse_queue.pop(0)
            from_component,value,to_component = signal
            self.pulse_count[value] += 1
            if to_component == 'gq' and value:
                print(f'{from_component} -{"high" if value else "low"}-> {to_component}')
            if to_component in self.components:
                component = self.components[to_component]
                component.process_signal(value, from_component)

def run(data, part=1):
    harness = Harness(data)
    if part == 1:
        for i in range(1000):
            harness.push_button()
        return harness.pulse_count[True] * harness.pulse_count[False]
    
    # For part 2, this does not work at all; there's just too much stuff to do it by brute force
    # We need to count button presses to get to the output. That's almost certainly feeding a 
    # Conjunction/NAND gate. So, we see how many button pushes it takes to get a True signal
    # on each of the inputs to that NAND, and assume that a LCM will suffice for getting all four in sync.

    nand = [x for x in harness.components.values() if 'rx' in x.outputs][0]
    nand_inputs = list(nand.input_memory.keys())
    button_presses = {}

    button_cnt = 1
    while True:
        harness.push_button()
        for input,val in nand.input_memory.items():
            if val and input not in button_presses:
                button_presses[input] = button_cnt
        if len(button_presses) == len(nand_inputs):
            return lcm(button_presses.values())
        button_cnt += 1

ex1='''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
'''

ex2='''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''

assert run(ex1) == 32000000
assert run(ex2) == 11687500
print('20a: ', run(data))
print('20b: ', run(data, part=2))