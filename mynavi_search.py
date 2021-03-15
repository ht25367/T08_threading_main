import os
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
	# Chromeドライバーの読み込み
	options = ChromeOptions()
	
	# ヘッドレスモード（画面非表示モード）の設定
	if headless_flg == True:
		options.add_argument('--headless')

	# 起動オプションの設定
	options.add_argument(
		'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
	# options.add_argument('log-level=3')
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--ignore-ssl-errors')
	options.add_argument('--incognito')		  # シークレットモードの設定を付与
	return Chrome(ChromeDriverManager().install(), options=options)

# 「マイナビ」にて引数ワードで検索する関数
def set_keyword(keyword,queue):

	if os.name == 'nt': #Windows
		driver = set_driver("chromedriver.exe", False)
	elif os.name == 'posix': #Mac
		driver = set_driver("chromedriver", False)
	driver.get("https://tenshoku.mynavi.jp/")
	time.sleep(5)
	try:
		# ポップアップを閉じる
		driver.execute_script('document.querySelector(".karte-close").click()')
		time.sleep(5)
		driver.execute_script('document.querySelector(".karte-close").click()')
	except:
		pass
	
	# キーワードで検索
	driver.find_element_by_class_name("topSearch__text").send_keys(keyword)
	driver.find_element_by_class_name("topSearch__button").click()
	queue.put(driver)


# 指定したページのデータ(会社名・勤務地)を取得する関数
def get_elm(driver,page):

	#ページを移動
	url = driver.current_url
	i = url.find("/pg")
	# URLオプション「pg」が１ページ目にはない(.fintは-1)
	if i != -1:
		back_url = url[i+1:]
		j = back_url.find("/")
		driver.get( url[:i+3] + str(page) + back_url[j:] )
	else:
		i = url.find("/kw")
		back_url = url[i+1:]
		j = back_url.find("/")
		driver.get( url[:i+j+2] + "pg" + str(page) + back_url[j:] )
	time.sleep(5)

	# elementsを取得 tr[1仕事内容、2対象となる方、3勤務地、4給与、5初年度年収]
	name_elm = driver.find_elements_by_class_name("cassetteRecruit__name")
	office_elm=driver.find_elements_by_css_selector(".tableCondition tbody tr:nth-child(3) td")
	search_dict = {"page":[],"会社名":[],"勤務地":[]}
	for name,office in zip(name_elm,office_elm):
		search_dict["page"].append(page)
		search_dict["会社名"].append(name.text[:10])
		search_dict["勤務地"].append(office.text[:10])
	
	
	# csvファイル保存
	recruit_pd = pd.DataFrame(search_dict)
	recruit_pd.to_csv("t08_Recruit_data.csv",mode = "a",header=False,index=False)

	print(f"page:{page}, {len(name_elm)}件")

