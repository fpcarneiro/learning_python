group_size = int(input())
room_number_list = []
for r in input().split(" "):
    e = room_number_list.get(int(r),[])
    e.append(int(r))
    room_number_list[int(r)] = e
    print(room_number_list)
print(room_number_list)
#print(capitain)

