import re

find_kill_time = re.compile(
    r'"time":(.*?),"type":"CHAT_MESSAGE_HERO_KILL","value":.*?,"player1":.*?,"player2":.*?'
)
find_damage = re.compile(
    r'{"time":.*?,"type":"DOTA_COMBATLOG_DAMAGE","value":.*?,"attackername":".*?","targetname":".*?_hero_.*?","sourcename":"npc_dota_hero_.*?","targetsourcename":".*?_hero_.*?","attackerhero":.*?,"targethero":true,"attackerillusion":.*?,"targetillusion":false,"inflictor":".*?"}'
)
get_damage_time = re.compile(r'.*?"time":(.*?),')
find_death = re.compile(
    r'"time":(.*?),"type":"DOTA_COMBATLOG_DEATH","value":.*?,"attackername":"npc_dota_.*?","targetname":"npc_dota_.*?","sourcename":"npc_dota_(.*?)_.*?","targetsourcename":"npc_dota_hero_.*?","attackerhero":.*?,"targethero":true,"attackerillusion":.*?,"targetillusion":false,'
)

flag = re.compile(r'"*.?"(flag)')

demo=input("请输入要解析的日志文件名:")
#获取英雄列表
hero_name = []
hero_chinese_name=[]
flags = 0
flags = int(flags)
nums = 10
nums = int(nums)
findplay_hero = re.compile(r'"time":1,"type":"interval","unit":"CDOTA_Unit_Hero_(.*?)",.*?"hero_id":(.*?),')     
get_times = re.compile(r'"time":(.*?),')
with open("%s"%demo, "r", encoding="utf-8") as fp:  #这里改成你要解析的日志文件的名字
    play_list = fp.readlines()
    for line in play_list:
        play_hero = re.findall(findplay_hero, line)
        if play_hero != []:
            num = play_list.index(line)
            gettime = re.findall(get_times, play_list[num])[0]
            gettime = int(gettime)
            while (gettime == (1) and (flags < nums)):
                if re.findall(findplay_hero, play_list[num]) != []:
                    play_hero_name = re.findall(findplay_hero, play_list[num])
                    shi=play_hero_name[0][1]
                    getChinese=re.compile('%s:(.*)\n'%shi,re.S)
                    hero_name.append(play_hero_name[0][0])
                    with open("英雄名.txt","r",encoding="utf-8") as f:
                        for lin in f.readlines():
                            if re.findall(getChinese,lin)!=[]:
                                hero_chinese_name.append(re.findall(getChinese,lin)[0])
                    flags = flags + 1
                num = num + 1
                gettime = re.findall(get_times, play_list[num])[0]
                gettime = int(gettime)
            break



#获取dreft_start所在位置
def get_strat():
    draft_start = re.compile(r'"time":.*?,"type":"draft_start"')
    with open("%s"%demo, "r", encoding="utf-8") as fp:  #这里改成你要解析的日志文件的名字
        list = fp.readlines()
        for i in list:
            if re.findall(draft_start, i) != []:
                start_num = list.index(i)
                return start_num



