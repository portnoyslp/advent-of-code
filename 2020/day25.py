from aocd import data


def parse(input_str):
    card_key, door_key = input_str.split()
    return int(card_key), int(door_key)


def transform(subject_num, loop_size):
    cur_val = 1
    for l in range(loop_size):
        cur_val = transform_step(cur_val, subject_num)
    return cur_val


def transform_step(cur_val, subject_num):
    cur_val *= subject_num
    cur_val %= 20201227
    return cur_val


def crack_key(key, subject_num=7):
    loop_size = 1
    val = subject_num
    while True:
        loop_size += 1
        val = transform_step(val, subject_num)
        if val == key:
            break
    return loop_size


def get_enc_key(input_str):
    card_key, door_key = parse(input_str)
    card_loop_size = crack_key(card_key)
    door_loop_size = crack_key(door_key)
    if card_loop_size < door_loop_size:
        return transform(door_key, card_loop_size)
    else:
        return transform(card_key, door_loop_size)


assert get_enc_key('5764801 17807724') == 14897079
print(f'25a: {get_enc_key(data)}')
