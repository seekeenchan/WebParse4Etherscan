# Written By SHIJIAN CHEN 2022
'''
A FEW THINGS NEED TO BE NOTICED:
    Pool name is not recorded
    * ：Before Ethereum London Upgrade (p.s. Ethereum London Upgrade Starts from block 12,965,000 on August 5th, 2021)
    example:  Block #15320859
    0  Block Height: 15320859
    1  Timestamp: 1 hr 14 mins ago (Aug-11-2022 01:00:02 PM +UTC)
    2  Transactions: 461 transactions and 122 contract internal transactions in this block
    3  Mined by: 0x1ad91ee08f21be3de0ba2ba6918e714da6b45836 (Hiveon Pool) in 9 secs
    4  Block Reward: 2.240093675723923609 Ether (2 + 0.661713528696666943 - 0.421619852972743334)
    5  Uncles Reward: 0
    6  Difficulty: 12,136,278,927,982,619
    7  Total Difficulty: 56,115,277,296,070,223,283,810
    8  Size: 132,554 bytes
    9  Gas Used: 29,993,054 (99.98%) +100% Gas Target
    10  Gas Limit: 29,999,972
    11  *  Base Fee Per Gas: 0.000000014057249821 Ether (14.057249821 Gwei)
    12  *  Burnt Fees: 🔥 0.421619852972743334 Ether
    13  Extra Data: Hiveon sg-heavy-qtu (Hex:0x486976656f6e2073672d68656176792d717475)
    14  Hash: 0xd71c1bede2431deace7c0008df9cf7e63dc96fd320bd019833cbddd1e3d7ac75
    15  Parent Hash: 0x13de3ca34eca4ff70e57c96dc7760310535922917d52bbcc48353ffa083ce8bd
    16  Sha3Uncles: 0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347
    17  StateRoot: 0x889a447f3da4e9e8b0ae5528e060edc995ee7ab4ea433b9bfd42d4066ba4e2a2
    18  Nonce: 0x9f828113b43d24da
'''

import requests
import logging
import re
import calendar
from bs4 import BeautifulSoup
import time
import pandas as pd

def not_empty(s):
  return s and s.strip()


def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())


initBlock=15338100
newestBlock=15338130



logging.captureWarnings(True)
blockIndex=list(range(initBlock,newestBlock))
url=[];blockHtml=[]
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
basicUrl="https://cn.etherscan.com/block/"
BlockHeight=[];Timestamp=[];Transactions=[];InternalTransactions=[];MinerAddr=[];BlockInterval=[];
BlockReward=[];UnclesReward=[];Difficulty=[];TotalDifficulty=[];Size=[];UnclesNum=[];
GasUsed=[];GasUsedRate=[];GasTargetRate=[];GasLimit=[];
BaseFeePerGasEther=[];BaseFeePerGasGwei=[];BurntFeesEther=[];
ExtraData=[];ExtraDataHex=[];Hash=[];ParentHash=[];Sha3Uncles=[];
StateRoot=[];Nonce=[];
StaticBlockReward=[];TxnFees=[];BurntFees=[];

for eachBlock in blockIndex:
    url.append(basicUrl+str(eachBlock))
    try:
        tempBlockHtml=requests.get(url[-1],headers=headers)
        blockHtml.append(tempBlockHtml)
        print('OK at urlGet')
    except Exception as e:
        blockHtml.append(["requestError"])
        print('Error at urlGet')

