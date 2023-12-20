from collections import deque
from dataclasses import dataclass
from enum import Enum


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


class Pulse(Enum):
    HIGH = 1
    LOW = 0


def toggle(pulse):
    if pulse == Pulse.HIGH:
        return Pulse.LOW
    return Pulse.HIGH


@dataclass
class Module:
    type: str
    label: str
    output: list
    state: Pulse
    inputs: dict

    def __init__(self, type, label, output):
        self.type = type
        self.label = label
        self.output = output
        self.state = Pulse.LOW
        self.inputs = {}

    def set_inputs(self, inputs):
        self.inputs.update(inputs)

    def process(self, from_module, pulse):
        if self.type == "%":
            if pulse == Pulse.LOW:
                self.state = toggle(self.state)
                return self.state
            return None
        if self.type == "&":
            self.inputs.update({from_module: pulse})
            if all(map(lambda input: input[1] == Pulse.HIGH, self.inputs.items())):
                return Pulse.LOW
            return Pulse.HIGH
        if self.type == "b":
            return pulse


def parse_input(input):
    modules = {}
    for line in input:
        l1, l2 = line.split("->")
        type = l1[0]
        label = l1[1:].strip()
        output = [t.strip() for t in l2.split(",")]
        module = Module(type, label, output)
        modules.update({label: module})
    for module in modules:
        label = modules[module].label
        inputs = {}
        for m in modules:
            if label in modules[m].output:
                inputs.update({modules[m].label: Pulse.LOW})
        modules[module].set_inputs(inputs)
    return modules


def part1(input):
    modules = parse_input(input)

    count_low = 0
    count_high = 0
    for i in range(1000):
        queue = deque()
        queue.append((None, "roadcaster", Pulse.LOW))
        while len(queue):
            from_label, current_label, input_pulse = queue.popleft()
            if input_pulse == Pulse.HIGH:
                count_high += 1
            else:
                count_low += 1
            if current_label in modules:
                current = modules[current_label]
                output_pulse = current.process(from_label, input_pulse)
                if output_pulse != None:
                    for m in current.output:
                        queue.append((current_label, m, output_pulse))
    return count_high * count_low


def part2(input):
    modules = parse_input(input)

    outputs_to_end = None
    for m in modules:
        if "rx" in modules[m].output:
            outputs_to_end = m
            break

    interesting_labels = modules[outputs_to_end].inputs.keys()
    interesting_occurences = {}
    for l in interesting_labels:
        interesting_occurences.update({l: []})

    for i in range(8000):
        queue = deque()
        queue.append((None, "roadcaster", Pulse.LOW))
        while len(queue):
            from_label, current_label, input_pulse = queue.popleft()
            if current_label in interesting_labels and input_pulse == Pulse.LOW:
                interesting_occurences[current_label].append(i)
            if current_label in modules:
                current = modules[current_label]
                output_pulse = current.process(from_label, input_pulse)
                if output_pulse != None:
                    for m in current.output:
                        queue.append((current_label, m, output_pulse))

    result = 1
    for occurences in interesting_occurences.values():
        assert len(occurences) == 2
        result *= occurences[1] - occurences[0]
    return result


testInput1 = readInput("20_test1.txt")
assert part1(testInput1) == 32000000

testInput2 = readInput("20_test2.txt")
assert part1(testInput2) == 11687500

input = readInput("20.txt")
print(part1(input))
print(part2(input))
