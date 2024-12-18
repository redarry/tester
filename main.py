import os
import json
import time
import psutil
import argparse
import colorama
import threading
import subprocess
import configparser        

class Test:
    def __init__(self, init_command: str, main_command: str, final_command: str, tests: dict, inf: str, outf: str, max_time=1,encoding='utf-8') -> None:
        self.init_command=init_command
        self.main_command=main_command
        self.final_command=final_command
        self.inf=inf
        self.outf=outf
        self.tests=tests
        self.max_time=max_time
        self.encoding=encoding

    def __test_program(self, command:str, input_data:str):
        self.output=None
        self.error=False
        with open(self.inf, 'w', encoding=self.encoding) as file:
            file.write(input_data)
        output=open(self.outf, 'w', encoding=self.encoding)
        start_time=time.time()
        try:
            process=subprocess.Popen(command.split(), universal_newlines=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=output)
            process.communicate(input=input_data, timeout=self.max_time)
            with open(self.outf, 'r', encoding=self.encoding) as file:
                self.output=file.read()
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as ex:
            print(ex)
            self.error=True
        self.time=time.time()-start_time

    def run_test(self) -> None:
        print('[*] preparation of the program')
        os.system(self.init_command)
        print('[*] processing of input data')
        max_test_name_len=0
        for i in self.tests:
            if len(i)>max_test_name_len:max_test_name_len=len(i)
        d='/-\\|/-\\|'
        for test_name, test in self.tests.items():
            thread=threading.Thread(target=self.__test_program, args=[self.main_command, test['input']])
            thread.start()
            start_time=time.time()
            last_str=f'{test_name}{" "*(max_test_name_len-len(test_name))} {d[0]}'
            print(last_str, end='')
            while thread.is_alive():
                new_str=f'{test_name}{" "*(max_test_name_len-len(test_name))} {d[int((time.time()-start_time)*10)%8]}'
                if new_str!=last_str: print('\r'+new_str, end='')
                last_str=new_str
            thread.join()

            if self.output==None: 
                if self.error: code=colorama.Back.RED+'[RE]'+colorama.Style.RESET_ALL
                else: code=colorama.Back.RED+'[TL]'+colorama.Style.RESET_ALL 
            elif (type(test['output'])==list and self.output.strip() in [data.strip() for data in test['output']]) or (type(test['output'])!=list and self.output.strip()==test['output'].strip()): code=colorama.Back.GREEN+'[OK]'+colorama.Style.RESET_ALL
            else: code=colorama.Back.RED+'[WA]'+colorama.Style.RESET_ALL

            run_time=str(self.time)[:4]
            if run_time[-1]=='.': run_time=' '+run_time[:-1]
            run_time+=' s.'
            if self.time>self.max_time: run_time=colorama.Fore.RED+run_time+colorama.Style.RESET_ALL
            else: run_time=colorama.Fore.GREEN+run_time+colorama.Style.RESET_ALL

            print(f'\r{test_name}{" "*(max_test_name_len-len(test_name))} | {run_time} | {code}')

        print('[*] completion of testing')
        os.remove(self.inf)
        os.remove(self.outf)
        os.system(self.final_command)

if __name__=='__main__':
    parser=argparse.ArgumentParser(prog='tester', description='this program performs automatic task testing')
    parser.add_argument('--time', type=float, default=1, help='maximum program execution time')
    parser.add_argument('--type', type=str, default='executable', help='type of program')
    parser.add_argument('-i', '--input-file', type=str, default='input.txt', help='input file')
    parser.add_argument('-o', '--output-file', type=str, default='output.txt', help='output file')
    parser.add_argument('--encoding', type=str, default='utf-8', help='encoding of input and output files')
    parser.add_argument('program', type=str, help='program for testing')
    parser.add_argument('tests', type=str, help='JSON file with tests')
    args = parser.parse_args()

    type_file=configparser.ConfigParser()
    program_path='/'.join(__file__.replace('\\', '/').split('/')[:-1])
    type_file.read(f"{program_path}/test_types/{args.type}.test")

    colorama.init()

    new_test=Test(type_file['Commands']['INIT_COMMAND'].replace('[file]', args.program),
              type_file['Commands']['MAIN_COMMAND'].replace('[file]', args.program), 
              type_file['Commands']['FINAL_COMMAND'].replace('[file]', args.program), 
              json.load(open(args.tests)), inf=args.input_file, outf=args.output_file,max_time=args.time, encoding=args.encoding)

    new_test.run_test()