for i in range(initBlock,newestBlock):

    BlockHeight.append(i);
    print('Block: ',i, '----Start----')

    soupText = BeautifulSoup(blockHtml[i - initBlock].text, 'lxml')
    soupText = soupText.get_text()
    soupText = soupText.split("\n")
    list_soupText = list(filter(not_empty, soupText))
    print(list_soupText)

    if (blockHtml[i-initBlock]=="requestError") or ('Sorry, our servers are currently busy' in list_soupText):
        Timestamp.append("requestError");
        Transactions.append("requestError");
        MinerAddr.append("requestError");
        BlockInterval.append("requestError");
        BlockReward.append("requestError");
        UnclesReward.append("requestError");
        Difficulty.append("requestError");
        TotalDifficulty.append("requestError");
        Size.append("requestError");
        GasUsed.append("requestError");
        GasUsedRate.append("requestError");
        GasTargetRate.append("requestError");
        GasLimit.append("requestError");
        BaseFeePerGasEther.append("requestError");
        BaseFeePerGasGwei.append("requestError");
        BurntFeesEther.append("requestError");
        ExtraData.append("requestError");
        ExtraDataHex.append("requestError");
        Hash.append("requestError");
        ParentHash.append("requestError");
        Sha3Uncles.append("requestError");
        StateRoot.append("requestError");
        Nonce.append("requestError");
        StaticBlockReward.append("requestError")
        TxnFees.append("requestError")
        BurntFees.append("requestError")
        UnclesNum.append("requestError")
        InternalTransactions.append("requestError")
        continue
    else:

        # Nonce
        indexNonce=list_soupText.index(" Nonce:")+1
        Nonce.append(list_soupText[indexNonce])

        # StateRoot
        indexStateRoot=list_soupText.index(" StateRoot:")+1
        StateRoot.append(list_soupText[indexStateRoot])

        # Sha3Uncles
        indexSha3Uncles=list_soupText.index(" Sha3Uncles:")+1
        Sha3Uncles.append(list_soupText[indexSha3Uncles])

        # ParentHash
        indexParentHash=list_soupText.index(" Parent Hash:")+1
        ParentHash.append(list_soupText[indexParentHash])

        # Hash
        indexHash=list_soupText.index(" Hash:")+1
        Hash.append(list_soupText[indexHash])

        # ExtraData & ExtraDataHex
        indexExtraData=list_soupText.index(" Extra Data:")+1
        if list_soupText[indexExtraData+1]=='Hash':
            ExtraData.append(list_soupText[indexExtraData].split('(Hex')[0])
            ExtraDataHex.append(list_soupText[indexExtraData].split(')')[-2].split(':')[-1])
        else:
            strExtraData=list_soupText[indexExtraData]+list_soupText[indexExtraData+1]
            ExtraData.append(strExtraData.split('(Hex')[0])
            ExtraDataHex.append(strExtraData.split(')')[-2].split(':')[-1])

        # Difficulty
        indexDifficulty=list_soupText.index(" Difficulty:")+1
        Difficulty.append(list_soupText[indexDifficulty].replace(',',''))

        # Total Difficulty
        indexTotalDifficulty=list_soupText.index(" Total Difficulty:")+1
        TotalDifficulty.append(list_soupText[indexTotalDifficulty].replace(',',''))

        # Timestamp
        indexTimestamp=list_soupText.index(" Timestamp:")+1
        strTimes=list_soupText[indexTimestamp]
        strTimes=remove_upprintable_chars(strTimes)
        p1=re.compile(r'[(](.*?)[)]',re.S)
        timeAll=str(re.findall(p1,strTimes))
        month=timeAll.split("-")[0].split("'")[1]
        month=str(list(calendar.month_abbr).index(month))
        day=timeAll.split("-")[1]
        year=timeAll.split("-")[2].split(" ")[0]
        hour=timeAll.split("-")[2].split(" ")[1].split(":")[0]
        minute=timeAll.split("-")[2].split(" ")[1].split(":")[1]
        second=timeAll.split("-")[2].split(" ")[1].split(":")[2]
        timeFormat=str(year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second)
        timeArray=time.strptime(timeFormat,"%Y-%m-%d %H:%M:%S")
        timeStamp_=int(time.mktime(timeArray))
        Timestamp.append(timeStamp_)

        # Transactions & InternalTransactions
        indexTransactions=list_soupText.index(" Transactions:")+1
        strTransactions=list_soupText[indexTransactions]
        strTransactions=remove_upprintable_chars(strTransactions)
        splitTransactions=re.findall("\d+\.?\d*",strTransactions)
        InternalTransactions.append(splitTransactions[1])
        Transactions.append(splitTransactions[0])


        # MinerAddr BlockInterval
        indexMine=list_soupText.index(" Mined by:")+1
        strMine=list_soupText[indexMine]
        strMine=remove_upprintable_chars(strMine)
        MinerAddr.append(strMine.split(" ")[0])
        tempSoup=BeautifulSoup(blockHtml[i-initBlock].text,'lxml')
        strSoup=str(tempSoup.findAll(text=re.compile("secs")))
        BlockInterval.append(re.findall("\d+\.?\d*",strSoup)[0])

        # Block Reward & StaticBlockReward & TxnFees & BurntFees
        indexBlockReward=list_soupText.index(" Block Reward:")+1
        strBlockReward=list_soupText[indexBlockReward]
        strBlockReward=remove_upprintable_chars(strBlockReward)
        BlockReward.append(strBlockReward.split(" ")[0])

        if ('(' in strBlockReward) and (')' in strBlockReward):
            StaticBlockReward.append(strBlockReward.split('(')[1].split(" ")[0])
            TxnFees.append(strBlockReward.split("(")[1].split("+")[1].split(" ")[1].split(" ")[0])
            if '-' in strBlockReward:
                BurntFees.append(strBlockReward.split('-')[1].split(' ')[1].split(')')[0])
            else:
                BurntFees.append('0')
        else:
            StaticBlockReward.append('0')
            TxnFees.append('0')
            BurntFees.append('0')


        # UncleReward & UnclesNum
        indexUncleReward=list_soupText.index(" Uncles Reward:")+1
        strUncleReward=list_soupText[indexUncleReward]
        strUncleReward=remove_upprintable_chars(strUncleReward)
        print(i,strUncleReward)
        if strUncleReward=='0':
            UnclesReward.append('0')
            UnclesNum.append('0')
        else:
            UnclesReward.append(strUncleReward.split(" ")[0])
            UnclesNum.append(strUncleReward.split("(")[1].split(" ")[0])

        # Size
        indexSize=list_soupText.index(" Size:")+1
        strSize=list_soupText[indexSize].split(" ")[0].replace(',','')
        Size.append(strSize)
        #print(Size)

        #  Gas Limit
        indexGasLimit=list_soupText.index(" Gas Limit:")+1
        GasLimit.append(list_soupText[indexGasLimit].replace(',',''))
        #print(Size)

        #  GasUsed & GasUsedRate & GasTargetRate
