group_size = int(input())
room_number_list = input().split(" ")
different = set(room_number_list)
g = {room_number_list.count(e):e for e in different}
print(g[1])
#print(capitain)

