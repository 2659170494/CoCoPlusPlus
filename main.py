from urllib.request import urlopen
import os
import argparse
import json
import sys
import configparser

env_dist = os.environ

# 获取当前位置，这将判断程序是以exe形式运行还是py脚本运行
# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
else:
    application_path = input("获取当前程序（脚本）路径失败，请指定临时要工作（即当前程序(脚本)运行的路径）的绝对路径（这将决定您的程序和配置文件会放置在哪里！）：")
    print("配置指定成功，该路径为临时工作路径，但下次还可以继续被调用。请联系作者反馈该bug")

# 配置文件，可以更改默认配置文件
global_config_file = "cocopp_config.ini"
global_config_path = os.path.join(application_path, global_config_file)  # 为了防止意外，配置文件将保存在程序位置

if not os.path.exists(global_config_file):
    if global_config_file[len(global_config_file) - 4:len(global_config_file)] != ".ini":
        global_config_file += ".ini"
    with open(global_config_path, mode="w+") as global_config:
        global_config.write("""[apktool]
        name = ''
        [setting]
        gui = 0
        """)
    global_config = configparser.ConfigParser().read(global_config_file, encoding='utf-8')
else:
    global_config = configparser.ConfigParser().read(global_config_file, encoding='utf-8')


def Check_Lastet_Apktool(and_update=0):
    try:
        versions_url = "https://api.bitbucket.org/2.0/repositories/iBotPeaches/apktool/downloads"
        versions_result = urlopen(versions_url)
        versions_result_read = versions_result.read()
        versions_result_json = json.loads(versions_result_read)
        if versions_result_json[0]["name"] != global_config['apktool']['name']:
            if and_update != 0 or and_update != "0":
                if Download_Lastet_Apktool(versions_result_json):
                    return {"code":200,"data":{"check_apktool":True},"msg":"检查成功"}
            return {"code":200,"data":{"check_apktool":False},"msg":"检查失败"}
        return {"code":200,"data":{"check_apktool":True},"msg":"检查成功"}
    except BaseException as error:
        print(f"发生错误:{str(error)}")
        return {"code":500,"data":{},"msg":f"发生错误:{str(error)}"}


def Download_Lastet_Apktool(versions_result_json=None):
    try:
        print("开始下载新版apktool")
        if versions_result_json is None:
            versions_url = "https://api.bitbucket.org/2.0/repositories/iBotPeaches/apktool/downloads"
            versions_result = urlopen(versions_url)
            versions_result_read = versions_result.read()
            versions_result_json = json.loads(versions_result_read)
        print("正在下载apktool")
        download_url = versions_result_json['values'][0]["links"]["self"]["href"]
        download_result = urlopen(download_url)
        download_result_read = download_result.read()
        with open(global_config_path+"/"+versions_result_json['values'][0]["name"],mode="w+") as download_file:
            download_file.write(download_result_read)
        print("下载apktool完毕")
        return {"code":200,"data":{"file_path":global_config_path+"/"+versions_result_json['values'][0]["name"]},"msg":"下载apktool完毕"}
    except BaseException as error:
        print(f"发生错误:{str(error)}")
        return {"code":500,"data":{},"msg":f"发生错误:{str(error)}"}

def check_java(java_arg=None):
    if java_arg != "":
        java_path = java_arg
        print("JAVA_HOME将为"+java_path)
    else:
        # 打印所有环境变量，遍历字典
        if 'JAVA_HOME' not in env_dist:
            print('JAVA_HOME 未指定，开始遍历PATH的java路径')
            path_list = env_dist["PATH"].split(";")
            for java_file in path_list:
                if java_file[len(java_file)-1:len(java_file)] == r"\\" or java_file[len(java_file)-1:len(java_file)] == "/":
                    java_file = java_file[0:len(java_file)-1]
                if os.path.exists(java_file+"\\bin\\java"):
                    java_path = java_file+"\\bin\\java"
                    print("JAVA_HOME将为"+java_path)
                    break
                elif os.path.exists(java_file+"\\java"):
                    java_path = java_file+"\\java"
                    print("JAVA_HOME将为"+java_path)
                    break
                elif os.path.exists(java_file+"\\bin\\java.exe"):
                    java_path = java_file+"\\bin\\java.exe"
                    print("JAVA_HOME将为"+java_path)
                    break
                elif os.path.exists(java_file+"\\java.exe"):
                    java_path = java_file+"\\java.exe"
                    print("JAVA_HOME将为"+java_path)
                    break
            print("PATH中未找到JAVA,请手动指定")
            exit()
        else:
            java_file = env_dist['JAVA_HOME']
            if java_file[len(java_file)-1:len(java_file)] == r"\\" or java_file[len(java_file)-1:len(java_file)] == "/":
                    java_file = java_file[0:len(java_file)-1]
            if os.path.exists(java_file+"\\bin\\java"):
                java_path = java_file+"\\bin\\java"
                print("JAVA_HOME将为"+java_path)
            elif os.path.exists(java_file+"\\java"):
                java_path = java_file+"\\java"
                print("JAVA_HOME将为"+java_path)
            elif os.path.exists(java_file+"\\bin\\java.exe"):
                java_path = java_file+"\\bin\\java.exe"
                print("JAVA_HOME将为"+java_path)
            elif os.path.exists(java_file+"\\java.exe"):
                java_path = java_file+"\\java.exe"
                print("JAVA_HOME将为"+java_path)
            else:
                print("PATH中未找到JAVA,请手动指定")
                exit()

#Download_Lastet_Apktool()

parser = argparse.ArgumentParser(description="""_________        _________                                 
\_   ___ \  ____ \_   ___ \  ____      .__         .__     
/    \  \/ /  _ \/    \  \/ /  _ \   __|  |___   __|  |___ 
\     \___(  <_> )     \___(  <_> ) /__    __/  /__    __/ 
 \______  /\____/ \______  /\____/     |__|        |__|    
        \/               \/                                
          """+'\nA tool for Codemao CoCo', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--options', '-O', help='选项按钮，必要参数。\n OPTIONS为D则反编译、OPTIONS为B则回编译', required=True)
parser.add_argument('--input', '-i', help='输入文件路径，必要参数，\n INPUT为需要处理的文件的绝对路径', required=True)
parser.add_argument('--apktool', '-apktool', help='apktool路径，非必要参数\n APKTOOL可指定apktool的文件路径，留空则自动下载', required=False)
parser.add_argument('--java', '-java', help='java路径，非必要参数\n JAVA可指定java的文件路径，留空则自动查找，若查找失败则需指定', required=False, default="")
args = parser.parse_args()


def Decompile_CoCo_Apk():
    pass


if __name__ == "__main__":
    print(f"用户输入的参数为{args.options}、{args.input}、{args.apktool}、{args.java}")
    