import Simulated_Annealing

#run=Simulated_Annealing.My_Simulated_Annealing(alpha=0.98,step=3000,T_threshold=0.001,temperature=1000000)
run=Simulated_Annealing.My_Simulated_Annealing(alpha=0.9,step=1000,T_threshold=0.01,temperature=1000)
final_sequence,final_time=run.Annealing()
print(run.instance_name)
print(final_sequence,final_time)







#.......................我佛慈悲.....................7
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -卍-|||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#..................佛祖开光 ,永无BUG...................
