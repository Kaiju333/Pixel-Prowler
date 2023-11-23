import tensorflow as tf

test_reloaded = tf.saved_model.load('test')

states = None
next_char = tf.constant(['  '])
result = [next_char]

for n in range(300):
  next_char, states = test_reloaded.generate_test(next_char, states=states)
  print(next_char)
  print("break")
  result.append(next_char)

print("\nFinal Result:")
print(tf.strings.join(result)[0].numpy().decode('utf-8'))
level_data = str(tf.strings.join(result)[0].numpy())
print(level_data)
processed_level_data = level_data.replace("b'","")
processed_level_data = processed_level_data.split("\\r\\n")
processed_level_data = ["","","",""] + processed_level_data
print(processed_level_data)