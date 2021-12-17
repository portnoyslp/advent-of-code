from aocd import lines

def bitstring(hexstring):
    output = ''
    for x in hexstring:
        str = bin(int(x, 16))[2:]
        n = len(str)
        if n % 4 != 0:
	        str = '0' * (4 - n % 4) + str
        output += str
    return output

class Packet:
    def __init__(self):
        self.subpackets = []
        self.version = None;
        self.value = None;
        self.type_id = None;
    
    def __repr__(self):
        return f'Packet<{self.version}/{self.type_id}:{self.value if len(self.subpackets) == 0 else self.subpackets}>'

    def __sum(self):
        return sum([x.value for x in self.subpackets])
    
    def __product(self):
        out = 1
        for x in self.subpackets:
            out *= x.value
        return out

    def __min(self):
        return min([x.value for x in self.subpackets])

    def __max(self):
        return max([x.value for x in self.subpackets])
    
    def __gt(self):
        return 1 if self.subpackets[0].value > self.subpackets[1].value else 0

    def __lt(self):
        return 1 if self.subpackets[0].value < self.subpackets[1].value else 0

    def __eq(self):
        return 1 if self.subpackets[0].value == self.subpackets[1].value else 0
    
    operations = {0 : __sum, 1: __product, 2: __min, 3: __max, 5: __gt, 6: __lt, 7: __eq }

    # Reads a packet from the string, and returns the part of the string that still has to be processed.
    def read_packet(self, binstring):
        self.version = int(binstring[:3],2)
        self.type_id = int(binstring[3:6], 2)
        
        cur_idx = 6
        if self.type_id == 4:
            # this is an immediate value.
            valstring = ""
            while True:
                valstring += binstring[cur_idx+1:cur_idx+5]
                eom = binstring[cur_idx] == '0'
                cur_idx += 5
                if eom:
                    break
            self.value = int(valstring, 2)
            return binstring[cur_idx:]

        # There are subpackets, and an operation to consider.
        cur_idx += 1
        if binstring[6] == '0':
            # next 15 bits are the length.
            packet_len = int(binstring[cur_idx:cur_idx + 15], 2)
            subpacket_string = binstring[cur_idx + 15:cur_idx + 15 + packet_len]
            leftover = binstring[cur_idx + 15 + packet_len:]
            while subpacket_string != '':
                packet = Packet()
                remaining = packet.read_packet(subpacket_string)
                self.subpackets.append(packet)
                subpacket_string = remaining
        else:
            # next 11 bits are the number of packets.
            num_packets = int(binstring[cur_idx:cur_idx + 11], 2)
            leftover = binstring[cur_idx+11:]
            for i in range(0,num_packets):
                packet = Packet()
                leftover = packet.read_packet(leftover)
                self.subpackets.append(packet)

        # calculate value according to type.
        self.value = self.operations[self.type_id](self)
        return leftover
    
    def value(self):
        return self.value

    def subpackets(self):
        return self.subpackets

    def sum_of_versions(self):
        return self.version + sum([p.sum_of_versions() for p in self.subpackets])

def version_sum(input):
    packet = Packet()
    packet.read_packet(bitstring(input))
    return packet.sum_of_versions()
    
def value(input):
    packet = Packet()
    packet.read_packet(bitstring(input))
    return packet.value

assert(version_sum('D2FE28') == 6)
assert(version_sum('38006F45291200') == 9)
assert(version_sum('EE00D40C823060') == 14)

assert(version_sum('8A004A801A8002F478') == 16)
assert(version_sum('620080001611562C8802118E34') == 12)
assert(version_sum('C0015000016115A2E0802F182340') == 23)
assert(version_sum('A0016C880162017C3686B18A3D4780') == 31)
print('16a: ', version_sum(lines[0]))


assert(value('C200B40A82') == 3)
assert(value('04005AC33890') == 54)
assert(value('880086C3E88112') == 7)
# CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
# D8005AC2A8F0 produces 1, because 5 is less than 15.
# F600BC2D8F produces 0, because 5 is not greater than 15.
# 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
assert(value('9C0141080250320F1802104A08') == 1)

print('16b: ', value(lines[0]))