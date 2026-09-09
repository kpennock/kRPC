import krpc
conn = krpc.connect(name='API check')
vessel = conn.space_center.active_vessel

print("type of vessel.delta_v:", type(vessel.delta_v))
print("value:", vessel.delta_v)
print()
print(dir(vessel))

stages = vessel.stages
print(type(stages), len(stages))
print(dir(stages[0]))