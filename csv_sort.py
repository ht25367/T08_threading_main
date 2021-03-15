import pandas as pd


def main():

	#ファイルを開く"t08_Recruit_data.csv"
	pd_data = pd.read_csv('t08_Recruit_data.csv',dtype={'page':int})
	
	#パンダスでソートする
	pd_data.sort_values(by=['page'],ascending=False)

	#ファイルに保存する"t08_Recruit_sort.csv"
	pd_data.to_csv("t08_Recruit_sort.csv")




if __name__ == "__main__":
	main()