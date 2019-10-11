from itertools import chain

def get_number_of_layers(input):
    """Returns the number of layers in the neural network"""
    count=0
    for layer in input['config']['layers']:
        count = count + 1
    return count + 1

def get_bias_array(input, numberLayers):
    """Returns a flattened array of bias values"""
    count=0
    output= [None] * numberLayers
    for layer in input['config']['layers']:
        output[count] = layer['bias_values']
        count = count + 1
    #? Flattening the array before returning
    return list(chain.from_iterable(output))

def get_weights_array(input, numberLayers):
    """Returns a flattened array of weights values"""
    count=0
    output= [None] * numberLayers
    for layer in input['config']['layers']:
        output[count] = list(chain.from_iterable(layer['kernel_values']))
        count = count + 1
    #? Flattening the array before returning
    return list(chain.from_iterable(output))

def replace_markers(file, markers):
    """ Replaces all given markes in given file with their respective value"""
    for marker, value in markers.items():
        file = file.replace(marker,str(value))
    return file

def read_marker_file(filename):
    """ Reads given filename"""
    with open(filename, 'r') as file:
        return file.read()

def build_activation_function_string(input, activation_functions):
    """Returns a string containing an array of indices representing the activation function for each layer"""
    array = []
    for layer in input['config']['layers']:
        #? Dictionary activation_functions contains the mapping to the indices
        array.append(str(activation_functions[layer['config']['activation'].lower()]))
    return convert_array_to_string(array)

def build_use_bias_string(input):
    """Returns a string containing an array of bools indicating the usage of biases"""
    array = []
    for layer in input['config']['layers']:
        array.append(str(int(layer['config']['use_bias'])))
    return convert_array_to_string(array)

def build_units_in_layers_string(input):
    """Returns a string containing an array of number of units for each layer"""
    first_layer = True
    array = []
    for layer in input['config']['layers']:
        #? First layer has to be treated different because of input shape
        if (first_layer):
            array.append(str(layer['config']['batch_input_shape'][1]))
            first_layer=False
        array.append(str(layer['config']['units']))
    return convert_array_to_string(array)

def build_layer_types_string(input, layer_types):
    """Returns a string containing an array of indices representing the layer type for each layer"""
    array = []
    for layer in input['config']['layers']:
        #? Dictionary layer_types contains the mapping to the indices
       array.append(str(layer_types[layer['class_name'].lower()]))
    return convert_array_to_string(array)

def build_indices_weights_string(input):
    """Returns a string containing an array of indices indicating the start position of weights for each layer"""
    last_layer_values = 0
    array=[]
    for layer in input['config']['layers']:
        array.append(str(last_layer_values))
        last_layer_values = last_layer_values + int(layer['config']['units']) * int(layer['config']['batch_input_shape'][1])
    return convert_array_to_string(array)

def build_indices_bias_string(input):
    """Returns a string containing an array of indices indicating the start position of biases for each layer"""
    last_layer_values = 0
    array=[]
    for layer in input['config']['layers']:
        array.append(str(last_layer_values))
        last_layer_values = last_layer_values + layer['config']['units']
    return convert_array_to_string(array)

def convert_array_to_string(array):
    """Returns a string containing the given array"""
    string = '{'
    for value in array:
        string = string + str(value) + ','
    return string[:-1] + '}'