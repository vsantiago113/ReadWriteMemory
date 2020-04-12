from Test.ReadWriteMemory import ReadWriteMemory
from random import randint

rwm = ReadWriteMemory()
process = rwm.get_process_by_name('ac_client.exe')
process.open()

print('\nPrint the Process information.')
print(process.__dict__)

health_pointer = process.get_pointer(0x004e4dbc, offsets=[0xf4])
ammo_pointer = process.get_pointer(0x004df73c, offsets=[0x378, 0x14, 0x0])
grenade_pointer = process.get_pointer(0x004df73c, offsets=[0x35c, 0x14, 0x0])
print(health_pointer)

health = process.read(health_pointer)
ammo = process.read(ammo_pointer)
grenade = process.read(grenade_pointer)

print('\nPrinting the current values.')
print({'Health': health, 'Ammo': ammo, 'Grenade': grenade})

process.write(health_pointer, randint(1, 100))
process.write(ammo_pointer, randint(1, 20))
process.write(grenade_pointer, randint(1, 5))

health = process.read(health_pointer)
ammo = process.read(ammo_pointer)
grenade = process.read(grenade_pointer)

print('\nPrinting the new modified random values.')
print({'Health': health, 'Ammo': ammo, 'Grenade': grenade})

process.close()
