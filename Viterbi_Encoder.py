inputs = ['1','0','0','1','1']
def v_xor(bit0,bit1):
    if(bit0==bit1):
        return '0'
    else:
        return '1'
def viterbi_encoder(inputs):
    #shift register encoder
    s_reg = ['0','0','0']
    obs = []
    for t in range (0,len(inputs)):
        #shifting the bits to right
        s_reg[2]=s_reg[1]
        s_reg[1]=s_reg[0]
        #inserting input
        s_reg[0]= inputs[t]
        state = s_reg[0]+ s_reg[1]
        obs.append([])
        #encoded bits
        obs[t] = v_xor(v_xor(s_reg[0],s_reg[1]),s_reg[2])+\
            v_xor(s_reg[0],s_reg[2])
    #    obs1 = ''.join(map(str, obs))
        print(s_reg,state)
    print(obs)
    #print codeword
    #print(obs1)
    #re-write list 'obs' as summable integers
    newlist = []
    # Check every item in list
    for item in obs:
      # If its a integer, add to newlist
      if isinstance(item, int):
        newlist.append(item)
        continue
      # else check and replace
      # evaluate branch combinations
      if '10' in item:
          item = item.replace('10', '1') # '10' = 1 + 0 = 1
      elif '01' in item:
          item = item.replace('01', '1') # '01' = 0 + 1 = 1
      elif '11' in item:
          item = item.replace('11', '2') # '11' = 1 + 1 = 2
      else:
          item = '0'                     # '00' = 0 + 0 = 0
     # Check other exception here
      
      newlist.append(int(item))
     
    print(newlist)
    Sum = sum(newlist)
    print(Sum)
    #Set even parity      
    if(Sum % 2 == 0):
          obs.insert(0,'0') #insert 0 bit if 'obs' is even
    else:
          obs.insert(0,'1') #insert 0 bit if 'obs' is odd
          
    print(obs) #re-print fully constructed codewrod with parity bit

viterbi_encoder(inputs)