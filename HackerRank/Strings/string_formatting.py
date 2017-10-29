def print_formatted(number):
    width = len('{0:b}'.format(number))
    for i in range(1, number+1):
        print(" ".join([('%d' % i).rjust(width), ('%o' % i).rjust(width), ('%X' % i).rjust(width), ("{0:b}".format(i)).rjust(width)]))

