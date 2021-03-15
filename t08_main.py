
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
import mynavi_search
import threading
import time
import queue


# main処理
def main():
	page = 12
	ts = []
	qs = []
	drivers = []
	
	# 空ファイルを作成
	recruit_pd = pd.DataFrame({"page":[],"会社名":[],"勤務地":[]})
	recruit_pd.to_csv("t08_Recruit_data.csv")

	# keyword = input("検索ワードを入力して下さい:")
	keyword = "長野"

	# t_cnt = input("並列処理を行うスレッド数を入力して下さい:")
	t_cnt = 1


	for i in range(page):
		if i < t_cnt:
			#スレッド数上限まで、[スレッド/キュー/ドライバー]を用意＞リスト追加
			q = queue.Queue()
			t = threading.Thread(target=mynavi_search.set_keyword,args=(keyword,q,))
			t.start()
			qs.append(q)
			ts.append(t)
			t.join()
			drivers.append(q.get())

		# 指定したページのデータ(会社名・勤務地)を取得するスレッド
		ts[i%t_cnt] = threading.Thread(target=mynavi_search.get_elm,args=(drivers[i%t_cnt],i+1,qs[i%t_cnt],))
		ts[i%t_cnt].start()
		# ts[i%t_cnt].join()
		# search_elm = qs[i%t_cnt].get()
		# for name,office in zip(search_elm["name"],search_elm["office"]):
		# 	search_dict["page"].append(i+1)
		# 	search_dict["会社名"].append(name.text[:10])
		# 	search_dict["勤務地"].append(office.text[:10])

	
	# csvファイル保存
	# file_name = "t08_Recruit_data.csv"
	# recruit_pd = pd.DataFrame(search_dict)
	# recruit_pd.to_csv(file_name)
	# print(f"{len(search_dict['会社名'])}件のデータを{file_name}に保存しました。")




if __name__ == "__main__":
	main()