#获取每次击杀前30秒伤害记录
def findkill_damage():
    find_kill = re.compile(
        r'{"time":.*?,"type":"CHAT_MESSAGE_HERO_KILL","value":.*?,"player1":.*?,"player2":.*?}'
    )  #击杀信息搜寻规则
    fin_kill_name = re.compile(
        r'"time":.*?,"type":"CHAT_MESSAGE_HERO_KILL","value":.*?,"player1":(.*?),"player2":.*?',
        re.I)
    damage_data_list = []
    kill_list = []
    with open("%s"%demo, "r", encoding="utf-8"
              ) as fp:  #将所有击杀信息与伤害信息读取到kill_list列表中 #这里改成你要解析的日志文件的名字
        for line in fp.readlines():
            kill = re.findall(find_kill, line)
            damage = re.findall(find_damage, line)
            death = re.findall(find_death, line)
            if kill != []:
                kill_list.append(line)
            if damage != []:
                kill_list.append(line)
            if death != []:
                kill_list.append(line)
    for li in kill_list:  #遍历整个列表
        if re.findall(find_kill, li) != []:  #遍历到击杀信息时执行下面语句
            damage_data_list.append(li)  #将击杀语句添加到列表中
            get_time = re.findall(find_kill_time, li)[0]  #获得击杀的时间
            get_kill_name = re.findall(fin_kill_name, li)[0]  #获得被击杀英雄序号
            get_kill_name = int(get_kill_name)  #这行不知道有没有用，Python刚学不久，这行就这样留着吧
            killed_hero = hero_name[get_kill_name]  #获得被击杀英雄名字
            killed_hero = str(killed_hero)
            killed_hero = killed_hero[0:3]  #截取所获取到的英雄名字的前4个字符，因为日志文件里面的英雄名字格式不统一,比如说沙王在伤害语句中的为：sand_king，在状态语句中则为：Sandking，上面的hero_name 函数获取的是状态语句的名字
            get_damage = re.compile(r'"time":.*?,"type":"DOTA_COMBATLOG_DAMAGE","value":.*?,"attackername":".*?","targetname":"npc_dota_hero_.*?","sourcename":"npc_dota_hero_.*?","targetsourcename":"npc_dota_hero_%s.*?","attackerhero":.*?,"targethero":true,"attackerillusion":.*?,"targetillusion":false,.*?"'%killed_hero, re.I)
            get_damage_xiang = re.compile(r'"time":.*?,"type":"DOTA_COMBATLOG_DAMAGE","value":.*?,"attackername":".*?","targetname":"npc_dota_hero_.*?","sourcename":"npc_dota_hero_%s.*?","targetsourcename":"npc_dota_hero_%s.*?","attackerhero":.*?,"targethero":true,"attackerillusion":.*?,"targetillusion":false,.*?"'% (killed_hero, killed_hero), re.I)
            get_time = int(get_time)
            damage_time = get_time
            n = damage_data_list.index(li)  #击杀语句的所在位置
            num = kill_list.index(li)
            start_num = get_strat()
            num1 = num
            while damage_time >= (get_time - 30) and num > start_num:
                if (re.findall(get_damage, kill_list[num]) != []) and re.findall(flag, kill_list[num]) == [] and(re.findall(get_damage_xiang, kill_list[num]) == []):
                    damage_time = re.findall(get_damage_time,kill_list[num])[0]
                    damage_time = int(damage_time)
                    damage_data = re.findall(get_damage, kill_list[num])[0]
                    damage_data = str(damage_data) + "flag"  #flag是为了标记，因为有时候两个击杀的时间离得很近，会导致伤害语句重复捕获
                    kill_list[num] = damage_data
                    damage_data_list.append(damage_data)
                    damage_data_list.append("\n")
                num = num - 1
                damage_time = re.findall(get_damage_time, kill_list[num])[0]
                damage_time = int(damage_time)

            else:
                while (int(re.findall(get_damage_time, kill_list[num1])[0]) <=
                       (get_time + 1)):
                    if (re.findall(get_damage, kill_list[num1]) !=
                        []) and (re.findall(flag, kill_list[num1]) == []):
                        damage_data = re.findall(get_damage,
                                                 kill_list[num1])[0]
                        damage_data = str(damage_data) + "flag"
                        kill_list[num1] = damage_data
                        damage_data_list.append(damage_data)
                        damage_data_list.append("\n")
                    num1 = num1 + 1
                    if num1 == len(kill_list):
                        break
        if re.findall(find_death, li) != [] and int(
                re.findall(find_death, li)[0][0]) == get_time:  #判断最后一击是否是来自于玩家
            if str(re.findall(find_death, li)[0][1]) != "hero":
                li = li + "flag"
                damage_data_list[n] = li

    return damage_data_list  #返回每个击杀击杀语句及其前30秒所有的伤害语句


