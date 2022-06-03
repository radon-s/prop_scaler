import subprocess

"""
Prop scaler by Hammer
"""


class prop_scaler:
    def __init__(self, path, new_path, name, scale):
        # defining names
        self.path_input = path
        self.name = name
        self.scale = scale
        self.new_path = new_path
        self.path_qc = f'{path}\\{name}.qc'
        self.path_qc_new = f'{path}\\{name}_scaled_{scale.replace(".","_")}.qc'
        self.path_bat = f'{path}/prop_scaler_compiler.bat'
        self.studiomdl = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Source\\bin\\studiomdl.exe"
        self.gamefolder = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Source\\cstrike"

    def read_qc(self):
        # reading .qc and storing the document
        try:
            with open(self.path_qc, 'r') as file:
                document = file.readlines()
                file.close()
        except OSError:
            print(f'\n{self.path_qc} not found!\n')
            e = 1
            return e
        else:
            return document

    def scale_line(self):
        # creating the scale line used in the document
        scale_line = f'\n$scale {self.scale}\n\n'
        return scale_line

    def bbox(self):
        # locating the bbox in the document and duplicating it according to the scale
        x = -1
        bbox_old = 'a'
        for line in self.read_qc():
            x += 1
            if line.startswith('$bbox'):
                bbox_old = [line]
                break

        if bbox_old != 'a':
            bbox_num = []
            for num in bbox_old[0].split():
                try:
                    bbox_num.append(float(num))
                except ValueError:
                    pass
            try:
                bbox_scale = [round(num * float(self.scale), 3) for num in bbox_num]
                bbox_scale_str = ' '.join(map(str, bbox_scale))
                bbox_line = f'$bbox {bbox_scale_str}\n'
                return [bbox_line, x]
            except ValueError:
                print(f'\n{self.scale} is not a valid scale!\n')
                return 1

        else:
            print('\nNo $bbox in .qc file!\n')
            error = 1
            return error

    def model_name(self):
        # locating the modelname in the document and adding the scale to it
        y = -1
        modelname = 'a'
        for line in self.read_qc():
            y += 1
            if line.startswith('$modelname'):
                modelname = line
                break

        if modelname != 'a':
            splitter = '\\'
            modelname_new = f'{modelname[:-6]}_scaled_{self.scale}.mdl"\n'
            modelname_new_split = modelname_new.split(splitter, )
            modelname_new_path = f'$modelname "{self.new_path}\\{modelname_new_split[-1]}'
            return [modelname_new_path, y]
        else:
            print('\nNo $modelname in .qc file!\n')
            error = 1
            return error

    def write_new_qc(self):
        # writing and creating the new scaled .qc file
        if self.read_qc() == 1:
            return 1

        elif self.bbox() == 1:
            return 1

        elif self.model_name() == 1:
            return 1

        else:
            # write on document
            document = self.read_qc()
            document[1] = self.scale_line()
            document[self.bbox()[1]] = self.bbox()[0]
            document[self.model_name()[1]] = self.model_name()[0]

            # write as file
            with open(self.path_qc_new, 'w') as file:
                file.writelines(document)
                file.close()

    def compiling(self):
        # compiling the .qc file into .mdl (and other files used in source) with studiomdl
        with open(self.path_bat, 'w') as file:
            file.writelines(f'"{self.studiomdl}" -nop4 -game "{self.gamefolder}" "{self.path_qc_new}"')
            file.close()

        subprocess.call(self.path_bat)
        modelname = self.model_name()[0]
        new_model_location = f'{self.gamefolder}\\models\\{modelname[12:-1]}'
        print(f'\nNew model saved in: {new_model_location}\n')


print('\n---------------------'
      ' \nProp scaler by Hammer '
      '\n--------------------- \nType stop to stop the script \n')

stop_script = 0
while not(stop_script == 1):
    path_input = input('Path: ')
    new_path_input = input('New Folder (from /cstrike/models): ')
    g = 0
    if path_input == 'Stop' or path_input == 'stop':
        g = 1
        stop_script = 1
    while g != 1:
        name_input = input('Name: ')
        if name_input == 'Stop' or name_input == 'stop':
            g = 1
            stop_script = 1

        scale_input = input('Scale: ')
        if scale_input == 'Stop' or scale_input == 'stop':
            g = 1
            stop_script = 1

        else:
            input_user = prop_scaler(path_input, new_path_input, name_input, scale_input)
            f = input_user.write_new_qc()
            if f == 1:
                g = 1
            else:
               input_user.compiling()


input('\nPress enter to exit')
exit()
