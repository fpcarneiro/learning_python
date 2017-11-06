def get_capitain_room(size, room_list):
    k = ((len(room_list)-1)//size)
    room_list.sort()
    d = set()
    for i in range(0,size-2):
        regular1 = set(room_list[i:(size*k)+i:size])
        regular2 = set(room_list[i+1:(size*k)+i:size])
        regular3 = set(room_list[i+2:(size*k)+i:size])
        capitain = (regular1 - regular2) & (regular1 - regular3)
        if len(capitain) != 0:
            break
    else:
        capitain = set([room_list[-1]])
    return capitain.pop()


if __name__ == "__main__":
    group_size = int(input())
    room_number_list = list(map(int, input().split(" ")))
    print(get_capitain_room(group_size, room_number_list))

