# -*- coding: UTF-8 -*-
import sys
from shopify_requests import Monitor, SecKill

if __name__ == '__main__':
    a = """

 __     ___    _        _____ ______ _____ _  _______ _      _      
 \ \   / / |  | |      / ____|  ____/ ____| |/ /_   _| |    | |     
  \ \_/ /| |  | |_____| (___ | |__ | |    | ' /  | | | |    | |     
   \   / | |  | |______\___ \|  __|| |    |  <   | | | |    | |     
    | |  | |__| |      ____) | |___| |____| . \ _| |_| |____| |____ 
    |_|   \____/      |_____/|______\_____|_|\_\_____|______|______|
                                                                    
                                                                                                                                                                                                                                                          
功能列表：                                                                                
 1.监控商品上架
 2.秒杀抢购商品
    """
    print(a)

    choice_function = input('请选择:')
    if choice_function == '1':
        Monitor().scrape()
    elif choice_function == '2':
        SecKill().seckill_by_selenium()
    else:
        print('没有此功能')
        sys.exit(1)
