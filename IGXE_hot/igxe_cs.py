import threading
import datetime
import re
import requests
import json
from lxml import etree
from xlutils import copy
import xlwt
import xlrd



all_href_list = []


def get_all_product_url():
    """获取所有商品url"""
    # https://www.igxe.cn/csgo/730?is_buying=0&price_from=10&price_to=500&page_no=1&page_size=200&_t=1562039824177
    all_url = requests.get("https://www.igxe.cn/csgo/730?is_buying=0&price_from=10&price_to=500&page_no=1&page_size=200&_t=1562039824177")
    html_index = etree.HTML(all_url.content)
    href_list = html_index.xpath('//*[@id="center"]/div/div[3]/div/div[2]/a/@href')
    for href in href_list:
        dict_pro = {}
        href_num = href.replace("/product/730/", "")
        # https://www.igxe.cn/product/730/3955
        name_num_url = "https://www.igxe.cn/product/730/%s"%href_num
        # https://www.igxe.cn/product/trade/730/3760
        on_sale__url = "https://www.igxe.cn/product/trade/730/%s" % href_num
        # https://www.igxe.cn/purchase/get_product_purchases?product_id=3760
        want_to_buy_url = "https://www.igxe.cn/purchase/get_product_purchases?product_id=%s"%href_num
        # https://www.igxe.cn/product/get_product_sales_history/730/3760
        historical_sale_url = "https://www.igxe.cn/product/get_product_sales_history/730/%s"%href_num
        dict_pro["name"] = name_num_url
        dict_pro["num"] = name_num_url
        dict_pro["on_sale_url"] = on_sale__url
        dict_pro["want_to_buy_url"] = want_to_buy_url
        dict_pro["historical_sale_url"] = historical_sale_url
        # all_on_sale_url_list.append(on_sale__url)
        # all_want_to_buy_url.append(want_to_buy_url)
        # all_historical_sale_url.append(historical_sale_url)
    # print(len(all_on_sale_url_list),all_want_to_buy_url,all_historical_sale_url)
        all_href_list.append(dict_pro)
    print(all_href_list)


def get_name_num(url):
    name_num_list = []
    c_product = requests.get(url)
    html = etree.HTML(c_product.content)
    name = html.xpath('//*[@id="id-box4-vue"]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/text()')[0]
    num = html.xpath('//*[@id="id-box4-vue"]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/text()')[1]
    num = num.replace("：","").replace("\n                                        ","").replace("件","")
    name_num_list.append(name)
    name_num_list.append(num)
    return name_num_list


def on_sale(url):
    on_sale_price_list = []
    c_trade = requests.get(url).content
    s_trade = json.loads(c_trade)
    for i in s_trade["d_list"]:
        on_sale_price_list.append(i["unit_price"])
        # print(i["unit_price"])
    return on_sale_price_list


def want_to_buy(url):
    want_to_buy_price_list = []
    # want_to_buy_time_list = []
    c_want_to_buy = requests.get(url).content
    s_want_to_buy = json.loads(c_want_to_buy)
    # for i in s_want_to_buy["datas"]["datas"]:
    #     # want_to_buy_time_list.append(i["date_created"])
    #     want_to_buy_price_list.append(i["unit_price"])
    #     # print(i["unit_price"])
    want_to_buy_price = s_want_to_buy["datas"]["datas"][0]["unit_price"]
    want_to_buy_price_list.append(want_to_buy_price)
    print(want_to_buy_price_list)
    # time_price_tuple = zip(want_to_buy_time_list,want_to_buy_price_list)
    return want_to_buy_price_list


def historical_sale(url):
    historical_sale_price_list = []
    historical_sale_time_list = []
    c_history = requests.get(url).content
    s_history = json.loads(c_history)
    for i in s_history["data"]:
        historical_sale_time_list.append(i["last_updated"])
        historical_sale_price_list.append(i["unit_price"])
        # print(i["unit_price"])
    time_price_tuple = zip(historical_sale_time_list,historical_sale_price_list)
    return time_price_tuple


