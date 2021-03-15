
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
	drivers = []
	
	# 空ファイルを作成
	recruit_pd = pd.DataFrame({"page":[],"会社名":[],"勤務地":[]})
	recruit_pd.to_csv("t08_Recruit_data.csv",index=False)

	# keyword = input("検索ワードを入力して下さい:")
	keyword = "長野"

	# t_cnt = input("並列処理を行うスレッド数を入力して下さい:")
	t_cnt = 2

	for i in range(page):
		if i < t_cnt:
			#スレッド数上限まで、[スレッド/キュー/ドライバー]を用意＞リスト追加
			q = queue.Queue()
			t = threading.Thread(target=mynavi_search.set_keyword,args=(keyword,q,))
			t.start()
			ts.append(t)
			t.join()
			drivers.append(q.get())

		# 指定したページのデータ(会社名・勤務地)を取得するスレッド
		ts[i%t_cnt] = threading.Thread(target=mynavi_search.get_elm,args=(drivers[i%t_cnt],i+1,))
		ts[i%t_cnt].start()
	


	[t.join() for t in ts]

	#csvファイルをページ順に並び替える
	pd_data = pd.read_csv("t08_Recruit_data.csv")
	sort_data = pd_data.sort_values(by=["page"])
	pd_data = sort_data.reset_index(drop=True)
	pd_data.to_csv("t08_Recruit_data.csv")


if __name__ == "__main__":
	main()
