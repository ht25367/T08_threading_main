import threading
import time


def fnc_3(n):
	for i in range(n):
		print(f"fnc_3:（3s毎) {i+1}/{n}回")
		time.sleep(3)
	print("fnc_3: 終了")

def fnc_5(n):
	for i in range(n):
		print(f"　　　　　　　　　　　　　　　fnc_5: (5s毎) {i+1}/6回")
		time.sleep(5)
	print("　　　　　　　　　　　　　　　fnc_5: 終了")



def main():
	n = 7

	t1 = threading.Thread(target=fnc_3,args=(n,))
	t2 = threading.Thread(target=fnc_5,args=(6,))

	# スレッドスタート
	print("\nmain: スレッドスタート、前")
	t1.start()
	t2.start()
	print("\nmain: スレッドスタート、直後")

	time.sleep(10)
	print("\nmain: スレッドスタート、10秒後")


	print("main: 以下、スレッド終了を待機します。")
	t1.join()
	t2.join()
	print("\nmain: 全てのスレッドが終了しました。")



if __name__ == '__main__':
	main()
