# -*- coding:utf-8 -*-
#author:dengxiangyu
#date:2017-08-11

# 描述:
# V1 WZJ 2016-12-20
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

# 用来加载解析yaml文件或JSON内容,并且支持vault的解密
loader = DataLoader()
    
# 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
variable_manager = VariableManager()

# 根据inventory加载对应变量,此处host_list参数可以有两种格式：
# 1: hosts文件(需要),
# 2: 可以是IP列表,此处使用IP列表
inventory = Inventory(loader=loader, variable_manager=variable_manager,host_list=['192.168.187.189'])
variable_manager.set_inventory(inventory)

# 设置密码,需要是dict类型
passwords=dict(conn_pass='your password')

# 初始化需要的对象
Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass', 
                      'module_path', 
                      'forks', 
                      'become', 
                      'become_method', 
                      'become_user', 
                      'check',
                      'listhosts', 
                      'listtasks', 
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo'])
# 初始化需要的对象
options = Options(connection='smart', 
                       remote_user='root',
                       ack_pass=None,
                       sudo_user='root',
                       forks=5,
                       sudo='yes',
                       ask_sudo_pass=False,
                       verbosity=5,
                       module_path=None,  
                       become=True, 
                       become_method='sudo', 
                       become_user='root', 
                       check=None,
                       listhosts=None,
                       listtasks=None, 
                       listtags=None, 
                       syntax=None)

# playbooks就填写yml文件即可,可以有多个,以列表形式
playbook = PlaybookExecutor(playbooks=['/Users/dengxiangyu/dengxiangyu/flask/op_platform/app/ansible/deploy_mysql.yml'],inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,options=options,passwords=passwords)
# 开始执行
def playbook_run():
    playbook.run()
