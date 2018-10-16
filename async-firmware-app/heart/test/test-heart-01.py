import random, time

cycles = 10000
center = 500

rand_factor = 400

rgb = [center for x in range(3)]

new_rgb = [random.randint(rand_factor*(-1), rand_factor) for x in range(3)]

print(rgb, new_rgb)

rgb = [rgb[x]+new_rgb[x] for x in range(3)]
print(rgb)
rgb = [rgb[x] - center for x in range(3)]
print(rgb)
rgb = [round((rgb[x]) * ((center - rand_factor)/center)) for x in range(3)]
# rgb = [int(((center-rand_factor)/center)*rgb[x]) for x in range(3)]
print(rgb)
rgb = [rgb[x] + center for x in range(3)]
print(rgb)
new_rgb = [random.randint(rand_factor*(-1), rand_factor) for x in range(3)]
rgb = [rgb[x]+new_rgb[x] for x in range(3)]
print(rgb)
# print(rgb)

for cycle in range(cycles):
    new_rgb = [random.randint(rand_factor * (-1), rand_factor) for x in range(3)]
    # rgb = [rgb[x] + new_rgb[x] for x in range(3)]
    rgb = [round((rgb[x] - center) * ((center - rand_factor)/center)) + center + new_rgb[x] for x in range(3)]
    print(rgb, new_rgb)
