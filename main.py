import os
import sys
import imagenes

script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
output_path = os.path.join(script_path, 'output')
input_path = os.path.join(script_path, 'input')

if __name__ == '__main__':
    for file in os.listdir(input_path ):
        print(sys.path)
        name = file
        pdf_path = os.path.join(input_path, file)
        name_without_extension = name[:-4]
        imagenes.convert_draw(pdf_path, output_path, name_without_extension)



