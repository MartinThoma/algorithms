import hasy_tools

data = hasy_tools.load_data()
print(data.keys())
# dict_keys(['x_train', 'y_train', 'x_test', 'y_test', 's_train', 's_test', 'labels'])

print(data['x_train'].shape)
