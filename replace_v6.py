import os
import shutil
import re
from argparse import ArgumentParser


def create_dirs():

    # La carpeta que se va a usar para modificar los archivos bvh
    main_dir = 'Modificador'
    # Las 2 carpetas donde van a ir los nuevos archivos y los archivos originales
    dirs = ['Nuevo', 'Cambiado']

    # Verifica que la carpeta principal exista y que sea una carpeta, de no ser asi es creada
    if not os.path.exists(main_dir):
        os.mkdir(main_dir)
    else:
        if not os.path.isdir(main_dir):
            os.mkdir(main_dir)

    # Entra a la carpeta principal para crear las 2 subcarpetas
    os.chdir(os.path.join(os.getcwd(), 'Modificador'))

    # Verifica que las carpetas Nuevo y Cambiado existan y que sean carpetas, de no ser asi son creadas
    for cur_dir in dirs:
        if os.path.exists(cur_dir):
            if not os.path.isdir(cur_dir):
                os.mkdir(cur_dir)
        else:
            os.mkdir(cur_dir)


def move_files(changed, new):

    # Mueve los archivos a las carpetas correspondientes solamente si previamente no existian y si son archivos
    for file in changed:
        if os.path.exists(os.path.sep.join([os.path.abspath('Cambiado'), file]))\
                and os.path.isfile(os.path.sep.join([os.path.abspath('Cambiado'), file])):
            pass
        # else:
            # shutil.move(file, os.path.abspath('Cambiado'))
    for file in new:
        if os.path.exists(os.path.sep.join([os.path.abspath('Nuevo'), file]))\
                and os.path.isfile(os.path.sep.join([os.path.abspath('Nuevo'), file])):
            pass
        else:
            shutil.move(file, os.path.abspath('Nuevo'))


def replace_offsets(offsets_file):

    # Contador para la cantidad de veces que una linea ha sido modificada
    offset_counter = 0

    # Listas de los datos especificados/deseados, los archivos originales que ya fueron procesados,
    # y los nuevos archivos con los cambios de offsets a los offsets deseados
    offsets = []
    changed_files = []
    new_files = []

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Remover comentario si se quiere usar el archivo de offsets
    # en la misma carpeta donde se encuentra el script de Python
    # with open(offsets_file, 'r') as rf:
    #     for line in rf:
    #         offsets.append(line.strip('\n'))
    #     rf.close()
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Llama al metodo auxiliar que crea carpetas solo cuando la carpeta principal 'Modificador' no exista
    # y se va a crear en la misma ubicacion del script.
    if not os.path.exists('Modificador'):
        create_dirs()
    else:
        # Entra a la carpeta principal y guarda los valores de offset del archivo offsets
        os.chdir(os.path.join(os.getcwd(), 'Modificador'))
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Remover comentario se quiere usar el archivo de offsets
        # en la misma carpeta donde se arrastran los archivos

        # Abre el archivo de los offsets especificados, los añade a una lista
        # y cuenta el numero de lineas que deberia ser 25
        with open(offsets_file, 'r') as rf:
            for line_index, line in enumerate(rf):
                offsets.append(line.strip('\n'))
            rf.close()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # En el caso de que la cantidad de lineas del archivo de offsets especificados no fuera 25,
        # le dice al usuario que el archivo deberia tener 25 lineas y este tiene el numero de lineas incorrecto
        if not (line_index + 1).__eq__(25):
            print(f'\nEl archivo tiene que tener 25 lineas. Este archivo tiene {line_index + 1} lineas.')
        else:
            # Separa los archivos en el nombre y la extension
            # Remover el os.getcwd(), si este diera problemas: for file in os.listdir():
            for file in os.listdir(os.getcwd()):
                f_name, f_ext = os.path.splitext(file)

                # Verifica lo que tenga extension bvh y lo demas lo ignora
                if f_ext == '.bvh':
                    new_file = 'modificado_'+str(file)
                    # Previene modificar un archivo mas de una vez
                    # ('Mientras que el archivo modificado no haya sido removido de la carpeta')
                    if not os.path.exists(os.path.join(os.getcwd(), 'Nuevo', new_file)):
                        with open(os.path.join(os.getcwd(), 'Nuevo', new_file), 'w') as f:
                            # Abre el archivo original y guarda su contenido en una lista
                            with open(file, 'r') as of:
                                for line in of:
                                    # Busca las lineas a modificar en el archivo original
                                    stripped_line = str(line).rstrip('\n').lstrip()
                                    if re.search('OFFSET', stripped_line):
                                        line = line.replace(stripped_line, offsets[offset_counter]
                                                            .rjust(len(stripped_line)))
                                        offset_counter += 1
                                    # Es necesario que se escriba afuera del if para que se copien todas las lineas
                                    # Copia todas las lineas al nuevo archivo junto con las lineas modificadas
                                    f.write(line)
                            # Resetea el contador que recorre la lista de offsets
                            offset_counter = 0
                            # Prepara las listas para seleccionar a que carpeta pertenece cada archivo finalizado
                            changed_files.append(file)
                            new_files.append(new_file)
            # Llama el metodo que mueve los archivos a su carpeta correspondiente segun las listas anteriores
            move_files(changed_files, new_files)


def bvh_modifier():

    # Llama al metodo auxiliar que crea carpetas solo cuando la carpeta principal 'Modificador' no exista
    # y se va a crear en la misma ubicacion del script.
    if not os.path.exists('Modificador'):
        create_dirs()
    else:
        # Objeto para agregar argumentos de linea de comando al script
        parser = ArgumentParser()

        # El argumento para añadir un archivo de texto de los offsets deseados
        # al script al momento de correrlo en la consola
        parser.add_argument('-f', '--filename', dest='offsets_file',
                            default='offsets.txt', help='Arrastre el archivo con los offsets deseados.'
                                                        'Si no se provee ningun archivo,'
                                                        'por defecto usa el archivo offstets.txt')

        # Procesa y alista los argumentos para ser usados
        args = parser.parse_args()

        if not(os.path.exists(os.path.join(os.getcwd(), "Modificador", "offsets.txt")) or os.path.exists(os.path.join('Modificador', args.offsets_file))):
            print('\nEl programa requiere que se incluya el archivo offsets.txt')
        else:
            # divide el archivo en nombre y extension
            f_name, f_ext = os.path.splitext(args.offsets_file)
            # Revisa si el archivo existe
            # y si no existe le dice al usuario que tiene un error en el nombre y que no existe
            '''
            Si prefiere el archivo offsets.txt en la misma carpeta del script
            if not os.path.exists(args.offsets_file):
            '''
            # Si prefiere el archivo offsets.txt en la misma carpeta de los BVH
            if not os.path.exists(os.path.join('Modificador', args.offsets_file)):
                print(f'\nError en el nombre de archivo. El archivo {args.offsets_file} no existe')
            else:
                # Revisa si el archivo es un archivo de texto con extension de txt
                # y si no lo es le dice al usuario que no lo es y le dice el nombre y tipo de archivo intento usar
                if not f_ext == '.txt':
                    print('\nEl archivo tiene que ser un archivo de texto txt. El archivo',
                          os.path.basename(f_name), 'usado es un archivo', f_ext[1:])
                else:
                    replace_offsets(args.offsets_file)


def main():
    bvh_modifier()


if __name__ == '__main__':
    main()