def death_damage(a_list):  #伤害语句分拣
    damage_data = a_list
    damage_value_list = []
    for j in range(0, 10):
        i = hero_name[j]
        i = str(i)
        i = i[0:3]  #截取所获取到的英雄名字的前4个字符
        findhero = re.compile(
            r'"time":.*?,"type":"DOTA_COMBATLOG_DAMAGE","value":(.*?),"attackername":".*?","targetname":".*?_hero_.*?","sourcename":"npc_dota_hero_%s.*?","targetsourcename":"npc_dota_hero_.*?","attackerhero":.*?,"targethero":true,"'
            % i, re.I)
        damage_value = 0
        for line in damage_data:
            death_data = re.findall(findhero, line)
            if death_data != []:
                death_data[0] = int(death_data[0])
                damage_value = damage_value + death_data[0]
        damage_value_list.append(damage_value)
    return damage_value_list  #返回一个包含10份伤害数据的列表


#判断谁是k头王
def k_tou_king(list):
    relist=[]
    ktou_num_list = {}
    ktoued_list={}
    for i in range(0,10):
            ktoued_list[i]=[]
    for i in range(10,20):
        ktou_num_list[i]=0
    for i in range(0, 10):
        ktou_num_list[i] = 0
    k_damage = list
    take_damage = re.compile(r'.*?"type":"DOTA_COMBATLOG_DAMAGE".*?'
                             )  #其实这个可以跟上面的find_damge合并的，但是得改好些语句，我有点犯困了，不改了。
    getkiller = re.compile(
        r'{"time":.*?,"type":"CHAT_MESSAGE_HERO_KILL","value":.*?,"player1":.*?,"player2":(.*?)}'
    )
    for line in k_damage:
        damager_list = []
        if re.findall(getkiller, line) != [] and re.findall(flag, line) == []:
            killer = int(re.findall(getkiller, line)[0])
            num = k_damage.index(line) + 1
            endnum = len(k_damage)
            while re.findall(find_kill_time,
                             k_damage[num]) == [] and num < endnum:
                if re.findall(get_damage_time, k_damage[num]) != []:
                    if re.findall(take_damage, k_damage[num]) != []:
                        damager_list.append(k_damage[num])
                num = num + 1
                if num == endnum:
                    break
            kill_damage = death_damage(damager_list)  #获取分拣后的伤害列表
            kill_damage.sort()  #将伤害由小到大排序
            killer_damage = death_damage(damager_list)  #在获取一份分拣后的伤害列表与排序后的作对比
            i = 0
            i = int(i)
            if killer_damage[killer]!=kill_damage[9]:
                ktou_num_list[killer_damage.index(max(killer_damage))+10]=ktou_num_list[killer_damage.index(max(killer_damage))+10]+1
                ktoued_list[killer_damage.index(max(killer_damage))].append(killer)
            while int(kill_damage[i]) == 0 and i < 10:
                if kill_damage[8] == 0:  #判断这次击杀是否为单杀
                    break
                if kill_damage[i + 1] == killer_damage[
                        killer]:  #排序后的伤害列表是这样的[0,0,0,0,0,2,3,4,5,6],[i+1]即为最小值,killer为击杀者的序号
                    ktou_num_list[killer] = ktou_num_list[killer] + 1
                    break
                i = i + 1
            relist.append(ktou_num_list)
            relist.append(ktoued_list)    
    return relist


def main():
    list = findkill_damage()
    a = death_damage(list)
    k = k_tou_king(list)
    for i in range(0, 10):
        get_hero = hero_chinese_name[i]
        print("%s打了:%s的致死伤害，k了%s个头,被k了%s个头" % (get_hero, a[i], k[0][i],k[0][i+10]),end=" ")
        for j in range(0,10):
            if k[1][i].count(j)!=0:
                print("%s k了%s个头"%(hero_chinese_name[j],k[1][i].count(j)),end=";")
        print("\n")        

main()