#        if i>=12965000:
#            soup=BeautifulSoup(blockHtml[i-initBlock].text,'lxml')
#            strGasTarget=str(soup.select('script')[-20].get_text())
#            print(strGasTarget)
#            strGasTarget=strGasTarget.split('\n')
#            GasTarget=int(re.findall(r"\d+\.?\d*",strGasTarget[2])[0])
#            if strGasTarget[2].find('-')!=-1:
#                GasTarget*=(-1)
#            GasTargetRate.append(GasTarget)
#        else:
        GasTargetRate.append("0")

        indexGasUsed=list_soupText.index(" Gas Used:")+1
        strGasUsed=list_soupText[indexGasUsed].replace(',','')
        GasUsed.append(strGasUsed.split(" ")[0])
        Rate='0.'+strGasUsed.split("(")[1].split("%")[0].replace('.', '')
        GasUsedRate.append(Rate)

        # BaseFeePerGasEther & BaseFeePerGasGwei & BurntFeesEther
        if i>=12965000:
            indexBaseFees=list_soupText.index(" Gas Limit:")+2
            strBaseFees=list_soupText[indexBaseFees]
            strBaseFeesRemove=remove_upprintable_chars(strBaseFees)
            k=re.findall(r"\d+\.?\d*",strBaseFeesRemove)
            BaseFeePerGasEther.append(k[0])
            BaseFeePerGasGwei.append(k[1])
            BurntFeesEther.append(k[2])


        print('Block: ',i, '----END----')

dict_={'BlockHeight':BlockHeight,
      'Timestamp':Timestamp,
      'Transactions': Transactions,
      'InternalTransactions': InternalTransactions,
      'MinerAddr': MinerAddr,
      'BlockInterval': BlockInterval,
      'BlockReward': BlockReward,
      'UnclesReward': UnclesReward,
      'Difficulty': Difficulty,
      'TotalDifficulty': TotalDifficulty,
      'Size': Size,
      'UnclesNum': UnclesNum,
      'GasUsed': GasUsed,
      'GasUsedRate': GasUsedRate,
      'GasTargetRate': GasTargetRate,
      'GasLimit': GasLimit,
      'BaseFeePerGasEther': BaseFeePerGasEther,
      'BaseFeePerGasGwei': BaseFeePerGasGwei,
      'BurntFeesEther': BurntFeesEther,
      'ExtraData': ExtraData,
      'ExtraDataHex': ExtraDataHex,
      'Hash': Hash,
      'ParentHash': ParentHash,
      'Sha3Uncles': Sha3Uncles,
      'StateRoot': StateRoot,
      'Nonce': Nonce,
      'StaticBlockReward': StaticBlockReward,
      'TxnFees': TxnFees,
      'BurntFees': BurntFees
      }
for key in dict_.keys():
    print(key,len(dict_[key]))
print(dict_)
df=pd.DataFrame(dict_)
df.to_csv('info.csv',encoding='utf-8-sig')