def xlwt_f(data_list):
    # 1.创建 Workbook
    wb = xlwt.Workbook()
    # 2.创建 worksheet
    ws = wb.add_sheet('igxe_sheet')
    # 3.写入第一行内容  ws.write(a, b, c)  a：行，b：列，c：内容
    # ws.write(0, 0, '商品')
    # ws.write(0, 1, '件数')
    # ws.write(0, 2, '正在销售1')
    # ws.write(0, 3, '正在销售2')
    # ws.write(0, 4, '正在销售3')
    # ws.write(0, 5, '正在销售4')
    # ws.write(0, 6, '正在销售5')
    # ws.write(0, 7, '正在销售6')
    # ws.write(0, 8, '正在销售7')
    # ws.write(0, 9, '正在销售8')
    # ws.write(0, 10, '正在销售9')
    # ws.write(0, 11, '正在销售10')
    # ws.write(0, 12, '历史销售1')
    # ws.write(0, 13, '历史销售2')
    # ws.write(0, 14, '历史销售3')
    # ws.write(0, 15, '历史销售4')
    # ws.write(0, 16, '历史销售5')
    # ws.write(0, 17, '历史销售6')
    # ws.write(0, 18, '历史销售7')
    # ws.write(0, 19, '历史销售8')
    # ws.write(0, 20, '历史销售9')
    # ws.write(0, 21, '历史销售10')
    # ws.write(0, 22, '求购1')
    # ws.write(0, 23, '求购2')
    # ws.write(0, 24, '求购3')
    # ws.write(0, 25, '求购4')
    # ws.write(0, 26, '求购5')
    # ws.write(0, 27, '求购6')


    # wb.save('./myExcel.xls')
    # [[["商品","件数","正在销售价格","求购","差价","历史时间","历史价格"],["AK-47",123,123,120,3...]],
    # [["商品","件数","正在销售价格","求购","差价","历史时间","历史价格"],["AK-47",123,123,120,3...]]]
    for i, item in enumerate(data_list):
        ws.write(i , 0, item[0])
        ws.write(i , 1, item[1])
        ws.write(i , 2, item[2])
        ws.write(i , 3, item[3])
        ws.write(i , 4, item[4])
        ws.write(i , 5, item[5])
        ws.write(i , 6, item[6])
        # ws.write(i + 1, 7, item[7])
        # ws.write(i + 1, 8, item[8])
        # ws.write(i + 1, 9, item[9])
        # ws.write(i + 1, 10, item[10])
        # ws.write(i + 1, 11, item[11])
        # ws.write(i + 1, 12, item[12])
        # ws.write(i + 1, 13, item[13])
        # ws.write(i + 1, 14, item[14])
        # ws.write(i + 1, 15, item[15])
        # ws.write(i + 1, 16, item[16])
        # ws.write(i + 1, 17, item[17])
        # ws.write(i + 1, 18, item[18])
        # ws.write(i + 1, 19, item[19])
        # ws.write(i + 1, 20, item[20])
        # ws.write(i + 1, 21, item[21])
        # ws.write(i + 1, 22, item[22])
        # ws.write(i + 1, 23, item[23])
        # ws.write(i + 1, 24, item[24])
        # ws.write(i + 1, 25, item[25])
        # ws.write(i + 1, 26, item[26])
        # ws.write(i + 1, 27, item[27])
    wb.save('./myExcel.xls')


def data_analysis():
    pass


def xls(res_list):
    excel_path = './test.xls'  # 文件路径
    # excel_path=unicode('D:\\测试.xls','utf-8')#识别中文路径
    rbook = xlrd.open_workbook(excel_path, formatting_info=True)  # 打开文件
    wbook = copy.copy(rbook)  # 复制文件并保留格式
    w_sheet = wbook.get_sheet(0)  # 索引sheet表
    row = 1
    col = 1
    value = 20180803
    w_sheet.write(row, col, value)
    wbook.save(excel_path)  # 保存文件


def main(href_list):
    global res_list
    count = 0
    for i in href_list:
        # print(res_list)
        data_lists = [["商品","件数","正在销售价格","求购","差价","历史时间","历史价格"]]
        name_num_url = i["name"]
        on_sale_url = i["on_sale_url"]
        want_to_buy_url = i["want_to_buy_url"]
        historical_sale_url = i["historical_sale_url"]
        name_num_list = get_name_num(name_num_url)
        num = int(name_num_list[1])
        if num < 10:
            continue
        on_sale_price_list = on_sale(on_sale_url)
        want_to_buy_price_list = want_to_buy(want_to_buy_url)
        time_price_list = list(historical_sale(historical_sale_url))
        for i in range(0,10):
            data_list = []
            data_list.append(name_num_list[0])
            data_list.append(num)
            on_sale_price = float(on_sale_price_list[i])
            want_to_buy_price = float(want_to_buy_price_list[0])
            data_list.append(on_sale_price)
            data_list.append(want_to_buy_price)
            data_list.append(on_sale_price - want_to_buy_price)
            data_list.append(time_price_list[i][0])
            data_list.append(time_price_list[i][1])
            data_lists.append(data_list)
        res_list = res_list + data_lists
        # res = name_num_list+on_sale_price_list+time_price_list+want_to_buy_price_list
        #
        # if len(res) == 28:
        #     pass
        # else:
        #     e_list = []
        #     e = 28-len(res)
        #     print(e)
        #     for ll in range(0,e):
        #         e_list.append("空")
        #     res = res+e_list
        # res_list.append(res)
        count += 1
        print(count)


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    get_all_product_url()
    res_list = []
    href_list_1 = all_href_list[0:20]
    href_list_2 = all_href_list[20:40]
    href_list_3 = all_href_list[40:60]
    href_list_4 = all_href_list[60:80]
    href_list_5 = all_href_list[80:100]
    href_list_6 = all_href_list[100:120]
    href_list_7 = all_href_list[120:140]
    href_list_8 = all_href_list[140:160]
    href_list_9 = all_href_list[160:180]
    href_list_10 = all_href_list[180:200]

    t_1 = threading.Thread(target=main, args=(href_list_1,))
    t_2 = threading.Thread(target=main, args=(href_list_2,))
    t_3 = threading.Thread(target=main, args=(href_list_3,))
    t_4 = threading.Thread(target=main, args=(href_list_4,))
    t_5 = threading.Thread(target=main, args=(href_list_5,))
    t_6 = threading.Thread(target=main, args=(href_list_6,))
    t_7 = threading.Thread(target=main, args=(href_list_7,))
    t_8 = threading.Thread(target=main, args=(href_list_8,))
    t_9 = threading.Thread(target=main, args=(href_list_9,))
    t_10 = threading.Thread(target=main, args=(href_list_10,))

    t_1.start()
    t_2.start()
    t_3.start()
    t_4.start()
    t_5.start()
    t_6.start()
    t_7.start()
    t_8.start()
    t_9.start()
    t_10.start()

    t_1.join()
    t_2.join()
    t_3.join()
    t_4.join()
    t_5.join()
    t_6.join()
    t_7.join()
    t_8.join()
    t_9.join()
    t_10.join()

    xlwt_f(res_list)
    # xls(res_list)
    endtime = datetime.datetime.now()
    print("共耗时(秒)⬇")
    print((endtime - starttime).seconds)

    # on_sale()


